"""Pruebas de estructura DevOps; NO sustituyen las pruebas contables de QA."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class DevOpsStructureTests(unittest.TestCase):
    def test_documented_stack_directories_exist(self):
        for name in ("backend", "frontend", "database", "tests", "docs"):
            with self.subTest(directory=name):
                self.assertTrue((ROOT / name).is_dir())

    def test_required_infrastructure_files_exist(self):
        for name in ("compose.yaml", ".env.example", ".gitignore",
                     ".github/workflows/ci.yml", "docs/guia-devops.md"):
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).is_file())

    def test_example_environment_contains_expected_variables(self):
        content = (ROOT / ".env.example").read_text(encoding="utf-8")
        for key in ("POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_PORT"):
            with self.subTest(variable=key):
                self.assertRegex(content, rf"(?m)^{key}=")

    def test_compose_has_healthcheck_and_local_port_binding(self):
        content = (ROOT / "compose.yaml").read_text(encoding="utf-8")
        self.assertIn("healthcheck:", content)
        self.assertIn("127.0.0.1:", content)
        self.assertIn("postgres_data:", content)

    def test_local_env_is_ignored(self):
        content = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("\n.env\n", "\n" + content)


if __name__ == "__main__":
    unittest.main()
