from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml

@dataclass
class AppConfig:
    keywords: Dict[str, Any]
    job_sources: List[Dict[str, Any]]
    google_sheets: Dict[str, str]
    resume: Dict[str, str]
    scoring: Dict[str, Any]

def load_config(path: str = "config.yaml") -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path.resolve()}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return AppConfig(
        keywords=data.get("keywords", {}),
        job_sources=data.get("job_sources", []),  # we may use this later
        google_sheets=data.get("google_sheets", {}),
        resume=data.get("resume", {}),
        scoring=data.get("scoring", {}),
    )
