# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) controller class for network retrieval and computations.
"""

import logging
import numpy as np
from sgtlib.modules import ProgressData
from PySide6.QtCore import Signal, Slot, QObject

from ...compute.response_analyzer import ALLOWED_GRAPH_FILE_EXTENSIONS


class NetworkController(QObject):


    changeImageSignal = Signal()
    imageChangedSignal = Signal()

    def __init__(self, controller_obj, parent: QObject = None):
        super().__init__(parent)
        self._ctrl = controller_obj
        self._graph_loaded = False

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
    def graph_is_ready(self):
        return self._graph_loaded

    @Slot(result=str)
    def get_pixmap(self):
        """Returns the URL that QML should use to load the image"""
        unique_num = np.random.randint(low=21, high=1000)
        return "image://imageProvider/" + str(unique_num)

    @Slot(result=str)
    def get_file_extensions(self):
        pattern_string = ' '.join(ALLOWED_GRAPH_FILE_EXTENSIONS)
        return f"Graph files ({pattern_string})"

    @Slot(result=bool)
    def enable_edge_list_upload(self):
        if self._ctrl.wait_flag:
            return False
        return True if self._ctrl.rgt_obj.edge_list is None else False

    @Slot(result=bool)
    def enable_vertex_positions_upload(self):
        if self._ctrl.wait_flag:
            return False
        return True if self._ctrl.rgt_obj.vertex_coordinates is None else False

    @Slot(result=bool)
    def graph_data_uploaded(self):
        is_edge_list_uploaded = not self.enable_edge_list_upload()
        is_vertex_positions_uploaded = not self.enable_vertex_positions_upload()
        return is_edge_list_uploaded and is_vertex_positions_uploaded

    @Slot(str)
    def upload_edge_list(self, file_path: str):
        """Upload an edge list file and return True if successful."""
        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            self.start_task()
            self._ctrl.submit_job(1, "Upload CSV", (file_path, 2), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Upload Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Error occurred!"))
            self._ctrl.handle_finished(1, False, ["Upload Error",  "Fatal error while trying to upload edge list."])

    @Slot(str)
    def upload_vertex_positions(self, file_path: str):
        """Upload a vertex position file and return True if successful."""
        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            self.start_task()
            self._ctrl.submit_job(1, "Upload CSV", (file_path, 1,), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Upload Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Error occurred!"))
            self._ctrl.handle_finished(1, False, ["Upload Error", "Fatal error while trying to upload vertex positions."])

    @Slot()
    def run_response_analyzer(self):
        """Run the response analyzer and send a progress signal."""

        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            if self._ctrl.rgt_obj.edge_list is None or self._ctrl.rgt_obj.vertex_coordinates is None:
                return

            self.start_task()
            self._ctrl.submit_job(1, "Compute Response", (self._ctrl.rgt_obj,), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Response Analyzer Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Fatal error occurred!"))
            self._ctrl.handle_finished(1, False, ["Analyzer Error",  "Fatal error while trying to compute ac-response."])

    @Slot()
    def export_response_to_file(self):
        """Export response (edge currents OR vertex potentials) and save as a file."""
        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            self.start_task()
            self._ctrl.submit_job(1, "Save Results", (self._ctrl.rgt_obj,), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Download Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(
                ProgressData(type="error", sender="RGT", message=f"Fatal error occurred!"))
            self._ctrl.handle_finished(1, False, ["Download Error", "Fatal error while trying to save results to file."])
