"""Shared input fingerprints for generated public campaign assets."""
from pathlib import Path
import hashlib

def input_hashes(root: Path):
    paths=[root/'src/data/campaign.json',root/'src/data/investigation.json']
    paths+=list((root/'src/content/pages').rglob('*.md'))
    paths+=list((root/'src').rglob('*.astro'))
    paths+=[root/'scripts/generate_campaign_assets.py',root/'scripts/campaign_provenance.py']
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_text(encoding='utf-8').replace('\r\n','\n').encode()).hexdigest() for p in sorted(paths)}
