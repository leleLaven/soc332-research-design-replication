import csv
import json
import tempfile
import unittest
from pathlib import Path

import reproduce

class ReproductionTests(unittest.TestCase):
    def load_inputs(self):
        with (reproduce.INPUT / "feasibility_audit.json").open(encoding="utf-8") as f:
            audit = json.load(f)
        with (reproduce.INPUT / "h3_h4_counts.json").open(encoding="utf-8") as f:
            groups = json.load(f)
        return audit, groups

    def test_builds_consistent_aggregate_exhibits(self):
        audit, groups = self.load_inputs()
        original = reproduce.OUTPUT
        with tempfile.TemporaryDirectory() as directory:
            reproduce.OUTPUT = Path(directory)
            try:
                reproduce.build(audit, groups)
                with (Path(directory) / "sample_flow.csv").open(encoding="utf-8", newline="") as f:
                    rows = list(csv.reader(f))
                self.assertEqual(rows[-2], ["Separate from identified parent in 2023", "1573"])
                self.assertEqual(rows[-1], ["Distinct original 2001 families", "1173"])
            finally:
                reproduce.OUTPUT = original

    def test_rejects_mismatched_cohort_counts(self):
        audit, groups = self.load_inputs()
        groups["cohort_n"] += 1
        with self.assertRaisesRegex(ValueError, "Cohort counts do not agree"):
            reproduce.build(audit, groups)

if __name__ == "__main__":
    unittest.main()
