# SOC332 Research Design: reproducible PSID feasibility exhibits

This repository rebuilds the aggregate sample-flow and measurement-availability tables used to document feasibility for the Research Design. The counts are unweighted and are not estimates of H1–H4.

## One-click reproduction

On GitHub, open **Actions → Reproduce feasibility exhibits → Run workflow**. The workflow runs the included tests, rebuilds both CSVs from the aggregate JSON files in `aggregate_inputs/`, verifies that the outputs match the committed files, and uploads them as the `research-design-feasibility-exhibits` artifact.

The workflow does not download or read person-level PSID records. The reproducible outputs are:

- `exhibits/sample_flow.csv`
- `exhibits/measurement_availability.csv`

The source-data audit scripts used to create the aggregate JSON inputs are not included in this public repository. The person-level PSID archives are also not included; obtain them separately from PSID and follow the applicable data-use terms.

## Scope and interpretation

The current feasibility cohort contains 1,573 people who were ages 10–17 in 2001 and met the stated 2023 household-role restrictions. They come from 1,173 distinct 2001 families. Education status is classifiable for 1,483; 90 remain unclassified. These counts do not establish any hypothesized association. Weighting, within-family dependence, final model samples, and missing-data decisions remain separate analysis decisions.

The aggregate tables summarize counts also described in the Research Design. If a submitted data exhibit changes, update the aggregate inputs, reproduction script, tests, and workflow so the submitted output can be regenerated identically.
