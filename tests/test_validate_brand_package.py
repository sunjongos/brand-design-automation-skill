import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_brand_package.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def example():
    return json.loads((ROOT / "assets" / "brand-package.example.json").read_text())


class BrandPackageTests(unittest.TestCase):
    def test_example_is_valid(self):
        self.assertEqual(MODULE.validate(example()), [])

    def test_rejects_unsafe_unapproved_release(self):
        data = copy.deepcopy(example())
        data["governance"]["privacy_checked"] = False
        self.assertIn("governance.privacy_checked: must be true before release", MODULE.validate(data))

    def test_rejects_incomplete_visual_system(self):
        data = copy.deepcopy(example())
        data["visual"]["colors"]["accent"] = "gold"
        data["visual"]["typography"]["minimum_body_px"] = 9
        errors = MODULE.validate(data)
        self.assertIn("visual.colors.accent: expected #RRGGBB", errors)
        self.assertIn("visual.typography.minimum_body_px: must be >= 12", errors)

    def test_rejects_duplicate_channels(self):
        data = copy.deepcopy(example())
        data["channels"].append(copy.deepcopy(data["channels"][0]))
        self.assertIn("channels: duplicate channel names", MODULE.validate(data))

    def test_rejects_low_text_contrast(self):
        data = copy.deepcopy(example())
        data["visual"]["colors"]["text"] = "#AAAAAA"
        data["visual"]["colors"]["background"] = "#FFFFFF"
        self.assertTrue(any("below 4.5:1" in error for error in MODULE.validate(data)))

    def test_rejects_proof_as_plain_text(self):
        data = copy.deepcopy(example())
        data["strategy"]["proof"] = "Trust us"
        self.assertIn("strategy.proof: expected list", MODULE.validate(data))

    def test_rejects_wrong_top_level_types_without_crashing(self):
        data = copy.deepcopy(example())
        data["strategy"] = []
        self.assertIn("strategy: required", MODULE.validate(data))


if __name__ == "__main__":
    unittest.main()
