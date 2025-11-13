# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) controller class for network retrieval and computations.
"""

import logging
import numpy as np
from sgtlib.modules import ProgressData, TaskResult
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

    @Slot(str, result=bool)
    def upload_edge_list(self, file_path: str):
        """Upload an edge list file and return True if successful."""
        edges = self._ctrl.add_graph_file(file_path)
        if edges is None:
            return False
        self._ctrl.rgt_obj.edge_list = edges

        self.imageChangedSignal.emit()
        self.run_response_analyzer()  # TO BE DELETED
        return True

    @Slot(str, result=bool)
    def upload_vertex_positions(self, file_path: str):
        """Upload a vertex position file and return True if successful."""
        node_positions = self._ctrl.add_graph_file(file_path)
        if node_positions is None:
            return False

        # flips vertically to have same orientation as initial image
        y_coords, x_coords = zip(*node_positions)
        neg_y_coords = [y * -1 for y in y_coords]
        self._ctrl.rgt_obj.vertex_coordinates = np.array(list(zip(x_coords, neg_y_coords)))

        self.imageChangedSignal.emit()
        return True

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
            self._ctrl.rgt_obj.compute_ac_response()
            self._ctrl.handle_finished(True, TaskResult(task_id="Compute Response", data=self._ctrl.rgt_obj, message="Response analyzer completed successfully!"))
        except Exception as err:
            self.stop_task()
            logging.exception("Response Analyzer Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Fatal error occurred! Close the app and try again."))
            self._ctrl.handle_finished(False, ["Analyzer Error",  "Fatal error while trying to compute ac-response. Close the app and try again."])

    @Slot()
    def export_response_to_file(self, response_type: str):
        """Export response (edge currents OR vertex potentials) and save as a file."""
        pass
