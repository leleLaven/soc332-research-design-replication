#!/usr/bin/env python3
"""Rebuild aggregate feasibility exhibits without person-level records."""

import csv
import json
from pathlib import Path

# Resolve paths from this file so the workflow works from any working directory.
ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "aggregate_inputs"
OUTPUT = ROOT / "exhibits"


def load(path):
    """Read one committed, privacy-safe aggregate JSON input."""
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def build(audit, groups):
    """Validate cohort totals, then write both aggregate CSV exhibits."""
    flow = audit["flows"]["10-17"]
    cohort = audit["candidate_10_17"]
    n = flow["no_known_parent_same_fu_followup"]

    # Stop before writing outputs if the input files disagree on the cohort.
    checks = [
        (n == groups["cohort_n"], "Cohort counts do not agree"),
        (
            groups["current_partnered_2023"] + groups["no_recorded_partner_2023"] == n,
            "Partner counts do not sum to cohort",
        ),
        (
            groups["one_identified_coresident_parent_2001"]
            + groups["two_identified_coresident_parents_2001"]
            == n,
            "Parent counts do not sum to cohort",
        ),
        (
            cohort["wealth_negative"] + cohort["wealth_zero"] + cohort["wealth_positive"] == n,
            "Wealth counts do not sum to cohort",
        ),
        (
            cohort["ba_classified"] + cohort["ba_unknown"] == n,
            "Education counts do not sum to cohort",
        ),
    ]
    for valid, message in checks:
        if not valid:
            raise ValueError(message)

    OUTPUT.mkdir(exist_ok=True)

    def write(name, header, rows):
        """Write stable UTF-8 CSV files for byte-for-byte CI comparison."""
        with (OUTPUT / name).open("w", encoding="utf-8", newline="") as target:
            writer = csv.writer(target, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(rows)

    # Sample-flow rows are unweighted selection counts, not hypothesis estimates.
    write(
        "sample_flow.csv",
        ["selection_step", "n"],
        [
            ("Resident in 2001, age 10-17", flow["resident_baseline"]),
            ("Linked to identified parent", flow["linked_resident_parent_baseline"]),
            ("Observed in 2023", flow["resident_followup"]),
            (
                "Reference person, spouse, or partner in 2023",
                flow["reference_spouse_partner_followup"],
            ),
            ("Separate from identified parent in 2023", n),
            ("Distinct original 2001 families", flow["unique_2001_families"]),
        ],
    )

    # Availability rows show classifiable measures within this feasibility cohort.
    write(
        "measurement_availability.csv",
        ["measure", "n"],
        [
            ("BA status classifiable", cohort["ba_classified"]),
            ("BA status unclassified", cohort["ba_unknown"]),
            ("Negative 2023 household net worth", cohort["wealth_negative"]),
            ("Zero 2023 household net worth", cohort["wealth_zero"]),
            ("Current spouse or permanent cohabiting pair", groups["current_partnered_2023"]),
            ("No such pair recorded", groups["no_recorded_partner_2023"]),
            (
                "One identified co-resident parent in 2001",
                groups["one_identified_coresident_parent_2001"],
            ),
            (
                "Two identified co-resident parents in 2001",
                groups["two_identified_coresident_parents_2001"],
            ),
        ],
    )


def main():
    """Load aggregate inputs and regenerate the committed proposal exhibits."""
    audit = load(INPUT / "feasibility_audit.json")
    groups = load(INPUT / "h3_h4_counts.json")
    build(audit, groups)
    print("Rebuilt aggregate exhibits")


if __name__ == "__main__":
    main()
