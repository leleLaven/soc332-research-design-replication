import csv
import tempfile
import unittest
from pathlib import Path

import reproduce

class ReproductionTests(unittest.TestCase):
    def test_builds_consistent_aggregate_exhibits(self):
        audit = reproduce.load_json(reproduce.INPUT / "feasibility_audit.json")
        groups = reproduce.load_json(reproduce.INPUT / "h3_h4_counts.json")
        original = reproduce.OUTPUT
        with tempfile.TemporaryDirectory() as directory:
            reproduce.OUTPUT = Path(directory)
            try:
                reproduce.build_exhibits(audit, groups)
                with (Path(directory) / "sample_flow.csv").open(encoding="utf-8", newline="") as f:
                    rows = list(csv.reader(f))
                self.assertEqual(rows[-2], ["Separate from identified parent in 2023", "1573"])
                self.assertEqual(rows[-1], ["Distinct original 2001 families", "1173"])
            finally:
                reproduce.OUTPUT = original

    def test_rejects_mismatched_cohort_counts(self):
        audit = reproduce.load_json(reproduce.INPUT / "feasibility_audit.json")
        groups = reproduce.load_json(reproduce.INPUT / "h3_h4_counts.json")
        groups["cohort_n"] += 1
        with self.assertRaisesRegex(ValueError, "cohort counts do not agree"):
            reproduce.build_exhibits(audit, groups)

if __name__ == "__main__":
    unittest.main()
