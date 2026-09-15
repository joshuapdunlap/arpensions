"""Keep the public letter and its download aligned with approved structured copy."""
from pathlib import Path
from html import escape
import argparse,json,re,sys
ROOT=Path(__file__).resolve().parent.parent
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    campaign=json.loads((ROOT/'src/data/campaign.json').read_text(encoding='utf-8'))
    letter=campaign['letter']
    block='<!-- campaign-letter:start -->\n<div class="copy-row"><button type="button" hidden data-copy="legislator-letter">Copy letter template</button><span role="status" aria-live="polite"></span></div>\n<blockquote class="letter-box" id="legislator-letter">'+escape(letter)+'</blockquote>\n\n[Download the plain-text letter](/assets/documents/legislator-letter-2026-09-15.txt). Personalize it before sending.\n<!-- campaign-letter:end -->'
    path=ROOT/'src/content/pages/take-action.md';text=path.read_text(encoding='utf-8')
    pattern=r'<!-- campaign-letter:start -->.*?<!-- campaign-letter:end -->'
    updated=re.sub(pattern,lambda _:block,text,flags=re.S)
    if not re.search(pattern,text,re.S):
        updated=re.sub(r'> Dear Senator or Representative,.*?(?=\nSources for the letter:)',lambda _:block+'\n',text,flags=re.S)
    download=ROOT/'public/assets/documents/legislator-letter-2026-09-15.txt'
    if args.write:path.write_text(updated,encoding='utf-8',newline='\n');download.write_text(letter+'\n',encoding='utf-8',newline='\n');print('Shared letter synchronized.');return 0
    if updated!=text or not download.exists() or download.read_text(encoding='utf-8').strip()!=letter.strip():print('Shared campaign letter is out of sync. Run python scripts/sync_campaign_content.py --write after editorial review.');return 1
    print('Shared campaign letter and download agree.');return 0
if __name__=='__main__':sys.exit(main())
