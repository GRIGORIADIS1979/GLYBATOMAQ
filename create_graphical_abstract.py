from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np,csv
ROOT=Path(__file__).resolve().parents[1]
DARK='#102b42';TEAL='#078da2';NAVY='#173f60';GOLD='#d89417';GREY='#596b77';PALE='#eef6f7'
fig=plt.figure(figsize=(18,10),facecolor='white')
ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,18);ax.set_ylim(0,10);ax.axis('off')
def text(x,y,s,size=12,color=DARK,weight='normal',ha='left',va='center',**kw):
 ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,ha=ha,va=va,**kw)
def panel(x,y,w,h,label,title):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=.13',facecolor='white',edgecolor='#b4cfd4',linewidth=1.4))
 ax.add_patch(FancyBboxPatch((x+.01,y+h-.55),w-.02,.54,boxstyle='round,pad=0.02,rounding_size=.12',facecolor=NAVY,edgecolor=NAVY))
 text(x+.2,y+h-.26,label+'  '+title,13,'white','bold')

ax.add_patch(FancyBboxPatch((.1,9.08),17.8,.78,boxstyle='round,pad=.02,rounding_size=.16',facecolor=NAVY,edgecolor=NAVY))
text(.37,9.51,'GLYBATOMAQ™',24,'white','bold')
text(4.4,9.52,'CTQW–MQWalk–MBHA for GLIPR1-Focused In Silico Prioritization',17,'white','bold')
text(4.41,9.22,'Molecular source records  •  normalized operator geometry  •  transport and ablation audit',10.5,'#c9e7ed')
W=5.63; XS=[.35,6.18,12.01]
for x,y,label,title in [(XS[0],4.86,'A','CHEMICAL PROVENANCE'),(XS[1],4.86,'B','HMC & OPERATOR KERNELS'),(XS[2],4.86,'C','QUANTUM GRAPH TRANSPORT'),(XS[0],.87,'D','EVIDENCE FUSION & ABLATION'),(XS[1],.87,'E','REPRODUCIBLE EXECUTION'),(XS[2],.87,'F','RECEPTOR-AWARE EVALUATION')]:panel(x,y,W,3.97,label,title)
# A chemical provenance
x=XS[0]; y=4.86
text(x+.23,y+3.02,'Four source-defined molecular graphs',12,weight='bold')
for k,(name,n) in enumerate([('HSX-cons2',92),('HSX-cons1',94),('HSX-cons3',91),('HSX-cons4',101)]):
 yy=y+2.56-.53*k
 ax.add_patch(Circle((x+.44,yy),.12,facecolor=[TEAL,'#5a8bc7',GOLD,'#8c70bf'][k],edgecolor='white'))
 text(x+.69,yy,f'{name}    {n} heavy atoms',11.5)
text(x+.24,y+.48,'MOL2/PDB source crosswalk; identity gate tracked',10,color=GREY)
text(x+.24,y+.22,'Original 2GLI and GLIPR1 evidence remain distinct',9.7,color=GREY)
# B HMC
x=XS[1]
text(x+.23,y+3.05,'Six-module chemistry-safe path',12,weight='bold')
labels=['M1','M2','M3','M4','M5','M6']
for k,c in enumerate(labels):
 xx=x+.48+k*.91
 ax.add_patch(Circle((xx,y+2.23),.24,facecolor=[NAVY,'#158ec2','#18966f','#d9a224','#dd7743','#8062b7'][k],edgecolor='white'))
 text(xx,y+2.23,c,10,'white','bold','center')
 if k<5:ax.add_patch(FancyArrowPatch((xx+.23,y+2.23),(xx+.68,y+2.23),arrowstyle='-|>',mutation_scale=12,color=GREY,linewidth=1.2))
text(x+.22,y+1.47,'ρ(X) = XXᵀ / Tr(XXᵀ)    •    Kᵢⱼ = Tr(ρᵢρⱼ)',11)
text(x+.22,y+1.03,'K ⪰ 0       dFS = arccos |overlap|',11)
text(x+.22,y+.50,'PSD overlap • Bures control • geometry gates',9.8,color=GREY)
# C Plot CTQW vs heat actual return prob across candidate, no invented curves
x=XS[2]
text(x+.24,y+3.09,'Source-graph node-zero return mass at t = 3',11.5,weight='bold')
records=list(csv.DictReader(open(ROOT/'computed/candidate_graph_transport.csv')))
chart=fig.add_axes([(x+.38)/18,(y+1.13)/10,4.85/18,1.56/10])
arr=np.arange(4); q=[float(r['ctqw_return_t3']) for r in records]; h=[float(r['heat_return_t3']) for r in records]
chart.bar(arr-.16,q,width=.32,color=TEAL,label='CTQW')
chart.bar(arr+.16,h,width=.32,color='#b0b6c3',label='Heat')
chart.set_xticks(arr,['c2','c1','c3','c4']);chart.set_ylim(0,1);chart.spines[['top','right']].set_visible(False);chart.tick_params(labelsize=9)
chart.legend(loc='upper right',frameon=False,fontsize=9,ncol=2)
text(x+.23,y+.45,'U(t) = exp(−itH),  H = D − W;   ∑ⱼ pⱼ(t) = 1',10.6)
# D fusion
x=XS[0];y=.87
text(x+.23,y+3.03,'Internal E2 fixed-weight source ledger',11.8,weight='bold')
chart=fig.add_axes([(x+.36)/18,(y+1.37)/10,4.9/18,1.45/10])
sc=[.8125,.6057,.44515,.39705]
chart.barh(['cons2','cons1','cons3','cons4'][::-1],sc[::-1],color=[TEAL,'#3aa8ba','#65bec7','#9bced2'][::-1]);chart.set_xlim(0,.9)
chart.spines[['top','right']].set_visible(False);chart.tick_params(labelsize=9)
text(x+.24,y+.79,'S = 0.20B + 0.25D + 0.20Q + 0.25M − Π',10.5)
text(x+.24,y+.39,'Leave-DFT-out reverses ranks of cons3 and cons4',10,color=GREY)
# E portability
x=XS[1]
text(x+.25,y+3.08,'One source → three execution strata',12,weight='bold')
steps=[('1  Python · SciPy · RDKit','MOL2 → Laplacian → exact CTQW'),('2  IBM Qiskit','2-qubit Pauli evolution demonstrator'),('3  Rigetti pyQuil','2-qubit port; pyQVM/authorized QPU')]
for k,(a,b) in enumerate(steps):
 yy=y+2.42-k*.81
 ax.add_patch(FancyBboxPatch((x+.25,yy-.29),5.1,.62,boxstyle='round,pad=.02,rounding_size=.06',facecolor=PALE,edgecolor='#cadee4',linewidth=1))
 text(x+.46,yy+.11,a,11,weight='bold');text(x+.46,yy-.14,b,9.4,color=GREY)
text(x+.25,y+.33,'Hashes · config · versions · shots · backend/job IDs',9.8,color=GREY)
# F context
x=XS[2]
text(x+.26,y+3.06,'Source-consistent interpretation',12,weight='bold')
notes=['GLIPR1 structures: PDB 3Q2U / 3Q2R','Archival 2GLI docking: GLI–DNA context','Rank movement + source evidence audited','Transport invariants + classical heat controls']
for k,n in enumerate(notes):
 yy=y+2.47-k*.58
 ax.add_patch(Circle((x+.36,yy),.08,facecolor=TEAL,edgecolor='white'))
 text(x+.55,yy,n,10.3)
text(x+.25,y+.28,'Next application: matched receptor docking and validation',9.6,color=GREY)
ax.add_patch(FancyBboxPatch((.1,.14),17.8,.51,boxstyle='round,pad=.01,rounding_size=.08',facecolor='#e7f3f5',edgecolor='#b9d5dc'))
text(9,.40,'Core result: chemistry-gated, operator-consistent, reproducible rank auditing with CTQW–MQWalk transport and projected MBHA',12.2,DARK,'bold','center')
out=ROOT/'figures/GLYBATOMAQ_Graphical_Abstract_Research.png'
fig.savefig(out,dpi=220,facecolor='white',bbox_inches='tight',pad_inches=.12)
fig.savefig(ROOT/'figures/GLYBATOMAQ_Graphical_Abstract_Research.pdf',facecolor='white',bbox_inches='tight',pad_inches=.12)
print(out)
