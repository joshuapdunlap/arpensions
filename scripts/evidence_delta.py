"""Local-only evidence inventory comparison. Ordinary builds never open a research vault.

The tracked snapshot stores hashed relative paths and file metadata, not private filenames.
Changes are review prompts, not proof of new holdings or completeness of a production.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,sys
ROOT=Path(__file__).resolve().parent.parent
SNAPSHOT=ROOT/'docs/evidence-inventory-snapshot.json'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--wiki',default=os.environ.get('EVIDENCE_ROOT'));parser.add_argument('--snapshot',action='store_true',help='Record metadata inventory after a deliberate review; does not certify every file as reviewed');args=parser.parse_args()
    if not args.wiki:parser.error('Supply --wiki with the local evidence-vault directory, or set EVIDENCE_ROOT. Builds do not need it.')
    wiki=Path(args.wiki).resolve()
    if not (wiki/'raw').is_dir():parser.error('Selected directory needs a raw evidence tree')
    current={};names={}
    agency_directories=sorted(p for p in (wiki/'raw').iterdir() if p.is_dir())
    for agency_directory in agency_directories:
        agency=agency_directory.name
        for path in sorted(agency_directory.rglob('*')):
            if not path.is_file():continue
            relative=path.relative_to(wiki).as_posix()
            key=hashlib.sha256(relative.encode()).hexdigest();stat=path.stat()
            current[key]={'agency':agency,'size':stat.st_size,'modifiedNs':stat.st_mtime_ns}
            names[key]=relative
    previous=json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {'files':{}}
    added=set(current)-set(previous['files']);removed=set(previous['files'])-set(current)
    changed={key for key in set(current)&set(previous['files']) if current[key]!=previous['files'][key]}
    data=json.loads((ROOT/'src/data/investigation.json').read_text(encoding='utf-8'))
    claims=json.loads((ROOT/'src/data/publication-matrix.json').read_text(encoding='utf-8'))
    affected_sources={source_id for source_id,source in data['sources'].items() if any(Path(source['originalFile']).name.casefold() in names[key].casefold() for key in added|changed)}
    affected_claims=[{'id':claim['id'],'pages':claim['pages']} for claim in claims if affected_sources&set(claim['sourceIds'])]
    report={'observedAt':datetime.now(timezone.utc).isoformat(),'comparison':'File metadata inventory; changed contents require source review','new':[names[k] for k in sorted(added)],'changed':[names[k] for k in sorted(changed)],'missingCount':len(removed),'affectedSourceIds':sorted(affected_sources),'affectedClaims':affected_claims}
    output=ROOT/'.qa/evidence-delta.json';output.parent.mkdir(exist_ok=True);output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    if args.snapshot:SNAPSHOT.write_text(json.dumps({'observedAt':report['observedAt'],'scope':'Metadata inventory across agency directories in the raw evidence tree. Inventory presence is not a source-review certification.','agencyDirectories':[p.name for p in agency_directories],'files':current},indent=2)+'\n',encoding='utf-8')
    print(f'Inventory: {len(current)} files; {len(added)} new, {len(changed)} metadata changes, {len(removed)} missing; {len(affected_claims)} potentially affected claims. Local report: .qa/evidence-delta.json')
    return 0
if __name__=='__main__':sys.exit(main())
