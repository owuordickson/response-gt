# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) controller class for network retrieval and computations.
"""

import numpy as np
import logging
from PySide6.QtCore import Signal, Slot, QObject


class NetworkController(QObject):


    changeImageSignal = Signal()
    imageChangedSignal = Signal()

    def __init__(self, controller_obj, parent: QObject = None):
        super().__init__(parent)
        self._ctrl = controller_obj
        self._img_loaded = False

        # Create Models
        # self.rgt = TreeModel([])

        # Attach listener for syncing models
        self._ctrl.syncModelSignal.connect(self.synchronize_graph_models)

    def start_task(self, msg: str = "please wait..."):
        """Activate the wait flag and send a wait signal."""
        self._ctrl.wait_msg = msg
        self._ctrl.wait_flag = True

    def stop_task(self):
        """Deactivate the wait flag and send a wait signal."""
        self._ctrl.wait_msg = ""
        self._ctrl.wait_flag = False

    def synchronize_graph_models(self, rgt_obj):
        """"""
        pass

    @Slot(result=bool)
    def display_image(self):
        return self._img_loaded

    @Slot(result=str)
    def get_pixmap(self):
        """Returns the URL that QML should use to load the image"""
        unique_num = np.random.randint(low=21, high=1000)
        return "image://imageProvider/" + str(unique_num)

    @Slot()
    def export_response_to_file(self, response_type: str):
        """Export network data and save as a file."""
        pass
