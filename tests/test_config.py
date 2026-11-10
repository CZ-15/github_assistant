import pytest
from config.integrate import (
    load_default_config,
    merge,
    render_user_config,
    specific_merge,
    user_text_load,
)
from pathlib import Path


def test_load_default_config():
    config = load_default_config()
    assert set(config) == {
        "ignored",
        "agent",
        "model"
    }

    assert set(config["ignored"]) == {
        "directories",
        "files",
        "suffixes"
    }

    assert set(config["agent"]) == {
        "cost_limit",
        "step_limit",
        "max_retries",
        "timeout",
        "max_consecutive_errors"
    }

    assert set(config["model"]) == {
        "name",
        "provider",
        "temperature"
    }


def test_render_user_config(tmp_path: Path):
    path = tmp_path / "user.yaml"

    path.write_text(
        """
agent:
  timeout: {{ user_timeout }}
model:
  name: {{ model_name }}
""".strip(),
        encoding="utf-8",
    )

    path = str(path)
    result = render_user_config(path, template_values = {
        "user_timeout": 12,
        "model_name": "deepseek"
    })

    result = user_text_load(result)

    assert result == {
        "agent": {
            "timeout": 12,
        },
        "model": {
            "name": "deepseek",
        },
    }


