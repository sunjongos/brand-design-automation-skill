import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "pipeline_state.py"
STAGES = ["planner", "brand_anchor", "landing", "figma_design", "canva", "social", "slides", "video", "qa", "delivery"]


class PipelineStateTests(unittest.TestCase):
    def test_incomplete_then_complete(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "run.json"
            subprocess.run(["python3", SCRIPT, "init", receipt, "--brand", "Test"], check=True, capture_output=True)
            first = subprocess.run(["python3", SCRIPT, "check", receipt], capture_output=True)
            self.assertNotEqual(first.returncode, 0)
            for stage in STAGES:
                subprocess.run(["python3", SCRIPT, "set", receipt, stage, "passed", "--artifact", stage], check=True, capture_output=True)
            final = subprocess.run(["python3", SCRIPT, "check", receipt], capture_output=True)
            self.assertEqual(final.returncode, 0)
            self.assertEqual(json.loads(receipt.read_text())["stages"]["video"]["status"], "passed")

    def test_blocked_is_not_full_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / "run.json"
            subprocess.run(["python3", SCRIPT, "init", receipt, "--brand", "Test"], check=True, capture_output=True)
            subprocess.run(["python3", SCRIPT, "set", receipt, "video", "blocked"], check=True, capture_output=True)
            result = subprocess.run(["python3", SCRIPT, "check", receipt], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
