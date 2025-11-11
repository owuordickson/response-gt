# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) main controller class.
"""

import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal, Slot, QObject

from .network_controller import NetworkController
from ... import __version__, __title__

class MainController(QObject):

    _waitChanged = Signal()
    _waitTextChanged = Signal()
    errorSignal = Signal(str)
    showAlertSignal = Signal(str, str)
    changeImageSignal = Signal()
    imageChangedSignal = Signal()
    syncModelSignal = Signal(object)
    updateProgressSignal = Signal(int, str)
    taskTerminatedSignal = Signal(bool, list)

    def __init__(self, qml_app: QApplication, parent: QObject = None):
        super().__init__(parent)
        self._qml_app = qml_app

        # Initialize flags
        self._wait_flag = False
        self._wait_msg = ""

        # Create network objects
        # self._config_file = config_file
        self._rgt_obj = None

        # Add Controllers
        self.network_ctrl = NetworkController(self)

        # Create Persistent Workers (Processes)
        # self._rgt_worker = PersistentProcessWorker()

    @Slot(result=str)
    def get_app_title(self):
        return f"{__title__}"

    @Slot(result=str)
    def get_app_version(self):
        """"""
        return f"v{__version__}"
