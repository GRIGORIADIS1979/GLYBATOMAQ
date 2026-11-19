"""Pure NumPy exact reference for the IBM/Rigetti 2-qubit gate-sequence demo.

Qubit 0 is the least-significant bit; this module requires only NumPy.
"""
import numpy as np

def main():
    I=np.eye(2,dtype=complex)
    H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)
    theta=.6
    RZ=np.diag([np.exp(-1j*theta/2),np.exp(1j*theta/2)])
    CNOT=np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]],dtype=complex) # control q0, target q1
    seq=np.kron(I,H)@CNOT@np.kron(RZ,I)@CNOT@np.kron(I,H)
    vec=seq[:,0]
    assert np.allclose(seq.conj().T@seq,np.eye(4))
    assert np.isclose(sum(abs(vec)**2),1)
    print('Portable 2-qubit test: PASS; basis probabilities (|q1 q0>):',np.round(abs(vec)**2,8).tolist())

if __name__=='__main__':main()
