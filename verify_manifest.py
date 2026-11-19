"""Verify source-file integrity and reproducible archive manifest."""
from pathlib import Path
import csv,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'SHA256_manifest.csv').open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
fail=[]
for r in rows:
  path=ROOT/r['path']
  if not path.is_file(): fail.append((r['path'],'missing')); continue
  if hashlib.sha256(path.read_bytes()).hexdigest()!=r['sha256'] or path.stat().st_size!=int(r['bytes']):fail.append((r['path'],'hash mismatch'))
if fail:
 print('FAIL',fail);sys.exit(1)
print('PASS:',len(rows),'files match manifest')
