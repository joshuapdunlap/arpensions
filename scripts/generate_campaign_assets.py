"""Generate current campaign PDF, QR and social card from approved structured content.

Optional authoring step, never required by ordinary builds. Install requirements-authoring.txt.
Run after npm ci so the licensed self-hosted font files are available.
"""
from pathlib import Path
import json,math,hashlib,sys
from html import escape
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
import qrcode
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from campaign_provenance import input_hashes
from datetime import date

ROOT=Path(__file__).resolve().parent.parent
data=json.loads((ROOT/'src/data/investigation.json').read_text(encoding='utf-8'))
campaign=json.loads((ROOT/'src/data/campaign.json').read_text(encoding='utf-8'))
campaign_date=date.fromisoformat(campaign['date'])
date_label=f'{campaign_date.strftime("%B")} {campaign_date.day}, {campaign_date.year}'
letter_path=ROOT/f'public/assets/documents/legislator-letter-{campaign["date"]}.txt'
records={row['id']:row for row in data['financialRecords']}
def millions(id):return f'${records[id]["amount"]/1_000_000:g} million'
def record_date(id):
    value=date.fromisoformat(records[id]['effectiveDate'])
    return f'{value.strftime("%B")} {value.day}, {value.year}'
tmp=ROOT/'.qa/campaign-fonts';tmp.mkdir(parents=True,exist_ok=True)
fontpaths={}
for name,package,file,weight in [('Spartan','@fontsource-variable/league-spartan','league-spartan-latin-wght-normal.woff2',650),('Mulish','@fontsource-variable/mulish','mulish-latin-wght-normal.woff2',400),('MulishBold','@fontsource-variable/mulish','mulish-latin-wght-normal.woff2',800),('Mono','@fontsource/ibm-plex-mono','ibm-plex-mono-latin-400-normal.woff2',None)]:
    font=FontFile(ROOT/'node_modules'/package/'files'/file)
    if weight:font=instantiateVariableFont(font,{'wght':weight},inplace=True)
    font.flavor=None;target=tmp/f'{name}.ttf';font.save(target);fontpaths[name]=target
    pdfmetrics.registerFont(TTFont(name,str(target)))
pdfmetrics.registerFontFamily('Mulish',normal='Mulish',bold='MulishBold')
images=ROOT/'public/assets/images';docs=ROOT/'public/assets/documents'
qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=12,border=4)
qr.add_data('https://arpensions.org/go/');qr.make(fit=True);qr.make_image(fill_color='#013237',back_color='white').save(images/'campaign-qr.png')

# Original typographic campaign artwork; no source evidence is simulated here.
im=Image.new('RGB',(1200,630),'#013237');draw=ImageDraw.Draw(im)
for j in range(22):
    points=[]
    for i in range(481):
        t=i*math.pi/240;r=160+j*2.1+14*math.sin(12*t+j*.17)
        points.append((997+r*math.cos(t),315+r*math.sin(t)))
    draw.line(points,fill='#28654e',width=1)
draw.line((48,64,1152,64),fill='#5b8d70',width=1)
mono=ImageFont.truetype(str(fontpaths['Mono']),14);display=ImageFont.truetype(str(fontpaths['Spartan']),79)
draw.text((48,29),'ARKANSANS FOR PENSION INTEGRITY',font=mono,fill='#c8e7c9')
draw.text((48,126),'Public money\ndeserves a public\ninvestment record.',font=display,fill='#e6f9e4',spacing=8)
draw.text((48,497),'SUPPORT THE PENSION INVESTMENT INTEGRITY ACT',font=mono,fill='#aad3b2')
draw.line((48,558,1152,558),fill='#5b8d70',width=1)
draw.text((48,585),'ARPENSIONS.ORG',font=mono,fill='#c8e7c9')
im.save(images/'og-rebuild.png',optimize=True)

pdf=canvas.Canvas(str(docs/f'pension-investment-integrity-act-brief-{campaign["date"]}.pdf'),pagesize=(612,792),invariant=1)
pdf.setTitle(f'Pension Investment Integrity Act | {date_label}')
pdf.setAuthor('Arkansans for Pension Integrity')
pine=HexColor('#013237');muted=HexColor('#496354');rule=HexColor('#b8cdbb')
styles={
 'body':ParagraphStyle('body',fontName='Mulish',fontSize=9.2,leading=13,textColor=pine,spaceAfter=0),
 'small':ParagraphStyle('small',fontName='Mulish',fontSize=8.1,leading=11.5,textColor=muted),
 'h2':ParagraphStyle('h2',fontName='Spartan',fontSize=16,leading=18,textColor=pine),
}
def para(text,x,y,width,style='body'):
    p=Paragraph(text,styles[style]);_,h=p.wrap(width,900);p.drawOn(pdf,x,y-h);return y-h
pdf.setFillColor(pine);pdf.rect(0,686,612,106,fill=1,stroke=0)
pdf.setFillColor(HexColor('#bde0c2'));pdf.setFont('Mono',8.5);pdf.drawString(38,762,'ARKANSANS FOR PENSION INTEGRITY  /  '+date_label.upper())
pdf.setFillColor(HexColor('#e6f9e4'));pdf.setFont('Spartan',27);pdf.drawString(38,726,'Pension Investment Integrity Act')
pdf.setFont('Mulish',10);pdf.drawString(38,704,'A campaign proposal for the 2027 Arkansas regular session')
y=665
y=para('<b>'+escape(campaign['headline'])+'</b> '+escape(data['policy']['summary']),38,y,536)-17
y=para('THE DOCUMENTED PENSION RECORD',38,y,536,'h2')-10
pdf.setStrokeColor(rule);pdf.line(38,y,574,y);y-=13
y=para(f'<b>APERS: {millions("apers_september_holding")} par.</b> Two positions in the {record_date("apers_september_holding")} custody report, marked preliminary. The earlier {millions("apers_october_purchase")} purchase is a historical event. Allocation among APERS-administered systems remains unresolved.',38,y,536)-8
y=para(f'<b>ATRS: {millions("atrs_february_purchase")} par.</b> Completed bond purchase {record_date("atrs_february_purchase")}, inside the {millions("atrs_january_funding")} manager account funded {record_date("atrs_january_funding")}. The account also held U.S. Treasuries and cash. Funding and its underlying bond must not be added together.',38,y,536)-15
y=para('FIVE REQUIREMENTS FOR COVERED ACQUISITIONS',38,y,536,'h2')-9
for i,item in enumerate(data['requirements']):
    y=para(f'<b>{i+1}. {escape(item["title"])}.</b> {escape(item["description"])}',38,y,536)-7
y-=6
y=para('HOW THE PROPOSAL WOULD WORK',38,y,536,'h2')-8
y=para(escape(campaign['operatingSummary']),38,y,536)-8
y=para('Help develop the proposal and consider sponsorship. Legal drafting, enforcement, contract transition and cost review remain pending. Request a briefing: <b>info@arpensions.org</b>. Full coverage, operating examples and calendar: <b>arpensions.org/the-act/</b>.',38,y,536)-14
pdf.setStrokeColor(rule);pdf.line(38,y,574,y);y-=10
y=para('<b>Source trail:</b> APERS September custody, physical p.1; ATRS completed funding, p.3; ATRS completed trade, transaction row2. Aon’s implementation and manager-selection advice is substantive; the campaign asks for a consistent decision-specific financial explanation. Reviewed source exhibits: <b>arpensions.org/documents/</b>.',38,y,450,'small')-8
pdf.drawImage(str(images/'campaign-qr.png'),515,y+8,width=58,height=58)
pdf.linkURL('https://arpensions.org/go/',(515,y+8,573,y+66),relative=0)
if y<36:raise RuntimeError(f'Brief exceeds one-page space: baseline {y}')
pdf.setFont('Mono',7.5);pdf.setFillColor(muted);pdf.drawString(38,25,'ARPENSIONS.ORG  |  CURRENT BRIEF  |  REVIEWED '+campaign['date'])
pdf.linkURL('https://arpensions.org/the-act/',(38,20,350,36),relative=0)
pdf.showPage();pdf.save()
letter_path.write_text(campaign['letter']+'\n',encoding='utf-8',newline='\n')
if '--brief-only' in sys.argv:
    print('Generated current brief and letter for the initial authoring build. Run the full generator after Astro builds.')
    sys.exit(0)

# Page-specific PNG cards use the same reviewed titles as the static release.
# Run the Astro build before authoring, then rebuild to apply this route map.
cards={};card_dir=images/'social-cards';card_dir.mkdir(exist_ok=True)
for page in sorted((ROOT/'dist').rglob('*.html')):
    soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
    if soup.select_one('meta[name="robots"][content^="noindex"]'):continue
    route=urlsplit(soup.select_one('link[rel="canonical"]')['href']).path
    title=soup.select_one('meta[property="og:title"]')['content']
    filename=('home' if route=='/' else route.strip('/').replace('/','--'))+'.png'
    card=im.copy();d=ImageDraw.Draw(card)
    d.rectangle((0,82,792,549),fill='#013237')
    for size in range(76,37,-2):
        font=ImageFont.truetype(str(fontpaths['Spartan']),size);lines=[];line=''
        for word in title.split():
            candidate=(line+' '+word).strip()
            if d.textlength(candidate,font=font)>700 and line:lines.append(line);line=word
            else:line=candidate
        if line:lines.append(line)
        if len(lines)*(size+7)<=335:break
    d.multiline_text((48,130),'\n'.join(lines),font=font,fill='#e6f9e4',spacing=7)
    d.text((48,497),'THE PUBLIC RECORD  /  THE CASE FOR REFORM',font=mono,fill='#aad3b2')
    sealfont=ImageFont.truetype(str(fontpaths['Mono']),23)
    for y,text in [(286,'PUBLIC'),(320,'RECORD')]:
        d.text((997-d.textlength(text,font=sealfont)/2,y),text,font=sealfont,fill='#bde0c2')
    card.save(card_dir/filename,optimize=True)
    cards[route]={'url':'/assets/images/social-cards/'+filename,'title':title}
if len(cards)<60:raise RuntimeError('Build the complete Astro site before generating social cards.')
(ROOT/'src/data/social-cards.json').write_text(json.dumps(cards,indent=2)+'\n',encoding='utf-8',newline='\n')

outputs=[docs/f'pension-investment-integrity-act-brief-{campaign["date"]}.pdf',letter_path,images/'campaign-qr.png',images/'og-rebuild.png',ROOT/'src/data/social-cards.json']+list(card_dir.glob('*.png'))
manifest={'inputs':input_hashes(ROOT),'outputs':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(outputs)}}
(ROOT/'src/data/campaign-assets.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
print(f'Generated one-page brief, shared letter, {len(cards)} page-specific social cards, and owned QR destination. Recorded input and artifact fingerprints.')
