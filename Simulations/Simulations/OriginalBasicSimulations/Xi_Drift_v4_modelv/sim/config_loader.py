import json
import yaml
from typing import Dict

CONFIG = {
    "steps": 100,
    "dt": 0.01,
    "gamma": 0.05,
    "m": 1.0,
    "output_dir": "model5_autosim_gamma0.05_m1.0"
}

def load_config(path: str) -> Dict:
    if path.endswith(".json"):
        with open(path, "r") as f:
            return json.load(f)
    elif path.endswith(".yml") or path.endswith(".yaml"):
        with open(path, "r") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported config format. Use .json or .yml")
