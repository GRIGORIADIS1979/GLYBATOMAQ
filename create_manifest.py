"""Rebuild a deterministic SHA-256 manifest for all repository files except the manifest itself."""
from pathlib import Path
import csv, hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'SHA256_manifest.csv'
paths=[p for p in ROOT.rglob('*') if p.is_file() and p!=manifest and '__pycache__' not in p.parts and not p.name.startswith('.DS_Store')]
rows=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(paths)]
with manifest.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['path','sha256','bytes']);w.writeheader();w.writerows(rows)
print('Wrote SHA256_manifest.csv for',len(rows),'files')
