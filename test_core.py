"""Simple no-pytest core checks after running code/reproduce_core.py."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
def main():
  with open(ROOT/'computed/candidate_graph_transport.csv',newline='') as f: a=list(csv.DictReader(f))
  assert len(a)==4
  assert [int(x['n_heavy_atoms']) for x in a]==[92,94,91,101]
  assert all(float(x['max_probability_error']) < 1e-11 for x in a)
  with open(ROOT/'computed/internal_score_ablations.csv',newline='') as f: b=list(csv.DictReader(f))
  assert len(b)==24
  full={v['candidate']:float(v['score']) for v in b if v['ablation']=='Full E2 fusion'}
  assert abs(full['HSX-cons2']-.8125)<1e-10
  assert abs(full['HSX-cons4']-.39705)<1e-10
  dn={v['candidate']:int(v['rank']) for v in b if v['ablation']=='minus DFT-proxy'}
  assert (dn['HSX-cons3'],dn['HSX-cons4'])==(4,3)
  print('PASS: graph sizes, conservation, source fusion and DFT ablation')
if __name__=='__main__':main()
