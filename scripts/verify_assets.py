"""Verify immutable downloads, reviewed exhibit hashes, previews, briefs and QR codes."""
from pathlib import Path
import argparse,hashlib,json,sys
from urllib.request import Request,urlopen
import fitz,zxingcpp
from PIL import Image
from campaign_provenance import input_hashes

ROOT=Path(__file__).resolve().parent.parent
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
    errors=[];data=json.loads((ROOT/'src/data/investigation.json').read_text(encoding='utf-8'));assets=json.loads((ROOT/'src/data/public-assets.json').read_text(encoding='utf-8'))
    contract=json.loads((ROOT/'tests/fixtures/compatibility.json').read_text())
    manifest=json.loads((ROOT/'src/data/campaign-assets.json').read_text(encoding='utf-8'))
    catalog=json.loads((ROOT/'src/data/download-catalog.json').read_text(encoding='utf-8'))
    actual_downloads={'/assets/documents/'+p.name for p in (ROOT/'public/assets/documents').iterdir() if p.suffix in ('.pdf','.txt')}
    catalog_urls=[item['url'] for item in catalog]
    if len(catalog_urls)!=len(set(catalog_urls)) or set(catalog_urls)!=actual_downloads:errors.append('Download catalog must cover each public PDF and TXT exactly once')
    for item in catalog:
        if not item.get('category') or not item.get('contextId'):errors.append(f'Download lacks a category or context: {item["url"]}')
        if item.get('sourceId'):
            if assets.get(item['sourceId'],{}).get('assetUrl')!=item['url']:errors.append(f'Download source does not resolve: {item["url"]}')
        else:
            if not item.get('provenance') or not item.get('scope'):errors.append(f'Download lacks provenance limitations: {item["url"]}')
            if item.get('reviewedPublicSha256') and hashlib.sha256((ROOT/'public'/item['url'].lstrip('/')).read_bytes()).hexdigest()!=item['reviewedPublicSha256']:errors.append(f'Catalog artifact differs from reviewed hash: {item["url"]}')
    if manifest['inputs']!=input_hashes(ROOT):errors.append('Generated campaign assets are stale: review changed content, rebuild Astro, and regenerate campaign assets.')
    for relative,digest in manifest['outputs'].items():
        path=ROOT/relative
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:errors.append(f'Generated campaign artifact changed: {relative}')
    for card in json.loads((ROOT/'src/data/social-cards.json').read_text(encoding='utf-8')).values():
        if Image.open(ROOT/'public'/card['url'].lstrip('/')).size!=(1200,630):errors.append('Page-specific social card has wrong dimensions: '+card['url'])
    revisions=json.loads((ROOT/'src/data/download-revisions.json').read_text(encoding='utf-8'))
    for url,revision in revisions.items():
        if url not in contract['downloads'] or revision.get('originalSha256')!=contract['downloads'].get(url):errors.append(f'Invalid historical revision baseline: {url}')
        for field in ('replacementSha256','reviewedAt','reason','originalRetained'):
            if not revision.get(field):errors.append(f'Historical revision lacks {field}: {url}')
        if revision.get('replacementSha256')==revision.get('originalSha256'):errors.append(f'Historical revision does not change the artifact: {url}')
    for url,digest in contract['downloads'].items():
        digest=revisions.get(url,{}).get('replacementSha256',digest)
        path=ROOT/'public'/url.lstrip('/')
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:errors.append(f'Historical download changed: {url}')
    for source_id,source in data['sources'].items():
        if source.get('assetUrl') and source_id not in assets:errors.append(f'{source_id}: reviewed asset manifest entry missing')
    for source_id,asset in assets.items():
        path=ROOT/'public'/asset['assetUrl'].lstrip('/')
        if not path.exists():errors.append(f'Missing {asset["assetUrl"]}');continue
        if hashlib.sha256(path.read_bytes()).hexdigest()!=asset['sha256']:errors.append(f'{source_id}: public artifact differs from reviewed hash')
        try:
            if asset.get('format')=='email-text':
                if path.read_text(encoding='utf-8').strip()!=asset['transcript'].strip():errors.append(f'{source_id}: email transcript differs from downloadable text')
                continue_pdf=True
            else:continue_pdf=False
            if continue_pdf:pass
            else:
                with fitz.open(path) as pdf:
                    if len(pdf)!=asset['pages']:errors.append(f'{source_id}: page count changed')
                    if pdf.embfile_count():errors.append(f'{source_id}: embedded attachments require review')
        except Exception as exc:errors.append(f'{source_id}: unreadable PDF {exc}')
        fields=['treatment','originalFile','originalLocator','reviewedAt','transcript']
        if asset.get('format')!='email-text':fields.append('previews')
        for field in fields:
            if not asset.get(field):errors.append(f'{source_id}: missing {field}')
        for preview in asset['previews']:
            imagepath=ROOT/'public'/preview['url'].lstrip('/')
            if not imagepath.exists():errors.append(f'Missing preview {preview["url"]}');continue
            with Image.open(imagepath) as image:
                if image.size!=(preview['width'],preview['height']):errors.append(f'{source_id}: preview dimensions changed')
    for name in ('banknote-share.jpg','banknote-share.webp'):
        payloads=[r.text for r in zxingcpp.read_barcodes(Image.open(ROOT/'public/assets/images'/name))]
        if 'https://qr.generatorqr.com/3drm7MQpG' not in payloads:errors.append(f'{name}: historical QR changed')
    og=ROOT/'public/assets/images/og-rebuild.png'
    if not og.exists() or Image.open(og).size!=(1200,630):errors.append('New social card must be 1200 × 630')
    qr=ROOT/'public/assets/images/campaign-qr.png'
    if not qr.exists() or 'https://arpensions.org/go/' not in [r.text for r in zxingcpp.read_barcodes(Image.open(qr))]:errors.append('New QR must use owned /go/ destination')
    brief=ROOT/'public/assets/documents/pension-investment-integrity-act-brief-2026-09-15.pdf'
    if not brief.exists():errors.append('Current campaign brief missing')
    else:
        with fitz.open(brief) as pdf:
            text=' '.join(' '.join(page.get_text() for page in pdf).split())
            for token in ('$25','$9.9','January 2','non-tradable sovereign debt','30 days'):
                if token not in text:errors.append(f'Current brief missing {token}')
    if args.live:
        try:
            with urlopen(Request('https://qr.generatorqr.com/3drm7MQpG',headers={'User-Agent':'arpensions-public-asset-check/2'}),timeout=20) as response:
                destination=response.geturl()
                if not destination.startswith('https://arpensions.org'):errors.append(f'Printed QR now resolves to {destination}')
                else:print('Historical printed QR resolves to arpensions.org over HTTPS.')
        except Exception as exc:errors.append(f'Live QR resolution could not be verified: {exc}')
    if errors:print('\n'.join('ERROR: '+e for e in errors));return 1
    print(f'Asset audit passed: {len(contract["downloads"])} historical PDFs ({len(revisions)} documented privacy revisions), {len(assets)} reviewed source exhibits, social card and QR codes.');return 0
if __name__=='__main__':sys.exit(main())
