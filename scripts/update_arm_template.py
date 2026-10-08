#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path

def load_json_file(file_path):
    if not Path(file_path).is_file():
        print(f"File not found: {file_path}")
        sys.exit(1)
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def update_parameters(template_file, config_file):
    template = load_json_file(template_file)
    config = load_json_file(config_file)

    parameters = template.get("parameters", {})
    unknown_keys = sorted(set(config) - set(parameters))
	if unknown_keys:
        print("Config keys not found in exported ARM parameters:")
        for key in unknown_keys:
            print(f" - {key}")
        sys.exit(1)
    missing_keys = []

    for key in parameters.keys():
        if key in config:
            value = config[key]
            if isinstance(value, dict) and set(value) == {"env"}:
                value = os.environ.get(value["env"])
                if not value:
                    missing_keys.append(key)
                    continue
            parameters[key]["value"] = value
        else:
            missing_keys.append(key)

    if missing_keys:
        print("Missing values for the following keys in the config file or environment:")
        for k in missing_keys:
            print(f" - {k}")
        sys.exit(1)

    template["parameters"] = parameters
    save_json_file(template_file, template)

    print("ARM template parameters updated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_arm_template.py <template_file> <config_file>")
        sys.exit(1)

    template_path = sys.argv[1]
    config_path = sys.argv[2]

    update_parameters(template_path, config_path)
