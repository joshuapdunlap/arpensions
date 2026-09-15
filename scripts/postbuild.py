"""Preserve published fragment addresses and enhance static table readability."""
from pathlib import Path
from bs4 import BeautifulSoup
import json

root=Path(__file__).resolve().parent.parent
legacy=json.loads((root/'src/data/legacy-anchors.json').read_text())
for path in (root/'dist').rglob('*.html'):
    rel=path.relative_to(root/'dist').as_posix()
    route='/'+(rel[:-10] if rel.endswith('index.html') else rel)
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    main=soup.find('main')
    if not main: continue
    for old_id in legacy['anchors'].get(route,[]):
        if soup.find(id=old_id):continue
        target_id=legacy['targets'].get(route,{}).get(old_id,old_id)
        target=soup.find(id=target_id)
        if target is None:target=soup.find('h1') or main
        anchor=soup.new_tag('span',id=old_id)
        anchor['class']='legacy-anchor'
        anchor['aria-hidden']='true'
        target.insert_before(anchor)
    for i,table in enumerate(soup.select('.prose table')):
        if table.parent and 'table-scroll' in table.parent.get('class',[]): continue
        wrapper=soup.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':f'Scrollable data table {i+1}'})
        table.wrap(wrapper)
        for th in table.select('thead th'):th['scope']='col'
    path.write_text(str(soup),encoding='utf-8')
print('Preserved legacy fragments and wrapped wide data tables.')
