"""Reproducible MBHA search *demonstrator* over the 4-record E2 source ledger.

This runs a constrained, seed-fixed population heuristic on already known
score records. It does not redock molecules, optimize chemical structures, or
provide a meaningful performance benchmark against other optimizers.
"""
from pathlib import Path
import numpy as np,csv,json
ROOT=Path(__file__).resolve().parents[1]
NAMES=['HSX-cons2','HSX-cons1','HSX-cons3','HSX-cons4']
EVIDENCE=np.array([[1,1,.980,.922,.064], [.462,.589,.934,.833,.029], [.108,.305,.924,.778,.032], [.282,.013,.882,.780,.034]],float)
COEFF=np.array([.20,.25,.20,.25])
SCORES=EVIDENCE[:,:4]@COEFF-EVIDENCE[:,4]
# Descriptors here are source *support-vector* coordinates, not chemical identity descriptors.
F=EVIDENCE[:,:4]
S=(F-F.mean(axis=0))/(F.std(axis=0)+1e-8)

def nearest(pos):
    distances=np.sum((S-pos)**2,axis=1)
    return int(np.argmin(distances))  # stable source order for exact ties

def run(seed=1729,pop_size=16,epochs=25,eta=.28,jitter=.05):
    rng=np.random.default_rng(seed)
    population=rng.integers(0,len(NAMES),size=pop_size)
    # Keep a deterministic elite (best in the fixed source table) within the sampled pool.
    elite_idx=int(population[np.argmax(SCORES[population])])
    history=[]
    for step in range(epochs+1):
        best_idx=int(population[np.argmax(SCORES[population])])
        if SCORES[best_idx]>SCORES[elite_idx]:elite_idx=best_idx
        history.append({'generation':step,'elite_id':NAMES[elite_idx], 'elite_score':float(SCORES[elite_idx]),'unique_ids':len(set(population.tolist()))})
        if step==epochs:break
        for i in range(pop_size):
            # Exact elite retention; finite projection onto admissible IDs.
            if i==0:
                population[i]=elite_idx
            else:
                p=(1-eta)*S[population[i]]+eta*S[elite_idx]+jitter*rng.standard_normal(S.shape[1]); population[i]=nearest(p)
                # Controlled renewal (the source data table is unchanged).
                if rng.random()<.07:population[i]=rng.integers(0,len(NAMES))
    assert all(history[k]['elite_score']<=history[k+1]['elite_score']+1e-12 for k in range(len(history)-1))
    return history

if __name__=='__main__':
    h=run()
    f=ROOT/'computed/mbha_fixed_library_trace.csv'
    with f.open('w',newline='') as w:
       writer=csv.DictWriter(w,h[0].keys());writer.writeheader();writer.writerows(h)
    print(json.dumps({'run_type':'four-entry fixed-ledger MBHA algorithm smoke test','seed':1729,'generations':len(h)-1,'final':h[-1]},indent=2))
