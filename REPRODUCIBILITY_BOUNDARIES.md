# Methods and evidence provenance

## Verified in the provided CPU package
- Four graphs constructed from source MOL2 heavy-atom connectivity; 92/94/91/101 heavy atoms in source mapping order cons2/cons1/cons3/cons4.
- Real symmetric graph Laplacians and unitary CTQW evolution by spectral decomposition.
- Classical heat-diffusion reference and symmetric nonlocal teleport-edge augmentation (alpha 0.18).
- Finite-time normalization checks and six frozen-weight ablation variants.
- Seeded fixed-four-candidate MBHA *algorithm demonstration* and a purely numerical portable two-qubit gate calculation.

## Source-reported observations, not recalculated original simulations
- 3Q2R DockThor values transcribed from manuscript tables; no receptor/ligand projects, docked poses or scoring logs regenerated here.
- Other source docking tables, including 2GLI receptor and mixed-receptor source screenshots.
- DFT-proxy and QMC-style proxy support values; no first-principles calculations were executed within the package.

## Prospective / optional operations
- Full-resolution IBM Qiskit Hamiltonian circuit compilation and execution.
- Physical Rigetti QPU execution, calibrated shots and backend snapshots.
- New receptor-resolved docking, MD, quantum chemistry or biological evaluation.
- Independent external activity-label benchmark, statistical hypothesis tests of drug-discovery efficacy, and geometry–score correlation.

**Numerical terminology:** Continuous-time quantum walk (CTQW) is a unitary computational model of graph transport. The reported symmetric teleport coupling adds graph edges and preserves a Hermitian Hamiltonian. The original row-stochastic source transition table is a separate classical object and **not** itself a CTQW Hamiltonian. Fubini–Study geometry applies to normalized pure states, not arbitrary unnormalized descriptor vectors.

## Additional prerequisites for independent drug-discovery assessment
Obtain validated atom-mapped canonical/isomeric molecular structures, precise GLIPR1 receptor structures with preparation details, binding-site volumes and box coordinates, ligands with protonation states and conformer identities, original complete docking workflows and logs, prospective target labels, external nonredundant molecular benchmarks, and pre-specified matching of all evaluation budgets and metrics.
