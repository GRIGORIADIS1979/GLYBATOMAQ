# IBM Qiskit and Rigetti pyQuil software portability

The default core workflow is **CPU-only**. The optional `code/ibm_qiskit_bridge.py` uses a two-qubit four-vertex *illustrative* Laplacian evolution and statevector verification. The optional `code/rigetti_pyquil_bridge.py` uses a portable two-qubit *gate smoke test* on a local pyQVM; it is not the same exact full molecular-graph Hamiltonian. Neither file is evidence of QPU execution or a quantum advantage.

For a full 92–101-heavy-atom source graph, a project must specify:

1. A lossless (or explicitly approximated) encoding of an n-vertex Hermitian graph generator into at least `ceil(log2(n))` qubits, including padding of nonphysical basis states.
2. A Hamiltonian block encoding/Pauli expansion, initial-state preparation, time-grid and evolution synthesis error controls, and logical-to-physical qubit mapping.
3. A maximum circuit-depth/noise budget, a chosen backend and provider authorization, compiler package versions, gate-set calibration and measurement mitigation.
4. Every shot count, job ID, job timestamp and intermediate circuit hash.
5. The same initial states and observables evaluated by exact classical diagonalization and under the same noise model for hardware assessment.

Local software examples:
```
python -m pip install -r requirements-ibm-optional.txt
python code/ibm_qiskit_bridge.py
python -m pip install -r requirements-rigetti-optional.txt
python code/rigetti_pyquil_bridge.py
```
Do not publish provider credentials, QCS tokens or IBM API keys. Use secret-scoped CI integrations only after user authorization.

- IBM Qiskit: https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.PauliEvolutionGate
- Rigetti pyQuil: https://pyquil-docs.rigetti.com/en/stable/getting_started.html
