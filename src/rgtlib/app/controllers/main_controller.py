# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) main controller class.
"""

import os
import logging
import numpy as np
import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal, Slot, QObject
from sgtlib.modules import ProgressData, TaskResult, verify_path

from .network_controller import NetworkController
from ... import __version__, __title__
from ...compute.response_analyzer import ResponseAnalyzer, ALLOWED_GRAPH_FILE_EXTENSIONS


class MainController(QObject):

    _waitChanged = Signal()
    _waitTextChanged = Signal()
    errorSignal = Signal(str)
    showAlertSignal = Signal(str, str)
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
        self._config_file = ""
        self._rgt_obj = ResponseAnalyzer(self._config_file)

        # Add Controllers
        self.network_ctrl = NetworkController(self)

        # Create Persistent Workers (Processes)
        self._rgt_worker = None #PersistentProcessWorker()

    @property
    def wait_flag(self) -> bool:
        """Returns the wait flag indicating if the application is currently running a task in the background."""
        return self._wait_flag

    @wait_flag.setter
    def wait_flag(self, value: bool):
        """Sets the wait flag indicating if the application is currently running a task in the background."""
        self._wait_flag = value

    @property
    def wait_msg(self) -> str:
        """Returns the wait message indicating the current task."""
        return self._wait_msg

    @wait_msg.setter
    def wait_msg(self, value: str):
        """Sets the wait message indicating the current task."""
        self._wait_msg = value

    @property
    def rgt_obj(self):
        return self._rgt_obj

    def _cancel_loading(self):
        pass

    def cleanup_workers(self):
        """Stop all persistent workers before app exit."""
        self.showAlertSignal.emit("Important Alert", "Please wait as we safely close the app...")
        for worker in [self._rgt_worker]:
            if worker:
                worker.stop()

    def handle_progress_update(self, status_data: ProgressData) -> None:
        """
        Handler function for progress updates for ongoing GT tasks.
        Args:
            status_data: ProgressData object that contains the percentage and status message of the current task.

        Returns:

        """

        if status_data is None:
            return

        if 0 <= status_data.percent <= 100:
            self.updateProgressSignal.emit(status_data.percent, status_data.message)
            logging.info(f"({status_data.sender}) {status_data.percent}%: {status_data.message}", extra={'user': 'RGT Logs'})

        if status_data.type == "info":
            self.updateProgressSignal.emit(101, status_data.message)
            logging.info(f"({status_data.sender}) {status_data.message}", extra={'user': 'RGT Logs'})
        elif status_data.type == "error":
            self.errorSignal.emit(status_data.message)
            logging.exception(f"({status_data.sender}) {status_data.message}", extra={'user': 'RGT Logs'})

    def handle_finished(self, success_val: bool, result: None | TaskResult | list) -> None:
        """
        Handler function for sending updates/signals on termination of tasks.
        Args:
            success_val: True if the task was successful, False otherwise.
            result: The result of the task.
        Returns:
            None
        """
        self._cancel_loading()
        if not success_val:
            if type(result) is list:
                logging.info(f"{result[0]} : {result[1]}", extra={'user': 'RGT Logs'})
                self.taskTerminatedSignal.emit(success_val, result)
        else:
            if isinstance(result, TaskResult):
                self.stop_current_task(cancel_job=False)
                if result.task_id == "Export Graph":
                    # Saving files to Output Folder
                    self.handle_progress_update(ProgressData(percent=100, sender="RGT", message=f"Files Saved!"))
                    self.taskTerminatedSignal.emit(success_val, ["Files Saved", result.message])
                if result.task_id == "Compute Response":
                    self.handle_progress_update(ProgressData(percent=100, sender="RGT", message=result.message))
                    self.load_graph_into_view()  # trigger QML UI update
                    self.taskTerminatedSignal.emit(success_val, ["Response calculations completed", result.message])
            else:
                self.taskTerminatedSignal.emit(success_val, [])

    def submit_job(self, task_fxn, fxn_args=()):
        """"""
        if task_fxn == "Compute Response":
            print(f"{self._rgt_obj}: {fxn_args}")
        else:
            return

    def add_graph_file(self, file_path: str) -> None | np.ndarray:
        """Read the file and return graph data."""
        success, result = verify_path(file_path)
        if success:
            file_path = result
        else:
            logging.info(result, extra={'user': 'RGT Logs'})
            self.showAlertSignal.emit("File Error", result)
            return None

        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            allowed_ext = tuple(ext[1:] if ext.startswith('*.') else ext for ext in ALLOWED_GRAPH_FILE_EXTENSIONS)
            if file_ext not in allowed_ext:
                throw_msg = f"File extension {file_ext} is not allowed. Allowed extensions are {allowed_ext}"
                raise ValueError(throw_msg)

            graph_data = pd.read_csv(file_path, header=None, index_col=False).to_numpy()
            return graph_data
        except Exception as err:
            logging.exception("File Error: %s", err, extra={'user': 'RGT Logs'})
            self.showAlertSignal.emit("File Error", f"Error reading {file_path}. Try again.")
            return None

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
        if cancel_job:
            self.handle_progress_update(ProgressData(percent=99, sender="RGT", message="Cancelling job, please wait..."))
        else:
            # Restart Process after 3 tasks
            if self._rgt_worker.task_count < 3:
                return
        #self._rgt_worker.stop()
        #self._rgt_worker = PersistentProcessWorker()
        self.handle_finished(True, None)

    @Slot(result=bool)
    def is_task_running(self):
        return self._wait_flag

    @Slot()
    def reset_rgt_obj(self):
        self.rgt_obj.reset()
        self.network_ctrl._graph_loaded = False
        self.load_graph_into_view()

    @Slot()
    def load_graph_into_view(self):
        """Load the graph into the view."""
        try:
            if self.rgt_obj.vertex_coordinates is not None and self.rgt_obj.edge_list is not None:
                plt_fig = self.rgt_obj.plot_response_graph()
                if plt_fig is not None:
                    self.network_ctrl._graph_loaded = True
            self.network_ctrl._graph_loaded = False
            self.network_ctrl.imageChangedSignal.emit()
        except Exception as err:
            # self.reset_rgt_obj()
            self.network_ctrl._graph_loaded = False
            self.network_ctrl.imageChangedSignal.emit()
            logging.exception("View Error: %s", err, extra={'user': 'RGT Logs'})
            self.showAlertSignal.emit("Graph Error", "Error loading graph. Try again.")
