#!/usr/bin/env python3
"""Rebuild aggregate feasibility exhibits without person-level records."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
INPUT=ROOT/"aggregate_inputs"
OUTPUT=ROOT/"exhibits"
def load(path):
    with path.open(encoding="utf-8") as f: return json.load(f)
def build(audit, groups):
    flow=audit["flows"]["10-17"]; cohort=audit["candidate_10_17"]; n=flow["no_known_parent_same_fu_followup"]
    if n != groups["cohort_n"]: raise ValueError("Cohort counts do not agree")
    if groups["current_partnered_2023"]+groups["no_recorded_partner_2023"] != n: raise ValueError("Partner counts do not sum to cohort")
    if groups["one_identified_coresident_parent_2001"]+groups["two_identified_coresident_parents_2001"] != n: raise ValueError("Parent counts do not sum to cohort")
    if cohort["wealth_negative"]+cohort["wealth_zero"]+cohort["wealth_positive"] != n: raise ValueError("Wealth counts do not sum to cohort")
    if cohort["ba_classified"]+cohort["ba_unknown"] != n: raise ValueError("Education counts do not sum to cohort")
    OUTPUT.mkdir(exist_ok=True)
    def write(name,header,rows):
        with (OUTPUT/name).open("w",encoding="utf-8",newline="") as f: w=csv.writer(f,lineterminator="\n"); w.writerow(header); w.writerows(rows)
    write("sample_flow.csv",["selection_step","n"],[("Resident in 2001, age 10-17",flow["resident_baseline"]),("Linked to identified parent",flow["linked_resident_parent_baseline"]),("Observed in 2023",flow["resident_followup"]),("Reference person, spouse, or partner in 2023",flow["reference_spouse_partner_followup"]),("Separate from identified parent in 2023",n),("Distinct original 2001 families",flow["unique_2001_families"])])
    write("measurement_availability.csv",["measure","n"],[("BA status classifiable",cohort["ba_classified"]),("BA status unclassified",cohort["ba_unknown"]),("Negative 2023 household net worth",cohort["wealth_negative"]),("Zero 2023 household net worth",cohort["wealth_zero"]),("Current spouse or permanent cohabiting pair",groups["current_partnered_2023"]),("No such pair recorded",groups["no_recorded_partner_2023"]),("One identified co-resident parent in 2001",groups["one_identified_coresident_parent_2001"]),("Two identified co-resident parents in 2001",groups["two_identified_coresident_parents_2001"])])
def main():
    build(load(INPUT/"feasibility_audit.json"),load(INPUT/"h3_h4_counts.json"))
    print("Rebuilt aggregate exhibits")
if __name__=="__main__": main()
