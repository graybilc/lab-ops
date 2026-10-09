from pathlib import Path
import pytest
import yaml
from lab_ops.config import LabOpsConfig

def test_config_tilde_expansion(tmp_path):
    # 1. Create a dummy repository directory on disk
    dummy_repo = tmp_path / "dummy_repo"
    dummy_repo.mkdir()

    # 2. Write a temporary YAML config using the dummy path
    config_dict = {
        "global": {
            "output_dir": str(tmp_path / "reports"),
            "default_llm_model": "gpt-4o-mini"
        },
        "repositories": {
            "test_repo": {
                "name": "Test Repository",
                "path": str(dummy_repo),
                "type": "sandbox"
            }
        }
    }
    
    yaml_file = tmp_path / "test_config.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(config_dict, f)

    # 3. Load configuration and assert validation passes
    config = LabOpsConfig.load_from_yaml(yaml_file)
    assert "test_repo" in config.repositories
    assert config.repositories["test_repo"].path == dummy_repo.resolve()