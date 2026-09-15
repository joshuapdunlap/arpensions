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
    if manifest['inputs']!=input_hashes(ROOT):errors.append('Generated campaign assets are stale: review changed content, rebuild Astro, and regenerate campaign assets.')
    for relative,digest in manifest['outputs'].items():
        path=ROOT/relative
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:errors.append(f'Generated campaign artifact changed: {relative}')
    for card in json.loads((ROOT/'src/data/social-cards.json').read_text(encoding='utf-8')).values():
        if Image.open(ROOT/'public'/card['url'].lstrip('/')).size!=(1200,630):errors.append('Page-specific social card has wrong dimensions: '+card['url'])
    for url,digest in contract['downloads'].items():
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
    print(f'Asset audit passed: {len(contract["downloads"])} immutable PDFs, {len(assets)} reviewed source exhibits, social card and QR codes.');return 0
if __name__=='__main__':sys.exit(main())
