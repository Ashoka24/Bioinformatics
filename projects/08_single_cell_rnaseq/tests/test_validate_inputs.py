import tempfile
import unittest
from pathlib import Path

from scripts.validate_inputs import validate


class ValidateInputTests(unittest.TestCase):
    def test_missing_directory(self):
        path = Path(tempfile.gettempdir()) / "sc_rnaseq_missing_fixture_713582"
        self.assertTrue(any("does not exist" in item for item in validate(path)))

    def test_valid_matrix_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "matrix.mtx").write_text("%%MatrixMarket matrix coordinate integer general\n", encoding="utf-8")
            (root / "barcodes.tsv").write_text("cell1\n", encoding="utf-8")
            (root / "features.tsv").write_text("gene1\tGENE1\tGene Expression\n", encoding="utf-8")
            self.assertEqual(validate(root), [])

    def test_missing_feature_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "matrix.mtx.gz").write_bytes(b"")
            (root / "barcodes.tsv.gz").write_bytes(b"")
            self.assertTrue(any("features/genes" in item for item in validate(root)))


if __name__ == "__main__":
    unittest.main()
