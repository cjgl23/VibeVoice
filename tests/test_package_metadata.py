from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_pyproject_and_package_layout(self):
        with (ROOT / "pyproject.toml").open("rb") as handle:
            metadata = tomllib.load(handle)
        self.assertEqual(metadata["project"]["name"], "vibevoice")
        self.assertTrue(metadata["project"]["dependencies"])
        self.assertTrue((ROOT / "vibevoice" / "modular").is_dir())
        self.assertTrue((ROOT / "demo" / "gradio_demo.py").is_file())
        self.assertTrue((ROOT / "demo" / "vibevoice_asr_gradio_demo.py").is_file())


if __name__ == "__main__":
    unittest.main()
