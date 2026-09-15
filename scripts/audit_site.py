"""Audit approved source relationships and the actual Astro publication surface."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
import argparse, gzip, json, re, sys, yaml
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parent.parent

def audit(site=None):
    errors=[]
    data=json.loads((ROOT/'src/data/investigation.json').read_text(encoding='utf-8'))
    claims=json.loads((ROOT/'src/data/publication-matrix.json').read_text(encoding='utf-8'))
    sources=data['sources']
    financial_ids={r['id'] for r in data['financialRecords']}
    for row in data['financialRecords']:
        for related_id in row.get('overlapsRecordIds',[])+([row['parentFundingId']] if row.get('parentFundingId') else []):
            if related_id not in financial_ids:errors.append(f'Unknown related financial record {related_id}')
    for collection in (data['financialRecords'],data['timeline'],claims):
        for row in collection:
            for source_id in row['sourceIds']:
                if source_id not in sources: errors.append(f"Unknown source {source_id} in {row['id']}")
    for claim in claims:
        for field in ('claim','locator','scope','asOf','boundary','pages'):
            if not claim.get(field): errors.append(f"Claim {claim['id']} needs {field}")
    for path in (ROOT/'src/content/pages').rglob('*.md'):
        text=path.read_text(encoding='utf-8')
        frontmatter=yaml.safe_load(text.split('---',2)[1])
        for source_id in frontmatter.get('sourceIds',[]):
            if source_id not in sources:errors.append(f'{path.relative_to(ROOT)}: unknown source {source_id}')
        if '{%' in text or '{{ site' in text:errors.append(f'Unmigrated Liquid in {path.relative_to(ROOT)}')
        if re.search(r'[CD]:[\\/]|AR_DL\.png',text):errors.append(f'Private local path in {path.relative_to(ROOT)}')
    if site:
        site=Path(site)
        contract=json.loads((ROOT/'tests/fixtures/compatibility.json').read_text())
        documents={}
        cards=json.loads((ROOT/'src/data/social-cards.json').read_text(encoding='utf-8'))
        def target(url):
            path=site/unquote(urlsplit(url).path).lstrip('/')
            return path/'index.html' if not path.suffix else path
        for path in site.rglob('*.html'):
            soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser');documents[path.resolve()]=soup
            relative=str(path.relative_to(site))
            if len(soup.select('h1'))!=1:errors.append(f'{relative}: needs exactly one H1')
            if not soup.select_one('html[lang="en"]'):errors.append(f'{relative}: missing language')
            for selector in ('title','meta[name="description"]','link[rel="canonical"]','meta[property="og:image"]','main','a.skip-link'):
                if not soup.select_one(selector): errors.append(f'{relative}: missing {selector}')
            if not soup.select_one('meta[name="robots"][content^="noindex"]'):
                route=urlsplit(soup.select_one('link[rel="canonical"]')['href']).path
                card=cards.get(route)
                if not card or card['title']!=soup.select_one('meta[property="og:title"]')['content']:errors.append(f'{relative}: social card title is stale; rebuild Astro, regenerate campaign assets, then validate.')
                elif soup.select_one('meta[property="og:image"]')['content']!='https://arpensions.org'+card['url']:errors.append(f'{relative}: page-specific social card metadata missing')
            ids=[el['id'] for el in soup.select('[id]')]
            duplicates=[key for key,count in Counter(ids).items() if count>1]
            if duplicates:errors.append(f'{relative}: duplicate IDs {duplicates}')
            for image in soup.select('img'):
                if not image.has_attr('alt') or not image.get('width') or not image.get('height'):errors.append(f'{relative}: image needs alt and dimensions {image.get("src")}')
            for iframe in soup.select('iframe'):
                if not iframe.get('title'):errors.append(f'{relative}: iframe needs title')
            for script in soup.select('script[src]'):
                if urlsplit(script['src']).netloc:errors.append(f'{relative}: unexpected third-party initial script')
            public_text=soup.get_text(' ',strip=True)
            if re.search(r'[CD]:[\\/]|AR_DL\.png',public_text):errors.append(f'{relative}: private local path leaked')
            for tag in soup.select('[href],[src]'):
                url=tag.get('href') or tag.get('src') or ''
                split=urlsplit(url)
                if split.scheme or split.netloc or not url:continue
                dest=path if url.startswith('#') else target(url) if url.startswith('/') else path.parent/unquote(split.path)
                if dest.is_dir():dest=dest/'index.html'
                if not dest.exists():errors.append(f'{relative}: missing link or asset {url}')
                elif split.fragment and dest.suffix=='.html':
                    destsoup=documents.get(dest.resolve()) or BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser')
                    if not destsoup.find(id=unquote(split.fragment)):errors.append(f'{relative}: missing fragment {url}')
        for route in contract['routes']:
            path=target(route)
            if not path.exists():errors.append(f'Lost legacy route {route}');continue
            soup=documents[path.resolve()]
            for anchor in contract['anchors'].get(route,[]):
                if not soup.find(id=anchor):errors.append(f'Lost legacy fragment {route}#{anchor}')
        for claim in claims:
            for route in claim['pages']:
                if not target(route).exists():errors.append(f"Claim {claim['id']} references missing page {route}")
        for path,budget in ((site/'index.html',50*1024),(site/'evidence/index.html',100*1024)):
            if not path.exists():continue
            soup=documents[path.resolve()];js=0
            for script in soup.select('script'):
                if script.get('type')=='application/ld+json':continue
                src=script.get('src');file=site/src.lstrip('/') if src else None
                if file and file.exists():js+=len(gzip.compress(file.read_bytes(),mtime=0))
                elif not src:js+=len(gzip.compress(script.get_text().encode(),mtime=0))
            if js>budget:errors.append(f'{path.name}: compressed initial JS {js} exceeds {budget}')
            print(f'{path.relative_to(site)} initial compressed first-party JavaScript: {js:,} bytes')
        css=sum(len(gzip.compress(p.read_bytes(),mtime=0)) for p in (site/'_astro').glob('*.css'))
        if css>40*1024:errors.append(f'Shared compressed CSS {css} exceeds 40 KB')
        if not (site/'pagefind/pagefind.js').exists():errors.append('Pagefind search bundle missing')
        if (site/'CNAME').read_text().strip()!='arpensions.org':errors.append('Custom domain missing')
        print(f'Rendered {len(documents)} HTML pages; shared compressed CSS: {css:,} bytes')
    if errors:
        print('\n'.join(f'ERROR: {e}' for e in sorted(set(errors))));return 1
    print(f'Publication audit passed: {len(claims)} claims and {len(sources)} source references.');return 0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--site-dir','--site',dest='site');args=parser.parse_args();sys.exit(audit(args.site))
