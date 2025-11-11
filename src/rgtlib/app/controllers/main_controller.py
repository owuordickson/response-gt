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
        self._rgt_worker = None #PersistentProcessWorker()

    def cleanup_workers(self):
        """Stop all persistent workers before app exit."""
        self.showAlertSignal.emit("Important Alert", "Please wait as we safely close the app...")
        for worker in [self._rgt_worker]:
            if worker:
                worker.stop()

    @Slot(result=str)
    def get_about_details(self):
        about_str = f"""{__title__} v{__version__}"""
        return about_str

    @Slot(result=str)
    def get_app_title(self):
        return f"{__title__}"

    @Slot(result=str)
    def get_app_version(self):
        """"""
        return f"v{__version__}"

    @Slot(int)
    def stop_current_task(self, cancel_job: bool = True):
        """Stop a background thread and its associated worker."""
        # self.showAlertSignal.emit("Important Alert", "Cancelling job, please wait...")
        """if cancel_job:
            self.handle_progress_update(
                ProgressData(percent=99, sender="GT", message="Cancelling job, please wait..."))
        else:
            # Restart Process after 3 tasks
            if self._rgt_worker.task_count < 3:
                return
        self._rgt_worker.stop()
        self._rgt_worker = PersistentProcessWorker()
        self.handle_finished(True, None)"""

    @Slot(result=bool)
    def is_task_running(self):
        return self._wait_flag
