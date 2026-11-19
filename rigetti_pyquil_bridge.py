"""Optional Rigetti pyQuil 4.x portability test on a 2-qubit circuit.

This gate-sequence smoke test matches an IBM/Qiskit portable circuit pattern;
it is NOT an implementation of the full 92--101-atom CTQW Hamiltonians.
By default use 2q-pyqvm, no hardware access. Set RIGETTI_QC_NAME only
when authenticated and authorized to use a specified QPU.
"""
import os
import json
import numpy as np
from pyquil import Program, get_qc
from pyquil.gates import H, CNOT, RZ, MEASURE

def main():
    shots=int(os.environ.get('GLY_SHOTS','2048'))
    theta=0.6
    name=os.environ.get('RIGETTI_QC_NAME','2q-pyqvm')
    p=Program()
    ro=p.declare('ro','BIT',2)
    p += H(0)
    p += CNOT(0,1)
    p += RZ(theta,1)
    p += CNOT(0,1)
    p += H(0)
    p += MEASURE(0,ro[0])
    p += MEASURE(1,ro[1])
    p.wrap_in_numshots_loop(shots)
    qc=get_qc(name)
    exe=qc.compile(p)
    result=qc.run(exe).get_register_map()['ro']
    key=result[:,0]+2*result[:,1]
    counts=np.bincount(key,minlength=4).tolist()
    print(json.dumps({'backend':name,'shots':shots,'counts_lsb':counts,'theta':theta},indent=2))
    # On hardware capture QPU identifier, calibration timestamp, compiler
    # version, shot budget, job ID, measurement mitigation and output hash.

if __name__=='__main__':main()
