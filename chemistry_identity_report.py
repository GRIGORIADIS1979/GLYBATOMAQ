"""Audit identity and sanitization status of four source-defined GLYBATOMAQ records.
Writes computed/chemical_identity_audit.csv. A successful parser is NOT a
proof that the supplied IUPAC name or stereochemistry is chemically correct.
"""
from pathlib import Path
import csv
from rdkit import Chem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
ROOT=Path(__file__).resolve().parents[1]
FILES=[('HSX-cons2','GLYBATOMAQ-HSX-cons1 (1).mol2',92),('HSX-cons1','GLYBATOMAQ-HSX-cons1 (2).mol2',94),('HSX-cons3','GLYBATOMAQ-HSX-cons3.mol2',91),('HSX-cons4','GLYBATOMAQ-HSX-cons4.mol2',101)]
rows=[]
for name,filename,expected in FILES:
    path=ROOT/'source_inputs'/filename
    mol=Chem.MolFromMol2File(str(path),sanitize=False,removeHs=False,cleanupSubstructures=False)
    if mol is None:raise RuntimeError('MOL2 parser failed: '+filename)
    count=sum(a.GetAtomicNum()>1 for a in mol.GetAtoms())
    if count!=expected:raise AssertionError((name,count,expected))
    try:
        Chem.SanitizeMol(Chem.Mol(mol))
        s='passed';err=''
    except Exception as exc:
        s='failed';err=str(exc).replace('\\n',' ')[:240]
    formal_charge=sum(a.GetFormalCharge() for a in mol.GetAtoms())
    rows.append({'candidate':name,'source_mol2_file':filename,'n_atoms_in_source_record':mol.GetNumAtoms(),'n_heavy_atoms':count,'n_bonds':mol.GetNumBonds(),'source_formal_charge_sum':formal_charge,'full_rdkit_sanitization':s,'sanitize_error_excerpt':err,'preferred_iupac_verified':'false'})
out=ROOT/'computed'/'chemical_identity_audit.csv';out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',newline='') as f:
    writer=csv.DictWriter(f,rows[0].keys());writer.writeheader();writer.writerows(rows)
print('PASS: source parsing / heavy atom counts; certified IUPAC names: none claimed')
for r in rows:print(r['candidate'],r['n_heavy_atoms'],r['full_rdkit_sanitization'])
