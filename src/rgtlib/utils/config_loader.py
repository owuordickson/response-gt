# SPDX-License-Identifier: GNU GPL v3

"""
Loads default configurations from 'configs.ini' file
"""

import os
import configparser
from typing import Union
from sgtlib.modules import verify_path


def read_config_file(config_path):
    """Read the contents of the 'configs.ini' file"""
    config = configparser.ConfigParser()
    success, result = verify_path(config_path)
    if success:
        config_file = result
    else:
        # Using the default config file. Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = 'configs.ini'
        config_file = os.path.join(script_dir, config_path)
    # Load the default configuration from the file
    try:
        config.read(config_file)
        return config
    except configparser.Error:
        # print(f"Unable to read the configs from {config_file}.")
        return None


def load_rgt_configs(cfg_path: str = ""):
    """ResponseGT computation configuration loader."""

    options_rgt: dict[str, dict[str, Union[int, float]]]  = {
        "response_type": {"id": "response_type", "type": "ac-metric", "text": "Response Type", "value": 0},
        "potential_frequency": {"id": "potential_frequency", "type": "dc-metric", "text": "", "value": 0.000000000001},
        "potential_fraction": {"id": "potential_fraction", "type": "dc-metric", "text": "", "value": 0.05},
        "potential_magnitude": {"id": "potential_magnitude", "type": "dc-metric", "text": "", "value": 100.0},
        "resistivity": {"id": "resistivity", "type": "dc-metric", "text": "", "value": 1.0},
        "capacitance": {"id": "capacitance", "type": "dc-metric", "text": "", "value": 0.000000000001},
        "inductance": {"id": "inductance", "type": "dc-metric", "text": "", "value": 0.00000000000000000001},
        "leak_resistivity": {"id": "leak_resistivity", "type": "dc-metric", "text": "", "value": 1000000000}
    }

    # Load configuration from the file
    config = read_config_file(cfg_path)
    if config is None:
        return options_rgt

    try:
        options_rgt["response_type"]["value"] = int(config.get('ac-metric', 'response_type'))
        options_rgt["potential_frequency"]["value"] = float(config.get('dc-metric', 'potential_frequency'))
        options_rgt["potential_fraction"]["value"] = float(config.get('dc-metric', 'potential_fraction'))
        options_rgt["potential_magnitude"]["value"] = float(config.get('dc-metric', 'potential_magnitude'))
        options_rgt["resistivity"]["value"] = float(config.get('dc-metric', 'resistivity'))
        options_rgt["capacitance"]["value"] = float(config.get('dc-metric', 'capacitance'))
        options_rgt["inductance"]["value"] = float(config.get('dc-metric', 'inductance'))
        options_rgt["leak_resistivity"]["value"] = float(config.get('dc-metric', 'leak_resistivity'))

        return options_rgt
    except configparser.NoSectionError:
        return options_rgt

