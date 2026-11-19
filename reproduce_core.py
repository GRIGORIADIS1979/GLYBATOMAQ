"""GLYBATOMAQ candidate graph transport and fixed-weight source-ledger ablation.

Run from any working directory:
  python code/reproduce_core.py
Source MOL2 records are parsed without RDKit sanitization; no chemical identity certification.
This numerical program does not perform receptor-ligand docking or biochemical prediction.
"""
from pathlib import Path
import numpy as np, csv, sys
from scipy.linalg import eigh
from rdkit import Chem, RDLogger
RDLogger.DisableLog('rdApp.*')
BASE=Path(__file__).resolve().parents[1]
SRC=BASE/'source_inputs';OUT=BASE/'computed';OUT.mkdir(exist_ok=True)
FILEMAP={
 'HSX-cons2':'GLYBATOMAQ-HSX-cons1 (1).mol2',
 'HSX-cons1':'GLYBATOMAQ-HSX-cons1 (2).mol2',
 'HSX-cons3':'GLYBATOMAQ-HSX-cons3.mol2',
 'HSX-cons4':'GLYBATOMAQ-HSX-cons4.mol2'}
EXPECTED={'HSX-cons2':92,'HSX-cons1':94,'HSX-cons3':91,'HSX-cons4':101}
RECORD=[]
for name,molfile in FILEMAP.items():
 m=Chem.MolFromMol2File(str(SRC/molfile),sanitize=False,removeHs=False,cleanupSubstructures=False)
 if m is None:raise ValueError('MOL2 parser failed: '+str(SRC/molfile))
 aa=[a.GetIdx() for a in m.GetAtoms() if a.GetAtomicNum()>1];loc={idx:i for i,idx in enumerate(aa)};n=len(loc)
 assert n==EXPECTED[name]
 W=np.zeros((n,n))
 for b in m.GetBonds():
  i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
  if i in loc and j in loc:W[loc[i],loc[j]]=W[loc[j],loc[i]]=1
 L=np.diag(W.sum(axis=1))-W
 assert np.allclose(L,L.T)
 l,V=eigh(L);lammax=max(l[-1],1.0);l=l/lammax
 psi=np.zeros(n,dtype=complex);psi[0]=1
 init=V.T.conj()@psi
 ts=np.linspace(0,9,130)
 quantum=np.array([abs(V@(np.exp(-1j*l*t)*init))**2 for t in ts])
 classical=np.array([np.clip(V@(np.exp(-l*t)*init),0,None).real for t in ts]);classical/=classical.sum(axis=1)[:,None]
 alpha=.18;mu=W.sum()/n
 WT=(1-alpha)*W +alpha*mu*(np.ones((n,n))-np.eye(n))/(n-1)
 LT=np.diag(WT.sum(axis=1))-WT;lt,VT=eigh(LT/lammax);co=VT.T.conj()@psi
 teleport=np.array([abs(VT@(np.exp(-1j*lt*t)*co))**2 for t in ts])
 err=max(abs(quantum.sum(axis=1)-1).max(),abs(teleport.sum(axis=1)-1).max())
 assert err<1e-11
 at=lambda X:float(np.interp(3,ts,X[:,0]))
 RECORD.append({'candidate':name,'n_heavy_atoms':n,'ctqw_return_t3':at(quantum),'heat_return_t3':at(classical),'teleport_return_t3':at(teleport),'max_probability_error':err})
with (OUT/'candidate_graph_transport.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,RECORD[0].keys());w.writeheader();w.writerows(RECORD)

names=list(FILEMAP)
ledger=np.array([[1,1,.980,.922,.064],[.462,.589,.934,.833,.029],[.108,.305,.924,.778,.032],[.282,.013,.882,.780,.034]])
weights=np.array([.20,.25,.20,.25])
ablations={'Full E2 fusion':(weights,True),'minus base':([0,.25,.20,.25],True),'minus DFT-proxy':([.20,0,.20,.25],True),'minus QMC proxy':([.20,.25,0,.25],True),'minus MQWalk':([.20,.25,.20,0],True),'minus diagnostic penalty':(weights,False)}
rows=[]
for label,(w,pen) in ablations.items():
 v=ledger[:,:4]@np.asarray(w)-(ledger[:,4] if pen else 0)
 order=np.argsort(-v);ranks=np.zeros(4,dtype=int);ranks[order]=np.arange(1,5)
 for i,name in enumerate(names):rows.append({'ablation':label,'candidate':name,'score':float(v[i]),'rank':int(ranks[i])})
with (OUT/'internal_score_ablations.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
assert next(x['rank'] for x in rows if x['ablation']=='minus DFT-proxy' and x['candidate']=='HSX-cons4')==3
print('PASS: four source-graph calculations and six fixed-weight ablation variants; outputs in',OUT)
