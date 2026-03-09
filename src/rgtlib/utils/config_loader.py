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
        # print(f"Configs loaded successfully from: {config_file}.")
        return config
    except configparser.Error:
        # print(f"Unable to read the configs from {config_file}.")
        return None


def initialize_list_data():
    """Initialize the list of parameters for the ResponseGT computation."""

    response_file_options: dict[str, dict[str, str | int | None | np.ndarray]] = {
        # Electrical Response
        "vertex_coordinates": {"id": "vertex_coordinates", "value": 0, "data": None, "type": "File", "text": "Vertex Coordinates", "visible": 1},
        "edge_list": {"id": "edge_list", "value": 0, "data": None, "type": "File", "text": "Edge List", "visible": 1},
        "resistivity_list": {"id": "resistivity_list", "value": 0, "data": None, "type": "File", "text": "Resistivity List", "visible": 1},
        "inductance_list": {"id": "inductance_list", "value": 0, "data": None, "type": "File", "text": "Inductance List", "visible": 1},
        "capacitance_list": {"id": "capacitance_list", "value": 0, "data": None, "type": "File", "text": "Capacitance List", "visible": 1},
        "leak_resistivity_list": {"id": "leak_resistivity_list", "value": 0, "data": None, "type": "File", "text": "Leak Resistivity List", "visible": 1},
        "given_potential_list": {"id": "given_potential_list", "value": 0, "data": None, "type": "File", "text": "Given Potential List", "visible": 1},
        "vertex_list": {"id": "vertex_list", "value": 0, "data": None, "type": "File", "text": "Vertex List", "visible": 1},
        "calculated_vertex_potentials": {"id": "calculated_vertex_potentials", "value": 0, "data": None, "type": "Custom", "text": "Calculated Vertex Potentials", "visible": 0},
        "calculated_edge_currents": {"id": "calculated_edge_currents", "value": 0, "data": None, "type": "Custom", "text": "Calculated Edge Currents", "visible": 0},
        # Mechanical Response
        "displacement_vector": {"id": "displacement_vector", "value": 0, "data": None, "type": "File", "text": "Displacement Vector", "visible": 1},
        "delete_edge_list": {"id": "delete_edge_list", "value": 0, "data": None, "type": "File", "text": "Edges to Delete", "visible": 1},
        "edge_mask_list": {"id": "edge_mask_list", "value": 0, "data": None, "type": "File", "text": "Valid Edge Mask", "visible": 1},
        "unpinned_vertex_positions": {"id": "unpinned_vertex_positions", "value": 0, "data": None, "type": "Custom", "text": "Calculated Unpinned Vertex Positions", "visible": 0},
        "unpinned_edge_list": {"id": "unpinned_edge_list", "value": 0, "data": None, "type": "Custom", "text": "Calculated Unpinned Edge List", "visible": 0},
        "calculated_displacements": {"id": "calculated_displacements", "value": 0, "data": None, "type": "Custom", "text": "Calculated Displacements", "visible": 0},
        "calculated_tensions": {"id": "calculated_tensions", "value": 0, "data": None, "type": "Custom", "text": "Calculated Tensions", "visible": 0},
        "calculated_active_tensions": {"id": "calculated_active_tensions", "value": 0, "data": None, "type": "Custom", "text": "Calculated Active Tensions", "visible": 0},
    }
    return response_file_options


def get_metric_options() -> list[dict[str, Union[str, int]]]:
    """Return a list of metric options for the QML adapter."""
    metric_options = [
        {"text": "10⁻²⁴", "multiplier": -24},
        {"text": "10⁻²¹", "multiplier": -21},
        {"text": "10⁻¹⁸", "multiplier": -18},
        {"text": "10⁻¹⁵", "multiplier": -15},
        {"text": "10⁻¹²", "multiplier": -12},  # picometer
        {"text": "10⁻⁹", "multiplier": -9},  # nanometer
        {"text": "10⁻⁶", "multiplier": -6},  # micrometer
        {"text": "10⁻³", "multiplier": -3},  # millimeter
        {"text": "10⁻²", "multiplier": -2},  # centimeter
        # {"text": "10⁻¹", "multiplier": -1},    # decimeter
        {"text": "10⁰", "multiplier": 0},  # meter
        # {"text": "10¹", "multiplier": 1},       # dekameter
        # {"text": "10²", "multiplier": 2},       # hectometer
        {"text": "10³", "multiplier": 3},  # kilometer
        {"text": "10⁶", "multiplier": 6},  # megameter
        {"text": "10⁹", "multiplier": 9},  # gigameter
        {"text": "10¹²", "multiplier": 12},  # terameter
        {"text": "10¹⁵", "multiplier": 15},
        {"text": "10¹⁸", "multiplier": 18},
        {"text": "10²¹", "multiplier": 21},
        {"text": "10²⁴", "multiplier": 24},
    ]
    return metric_options


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
        coefficient = float(value / (10 ** multiplier))

        # Ensure coefficient is in [1, 10)
        if abs(coefficient) < 1:
            coefficient *= 10
            multiplier -= 1

        # Force multiplier -1, 1, or 2 back to 0
        if multiplier in {-1, 1, 2}:
            coefficient = value  # collapse scaling into coefficient
            multiplier = 0

        lst_mult_data = get_metric_options()
        mult_range = {x["multiplier"] for x in lst_mult_data}
        if multiplier not in mult_range:
            # Find the closest multiplier in the list
            nearest_multiplier = min(mult_range, key=lambda x: abs(x - multiplier))
            # Update the coefficient and multiplier
            coefficient *= 10 ** (multiplier - nearest_multiplier)
            multiplier = nearest_multiplier
        return coefficient, multiplier

    # add the imposed direction (selected)
    options_rgt: dict[str, dict[str, Union[int, float, list]]] = {
        "response_type": {"id": "response_type", "type": "rgt-settings", "text": "Response Type", "visible": 1, "value": 0},
        "param_type": {"id": "param_type", "type": "param-settings", "text": "Response Type", "visible": 1, "value": 0},

        "potential_direction": {"id": "potential_direction", "type": "potential-settings", "text": "Potential Direction", "visible": 0, "value": 1,
                                "items": [
                                    {"id": "TB", "text": "Top-Bottom", "value": 1},
                                    {"id": "BT", "text": "Bottom-Top", "value": 0},
                                    {"id": "LR", "text": "Left-Right", "value": 0},
                                    {"id": "RL", "text": "Right-Left", "value": 0}
                                ]},
        "potential_magnitude": {"id": "potential_magnitude", "type": "potential-settings", "text": "Potential Magnitude", "visible": 1, "value": 100.0, "minValue": -100, "maxValue": 100},
        "selected_vertex_proportion": {"id": "selected_vertex_proportion", "type": "potential-settings", "text": "Fraction of Vertices", "visible": 1, "value": 0.05, "minValue": 0, "maxValue": 1},
        "potential_frequency": {"id": "potential_frequency", "type": "dc-param", "text": "Potential Frequency", "visible": 1, "value": 1, "multiplier": -6, "minValue": -1000, "maxValue": 1000},

        "resistivity": {"id": "resistivity", "type": "dc-param", "text": "Resistivity", "visible": 1, "value": 1, "multiplier": 0, "minValue": -1000, "maxValue": 1000},
        "capacitance": {"id": "capacitance", "type": "dc-param", "text": "Capacitance", "visible": 1, "value": 1, "multiplier": -6, "minValue": -1000, "maxValue": 1000},
        "inductance": {"id": "inductance", "type": "dc-param", "text": "Inductance", "visible": 1, "value": 1, "multiplier": -9, "minValue": -1000, "maxValue": 1000},
        "leak_resistivity": {"id": "leak_resistivity", "type": "dc-param", "text": "Leak Resistivity", "visible": 1, "value": 1, "multiplier": 6, "minValue": -1000, "maxValue": 1000},

        "cartesian_direction": {"id": "cartesian_direction", "type": "mech-param", "text": "Cartesian Direction", "visible": 1, "value": 0},
        "use_smallest_boolean": {"id": "use_smallest_boolean", "type": "mech-param", "text": "Use Smallest Boolean", "visible": 1, "value": 1},
    }

    # Load configuration from the file
    config = read_config_file(cfg_path)
    if config is None:
        return options_rgt

    try:
        options_rgt["response_type"]["value"] = int(config.get('rgt-settings', 'response_type'))
        options_rgt["param_type"]["value"] = int(config.get('rgt-settings', 'param_type'))
        frac_val = float(config.get('rgt-settings', 'selected_vertex_proportion'))

        pot_dir = str(config.get('dc-response', 'potential_direction'))
        freq_val = float(config.get('dc-response', 'potential_frequency'))
        mag_val = float(config.get('dc-response', 'potential_magnitude'))
        res_val = float(config.get('dc-response', 'resistivity'))
        cap_val = float(config.get('dc-response', 'capacitance'))
        ind_val = float(config.get('dc-response', 'inductance'))
        leak_val = float(config.get('dc-response', 'leak_resistivity'))

        cart_dir = int(config.get('mechanical-response', 'cartesian_direction'))
        small_bool = int(config.get('mechanical-response', 'use_smallest_boolean'))

        options_rgt["selected_vertex_proportion"]["value"] = frac_val
        options_rgt["potential_magnitude"]["value"] = mag_val
        for i in range(len(options_rgt["potential_direction"]["items"])):
            options_rgt["potential_direction"]["items"][i]["value"] = 1 if options_rgt["potential_direction"]["items"][i]["id"] == pot_dir else 0

        options_rgt["potential_frequency"]["value"], options_rgt["potential_frequency"]["multiplier"] = number_to_scientific_parts(freq_val)
        options_rgt["resistivity"]["value"], options_rgt["resistivity"]["multiplier"] = number_to_scientific_parts(res_val)
        options_rgt["capacitance"]["value"], options_rgt["capacitance"]["multiplier"] = number_to_scientific_parts(cap_val)
        options_rgt["inductance"]["value"], options_rgt["inductance"]["multiplier"] = number_to_scientific_parts(ind_val)
        options_rgt["leak_resistivity"]["value"], options_rgt["leak_resistivity"]["multiplier"] = number_to_scientific_parts(leak_val)

        options_rgt["cartesian_direction"]["value"] = cart_dir
        options_rgt["use_smallest_boolean"]["value"] = small_bool

        return options_rgt
    except configparser.NoSectionError:
        return options_rgt
