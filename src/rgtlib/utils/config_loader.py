# SPDX-License-Identifier: GNU GPL v3

"""
Loads default configurations from 'configs.ini' file
"""

import os
import math
import configparser
import numpy as np
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
        #print(f"Configs loaded successfully from: {config_file}.")
        return config
    except configparser.Error:
        #print(f"Unable to read the configs from {config_file}.")
        return None


def initialize_list_params():
    """Initialize the list of parameters for the ResponseGT computation."""

    response_file_options: dict[str, dict[str, str | int | None | np.ndarray]] = {
        "resistivity_list": {"id": "resistivity_list", "text": "Resistivity List", "visible": 1, "value": 0, "data": None},
        "inductance_list": {"id": "inductance_list", "text": "Inductance List", "visible": 1, "value": 0, "data": None},
        "capacitance_list": {"id": "capacitance_list", "text": "Capacitance List", "visible": 1, "value": 0, "data": None},
        "leak_resistivity_list": {"id": "leak_resistivity_list", "text": "Leak Resistivity List", "visible": 1, "value": 0, "data": None}
    }
    return response_file_options


def load_rgt_configs(cfg_path: str = ""):
    """ResponseGT computation configuration loader."""

    def number_to_scientific_parts(value: float):
        """
        Convert a number into (coefficient, multiplier) such that:
            value = coefficient * 10**multiplier

        Example:
            0.005 → (5, -3)
            123 → (1.23, 2)

        Special rule:
            If the multiplier is -1, 1, or 2 → force it to 0
        """

        if value == 0:
            return 0, 0

        # Determine scientific exponent
        multiplier = int(math.floor(math.log10(abs(value))))
        coefficient = value / (10 ** multiplier)

        # Ensure coefficient is in [1, 10)
        if abs(coefficient) < 1:
            coefficient *= 10
            multiplier -= 1

        # Force multiplier -1, 1, or 2 back to 0
        if multiplier in {-1, 1, 2}:
            coefficient = value  # collapse scaling into coefficient
            multiplier = 0
        return coefficient, multiplier


    # add the imposed direction (selected)
    options_rgt: dict[str, dict[str, Union[int, float]]]  = {
        "response_type": {"id": "response_type", "type": "ac-param", "text": "Response Type", "visible": 1, "value": 0},
        "potential_frequency": {"id": "potential_frequency", "type": "dc-param", "text": "Potential Frequency", "visible": 1, "value": 1, "multiplier": -6, "minValue": 0, "maxValue": 1000},
        "potential_fraction": {"id": "potential_fraction", "type": "dc-param", "text": "Potential Fraction", "visible": 1, "value": 5, "multiplier": -2, "minValue": 0, "maxValue": 1000},
        "potential_magnitude": {"id": "potential_magnitude", "type": "dc-param", "text": "Potential Magnitude", "visible": 1, "value": 100.0, "multiplier": 0, "minValue": 0, "maxValue": 1000},
        "resistivity": {"id": "resistivity", "type": "dc-param", "text": "Resistivity", "visible": 1, "value": 1.0, "multiplier": 0, "minValue": 0, "maxValue": 1000},
        "capacitance": {"id": "capacitance", "type": "dc-param", "text": "Capacitance", "visible": 1, "value": 1, "multiplier": -6, "minValue": 0, "maxValue": 1000},
        "inductance": {"id": "inductance", "type": "dc-param", "text": "Inductance", "visible": 1, "value": 1, "multiplier": -9, "minValue": 0, "maxValue": 1000},
        "leak_resistivity": {"id": "leak_resistivity", "type": "dc-param", "text": "Leak Resistivity", "visible": 1, "value": 1, "multiplier": 6, "minValue": 0, "maxValue": 1000}
    }

    # Load configuration from the file
    config = read_config_file(cfg_path)
    if config is None:
        return options_rgt

    try:
        options_rgt["response_type"]["value"] = int(config.get('ac-response', 'response_type'))
        freq_val = float(config.get('dc-response', 'potential_frequency'))
        frac_val = float(config.get('dc-response', 'potential_fraction'))
        mag_val = float(config.get('dc-response', 'potential_magnitude'))
        res_val = float(config.get('dc-response', 'resistivity'))
        cap_val = float(config.get('dc-response', 'capacitance'))
        ind_val = float(config.get('dc-response', 'inductance'))
        leak_val = float(config.get('dc-response', 'leak_resistivity'))

        options_rgt["potential_frequency"]["value"], options_rgt["potential_frequency"]["multiplier"] = number_to_scientific_parts(freq_val)
        options_rgt["potential_fraction"]["value"], options_rgt["potential_fraction"]["multiplier"] = number_to_scientific_parts(frac_val)
        options_rgt["potential_magnitude"]["value"], options_rgt["potential_magnitude"]["multiplier"] = number_to_scientific_parts(mag_val)
        options_rgt["resistivity"]["value"], options_rgt["resistivity"]["multiplier"] = number_to_scientific_parts(res_val)
        options_rgt["capacitance"]["value"], options_rgt["capacitance"]["multiplier"] = number_to_scientific_parts(cap_val)
        options_rgt["inductance"]["value"], options_rgt["inductance"]["multiplier"] = number_to_scientific_parts(ind_val)
        options_rgt["leak_resistivity"]["value"], options_rgt["leak_resistivity"]["multiplier"] = number_to_scientific_parts(leak_val)

        return options_rgt
    except configparser.NoSectionError:
        return options_rgt
