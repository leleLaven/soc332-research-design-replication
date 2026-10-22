# SOC332 Research Design: reproducible PSID feasibility exhibits
This repository rebuilds aggregate sample-flow and measurement-availability tables for the Research Design. Counts are unweighted and are not estimates of H1–H4.
## One-click reproduction
Open **Actions → Reproduce feasibility exhibits → Run workflow**. GitHub Actions runs validation tests, rebuilds both CSVs, verifies the outputs, and uploads them as an artifact.
The workflow uses only aggregate JSON in `aggregate_inputs/`; it never downloads or reads person-level PSID records. Outputs: `exhibits/sample_flow.csv` and `exhibits/measurement_availability.csv`.
## Rebuild aggregate inputs from PSID public-use archives
Obtain `fam2001er.zip`, `fam2023er.zip`, `pid23.zip`, `wlth2001.zip`, and `ind2023er.zip` separately from PSID and keep them outside this repository. Run `scripts/audit_psid.py` and `scripts/h3_h4_counts.py` with the archive root and individual archive paths, then run `python3 reproduce.py` and `python3 -m unittest discover -s tests -v`.
Audit scripts write aggregate counts only. Their outputs are Git-ignored; person-level records are processed in memory and never written to this repository.
## Scope
The feasibility cohort contains 1,573 people ages 10–17 in 2001 who met 2023 household-role restrictions, from 1,173 distinct 2001 families. Education is classifiable for 1,483; 90 remain unclassified. These counts establish no hypothesized association. Weighting, within-family dependence, final model samples, and missing-data decisions remain separate decisions.
Public outputs contain aggregates and annotated code, never personal identifiers or raw PSID records. Update the workflow and tests if submitted exhibits change.
