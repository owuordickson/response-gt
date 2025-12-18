# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) main controller class.
"""

import logging
import numpy as np
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Signal, Slot, QObject
from sgtlib.modules import ProgressData, TaskResult

from .theme_manager import ThemeManager
from .network_controller import NetworkController
from ..workers.base_workers import BaseWorker
from ..workers.persistent_worker import PersistentProcessWorker
from ... import __version__, __title__
from ...compute.response_analyzer import ResponseAnalyzer


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
        self.theme_ctrl = ThemeManager()
        self.network_ctrl = NetworkController(self)

        # Create Persistent Workers (Processes)
        self._rgt_worker = PersistentProcessWorker(worker_id=1)

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

    def _cancel_loading(self, worker_id):
        if worker_id == 1:
            self.network_ctrl.stop_task()

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

    def handle_finished(self, worker_id: int, success_val: bool, result: None | TaskResult | list) -> None:
        """
        Handler function for sending updates/signals on termination of tasks.
        Args:
            worker_id: The process worker ID.
            success_val: True if the task was successful, False otherwise.
            result: The result of the task.
        Returns:
            None
        """
        self._cancel_loading(worker_id)
        if not success_val:
            if type(result) is list:
                logging.info(f"{result[0]} : {result[1]}", extra={'user': 'RGT Logs'})
                self.taskTerminatedSignal.emit(success_val, result)
        else:
            if isinstance(result, TaskResult):
                self.stop_current_task(cancel_job=False)
                if result.task_id == "Upload CSV":
                    upload_type = result.data[0]
                    file_path = result.data[1]
                    graph_data = result.data[2]

                    if type(file_path) is str:
                        self.rgt_obj._save_path = file_path

                    if upload_type == "vertices":
                        node_positions = graph_data
                        if node_positions is not None:
                            # flips vertically to have same orientation as initial image
                            y_coords, x_coords = zip(*node_positions)
                            neg_y_coords = [y * -1 for y in y_coords]
                            self.rgt_obj.list_data["vertex_coordinates"]["data"] = np.array(list(zip(x_coords, neg_y_coords)))
                            self.rgt_obj.list_data["vertex_coordinates"]["value"] = 1
                    elif upload_type == "edges":
                        edges = graph_data
                        if edges is not None:
                            self.rgt_obj.edge_list = edges
                            self.rgt_obj.list_data["edge_list"]["data"] = edges
                            self.rgt_obj.list_data["edge_list"]["value"] = 1
                    elif upload_type == "Potential List":
                        imposed_vertices = graph_data
                        if imposed_vertices is not None:
                            self.rgt_obj.list_data["given_potential_list"]["data"] = imposed_vertices
                            self.rgt_obj.list_data["given_potential_list"]["type"] = "File"
                            self.rgt_obj.list_data["given_potential_list"]["value"] = 1
                    elif upload_type == "Vertex List":
                        vert_list = graph_data
                        if vert_list is not None:
                            self.rgt_obj.list_data["vertex_list"]["data"] = vert_list
                            self.rgt_obj.list_data["vertex_list"]["type"] = "File"
                            self.rgt_obj.list_data["vertex_list"]["value"] = 1
                    elif upload_type == "Resistivity List":
                        res_list = graph_data
                        if res_list is not None:
                            self.rgt_obj.list_data["resistivity_list"]["data"] = res_list
                            self.rgt_obj.list_data["resistivity_list"]["value"] = 1
                    elif upload_type == "Inductance List":
                        ind_list = graph_data
                        if ind_list is not None:
                            self.rgt_obj.list_data["inductance_list"]["data"] = ind_list
                            self.rgt_obj.list_data["inductance_list"]["value"] = 1
                    elif upload_type == "Capacitance List":
                        cap_list = graph_data
                        if cap_list is not None:
                            self.rgt_obj.list_data["capacitance_list"]["data"] = cap_list
                            self.rgt_obj.list_data["capacitance_list"]["value"] = 1
                    elif upload_type == "Leak Resistivity List":
                        leak_list = graph_data
                        if leak_list is not None:
                            self.rgt_obj.list_data["leak_resistivity_list"]["data"] = leak_list
                            self.rgt_obj.list_data["leak_resistivity_list"]["value"] = 1
                    self.handle_progress_update(ProgressData(percent=100, sender="RGT", message=f"File Uploaded!"))
                    self.syncModelSignal.emit(self.rgt_obj)  # Sync models and refresh image
                    self.network_ctrl.imageChangedSignal.emit()  # trigger QML UI update
                    self.taskTerminatedSignal.emit(success_val, [])  # Hide Alert-Dialog
                if result.task_id == "Save Results":
                    # Saving files to Output Folder
                    self.handle_progress_update(ProgressData(percent=100, sender="RGT", message=f"Files Saved!"))
                    self.taskTerminatedSignal.emit(success_val, ["Files Saved", result.message])
                if result.task_id == "Compute Response":
                    new_rgt_obj = result.data
                    self.rgt_obj.copy_rgt_obj(new_rgt_obj)
                    self.handle_progress_update(ProgressData(percent=100, sender="RGT", message=result.message))

                    self.syncModelSignal.emit(self.rgt_obj) # Sync models and refresh image
                    self.network_ctrl.changeImageSignal.emit() # trigger QML UI update (load image)
                    self.taskTerminatedSignal.emit(success_val, [])  # Hide Alert-Dialog
            else:
                self.taskTerminatedSignal.emit(success_val, [])

    def submit_job(self, worker_id, task_fxn, fxn_args=(), track_updates: bool = True) -> None:
        """Start a background thread and its associated worker."""

        def _sync_signals(bg_worker: PersistentProcessWorker):
            bg_worker.taskCompleted.connect(self.handle_finished)
            if track_updates:
                bg_worker.inProgress.connect(self.handle_progress_update)

        if task_fxn is None or worker_id is None:
            return

        base_funcs = BaseWorker()

        if task_fxn == "Compute Response":
            target = base_funcs.task_compute_response
        elif task_fxn == "Upload CSV":
            target = base_funcs.task_upload_csv
        elif task_fxn == "Save Results":
            target = base_funcs.task_save_results
        else:
            return

        if worker_id == 1:
            started = self._rgt_worker.submit_task(func=target, args=fxn_args)
            if not started:
                self.showAlertSignal.emit("Please Wait", "Another GT job is running!")
                return
            _sync_signals(self._rgt_worker)
        else:
            return

    @Slot(int)
    def stop_current_task(self, worker_id: int = 1, cancel_job: bool = True):
        """Stop a background thread and its associated worker."""
        # self.showAlertSignal.emit("Important Alert", "Cancelling job, please wait...")
        if worker_id == 1:
            if cancel_job:
                self.handle_progress_update(
                    ProgressData(percent=99, sender="RGT", message="Cancelling job, please wait..."))
            else:
                # Restart Process after 3 tasks
                if self._rgt_worker.task_count < 3:
                    return
            self._rgt_worker.stop()
            self._rgt_worker = PersistentProcessWorker(worker_id)
            self.handle_finished(worker_id, True, None)

    @Slot(result=str)
    def get_about_details(self):
        about_str = f"""{__title__} v{__version__}"""
        self.network_ctrl.imageChangedSignal.emit()
        return about_str

    @Slot(result=str)
    def get_app_title(self):
        return f"{__title__}"

    @Slot(result=str)
    def get_app_version(self):
        """"""
        return f"v{__version__}"

    @Slot(result=bool)
    def is_task_running(self):
        return self._wait_flag

    @Slot()
    def reset_rgt_obj(self):
        self.rgt_obj.reset()
        self.network_ctrl._graph_loaded = False
        self.network_ctrl.imageChangedSignal.emit()

    @Slot()
    def load_graph_into_view(self):
        """Load the graph into the view."""
        try:
            self.network_ctrl.changeImageSignal.emit()
        except Exception as err:
            # self.reset_rgt_obj()
            self.network_ctrl.imageChangedSignal.emit()
            logging.exception("View Error: %s", err, extra={'user': 'RGT Logs'})
            self.showAlertSignal.emit("Graph Error", "Error loading graph. Try again.")
