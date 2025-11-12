# SPDX-License-Identifier: GNU GPL v3
"""
Compute AC response metrics
"""

import numpy as np
from sgtlib.modules import ProgressUpdate
from ..utils.config_loader import load_rgt_configs


ALLOWED_GRAPH_FILE_EXTENSIONS = ['*.csv']
class ResponseAnalyzer(ProgressUpdate):

    def __init__(self, config_file: str = ""):
        """"""
        super(ResponseAnalyzer, self).__init__()
        self._configs: dict = load_rgt_configs(config_file)
        self._props: list = []
        self._vertex_coordinates: None | np.ndarray = None
        self._vertex_potentials: None | np.ndarray = None
        self._edge_list: None | np.ndarray = None
        self._edge_currents: None | np.ndarray = None

    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, configs):
        self._configs = configs

    @property
    def props(self):
        return self._props

    @property
    def vertex_coordinates(self):
        return self._vertex_coordinates

    @property
    def vertex_potentials(self):
        return self._vertex_potentials

    @property
    def edge_list(self):
        return self._edge_list

    @property
    def edge_currents(self):
        return self._edge_currents

    @edge_list.setter
    def edge_list(self, edge_list: np.ndarray):
        self._edge_list = edge_list

    @vertex_coordinates.setter
    def vertex_coordinates(self, vertex_coordinates: np.ndarray):
        self._vertex_coordinates = vertex_coordinates

    @vertex_potentials.setter
    def vertex_potentials(self, vertex_potentials: np.ndarray):
        self._vertex_potentials = vertex_potentials

    def reset(self):
        """Reset all properties"""
        self._props = []
        self._vertex_coordinates = None
        self._vertex_potentials = None
        self._edge_list = None
        self._edge_currents = None
