import unittest
import json
import os

class TestDefaultConfig(unittest.TestCase):
    def setUp(self):
        """Load the configuration file before running tests."""
        config_path = os.path.join("config", "default_config.json")
        with open(config_path, "r") as file:
            self.config = json.load(file)

    def test_config_keys_exist(self):
        """Ensure all top-level keys are present in the configuration."""
        required_keys = {"project_name", "version", "debug", "logging", "services", "hardware", "deployment"}
        self.assertTrue(required_keys.issubset(self.config.keys()), "Missing required top-level keys in default_config.json")

    def test_logging_keys_exist(self):
        """Ensure the logging configuration contains required keys."""
        logging_config = self.config.get("logging", {})
        required_keys = {"log_level", "log_file"}
        self.assertTrue(required_keys.issubset(logging_config.keys()), "Missing keys in logging configuration")

    def test_deployment_keys_exist(self):
        """Ensure the deployment configuration contains required keys."""
        deployment_config = self.config.get("deployment", {})
        required_keys = {"update_interval", "repository_url", "auto_restart_on_update"}
        self.assertTrue(required_keys.issubset(deployment_config.keys()), "Missing keys in deployment configuration")

    def test_project_name(self):
        """Check if project_name is correctly set."""
        self.assertEqual(self.config["project_name"], "atlaspi", "Project name should be 'atlaspi'")

    def test_version_format(self):
        """Ensure the version follows the format 'x.y.z'."""
        import re
        version = self.config["version"]
        self.assertTrue(re.match(r"^\d+\.\d+\.\d+$", version), f"Invalid version format: {version}")


if __name__ == "__main__":
    unittest.main()
