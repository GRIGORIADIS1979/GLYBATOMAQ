# Data dictionary and original source classes

| Source | Important columns or fields | Unit | Evidence role |
|---|---|---|---|
| `source_inputs/*.mol2` | 3D coordinates, declared atom symbols, source bonds | Å and bond labels | Source mathematical graph; chemistry audit needed |
| `source_inputs/*.pdb` | Source coordinates and atom types | Å | Coordinate crosswalk only |
| `computed/candidate_graph_transport.csv` | `candidate`, `n_heavy_atoms`, `ctqw_return_t3`, `heat_return_t3`, `teleport_return_t3`, `max_probability_error` | dimensionless probabilities | CPU-computed graph quantities; source heavy-atom bonds |
| `computed/internal_score_ablations.csv` | `ablation`, `candidate`, `score`, `rank` | dimensionless source ledger | Deterministic frozen-weight E2 transformations |
| `computed/mbha_fixed_library_trace.csv` | `generation`, `elite_id`, `elite_score`, `unique_ids` | score or count | Seeded four-entry search illustration |
| `source_table_audit/data/source_dockthor_3Q2R.csv` | `source_label`, `dockthor_affinity`, `receptor_pdb`, source verification flags | docking program score | Transcribed source GLIPR1 3Q2R table; no source project rerun |
| `source_table_audit/data/source_vina_mixed_receptors_QUARANTINED.csv` | receptor labels, source scores | scoring-function kcal/mol label | Target-mixed source record; excluded from GLIPR1 claims |
| `data/archived_docking_2GLI/` | iGEMDOCK energy and residue contributions | program-specific units | Historical GLI–DNA comparison only |
| `data/rdkit_generated_fda_conformers/*.sdf` | locally generated RDKit ETKDG coordinates | Å | Derived geometry, *not* original PubChem 3D downloads |
| `data/investigator_assigned_iupac_names.json` | user-supplied systematic names | strings | Investigator naming records, require independent structure reconciliation |

The mathematical source-graph adjacency ignores bond order and formal charge: every declared heavy-atom bond contributes weight 1. Chemical connectivity used for source-graph transport has not been transformed into a validated pharmacological target predictor. The source E2 fusion weights are frozen, and leave-one-component-out scores do **not** renormalize remaining weights.
