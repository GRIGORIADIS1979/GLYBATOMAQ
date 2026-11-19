"""Optional IBM Qiskit demonstrator: a 4-vertex CTQW subgraph.

This 2-qubit illustrative circuit is a portability test, not an execution of a
92--101-atom source-graph Hamiltonian on quantum hardware.

Requires: qiskit>=1, scipy, numpy. API based on PauliEvolutionGate.
"""
import json
import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from qiskit.synthesis import LieTrotter


def four_vertex_path_laplacian():
    adjacency = np.array([[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],dtype=float)
    return np.diag(adjacency.sum(axis=1))-adjacency


def main():
    H = four_vertex_path_laplacian()/3.5
    t=0.6
    op = SparsePauliOp.from_operator(Operator(H))
    evo = PauliEvolutionGate(op, time=t, synthesis=LieTrotter(reps=80))
    circuit = QuantumCircuit(2)
    circuit.append(evo,[0,1])
    psi = Statevector.from_instruction(circuit).data
    reference = expm(-1j*H*t)[:,0]
    error = float(np.linalg.norm(psi-reference))
    print(json.dumps({'backend':'local Qiskit Statevector','n_qubits':2,'time':t,'product_formula_repetitions':80,'state_error_vs_exact':error,'probability_sum':float(np.vdot(psi,psi).real)},indent=2))
    print(circuit.decompose(reps=2).draw(output='text'))
    assert abs(np.vdot(psi,psi)-1)<1e-10
    assert error<0.05
    # For authorized IBM Quantum device execution, transpile to the current
    # target basis, map the physical qubits, specify shots, record job ID,
    # calibration snapshot and compiler version; see README.

if __name__=='__main__':main()
