# SPDX-License-Identifier: GNU GPL v3
"""
Pyside6 (GUI components) controller class for network retrieval and computations.
"""

import logging
import numpy as np
from sgtlib.modules import ProgressData
from PySide6.QtCore import Signal, Slot, QObject

from ..models.checkbox_model import CheckBoxModel
from ...utils.config_loader import get_metric_options
from ...compute.response_analyzer import ALLOWED_GRAPH_FILE_EXTENSIONS


class NetworkController(QObject):


    changeImageSignal = Signal()
    imageChangedSignal = Signal()

    def __init__(self, controller_obj, parent: QObject = None):
        super().__init__(parent)
        self._ctrl = controller_obj
        self._graph_loaded = False
        self._applying_changes = False

        # Create Models
        self.rgtOptions = CheckBoxModel([])
        self.rgtDCParams = CheckBoxModel([])
        self.rgtPotentialOptions = CheckBoxModel([])
        self.rgtPotentialDirections = CheckBoxModel([])
        self.metricsModel = CheckBoxModel(get_metric_options())

        # Attach listener for syncing models
        self._ctrl.syncModelSignal.connect(self.synchronize_rgt_models)

    def start_task(self, msg: str = "please wait..."):
        """Activate the wait flag and send a wait signal."""
        self._ctrl.wait_msg = msg
        self._ctrl.wait_flag = True

    def stop_task(self):
        """Deactivate the wait flag and send a wait signal."""
        self._ctrl.wait_msg = ""
        self._ctrl.wait_flag = False

    def synchronize_rgt_models(self, rgt_obj):
        """
        Reload ResponseGT configuration selections and controls from saved dict to QML components at every sync signal.

        :param rgt_obj: ResponseGT object with all the saved user-selected configuration selections.
        """
        if rgt_obj is None:
            return

        try:
            # Models Auto-update with saved sgt_obj configs. No need to re-assign!
            options_rgt = rgt_obj.configs

            # Get data from object configs
            rgt_settings = [v for v in options_rgt.values() if v["type"] == "rgt-settings"]
            rgt_dc_params = [v for v in options_rgt.values() if v["type"] == "dc-param"]
            rgt_potentials = [v for v in options_rgt.values() if v["type"] == "potential-settings"]
            rgt_pot_dir = options_rgt["potential_direction"]["items"]

            # Update QML adapter-models with fetched data
            self.rgtOptions.reset_data(rgt_settings)
            self.rgtDCParams.reset_data(rgt_dc_params)
            self.rgtPotentialOptions.reset_data(rgt_potentials)
            self.rgtPotentialDirections.reset_data(rgt_pot_dir)
        except Exception as err:
            logging.exception("Fatal Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Fatal Error", "Error re-loading RGT configurations! Close app and try again.")

    def update_response_params(self, rgt_obj):
        """Update the visible response parameters based on the Response-type."""
        if rgt_obj is None:
            return

        try:
            options_rgt = rgt_obj.configs
            res_type = options_rgt["response_type"]["value"]
            rgt_dc_params = [v for v in options_rgt.values() if v["type"] == "dc-param"]
            for  param in rgt_dc_params:
                if param["id"] == "resistivity":
                    param["visible"] = 1
                else:
                    param["visible"] = res_type
            self.rgtDCParams.reset_data(rgt_dc_params)
        except Exception as err:
            logging.exception("Fatal Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Fatal Error", "Error updating RGT parameters!")

    @Slot()
    def test_method(self):
        print("Test method called!")

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
        return not self._ctrl.rgt_obj.edges_uploaded

    @Slot(result=bool)
    def enable_vertex_positions_upload(self):
        if self._ctrl.wait_flag:
            return False
        return not self._ctrl.rgt_obj.vertices_uploaded

    @Slot(result=bool)
    def graph_data_uploaded(self):
        is_edge_list_uploaded = not self.enable_edge_list_upload()
        is_vertex_positions_uploaded = not self.enable_vertex_positions_upload()
        return is_edge_list_uploaded and is_vertex_positions_uploaded

    @Slot()
    def apply_changes(self):
        """Retrieve changes made by the user and apply to the response graph."""
        if not self._applying_changes:  # Disallow concurrent changes
            self._applying_changes = True
            self.update_response_params(self._ctrl.rgt_obj)
        self.changeImageSignal.emit()

    @Slot(str, str)
    def apply_imposed_vertices(self, source: str, data: str):
        """Apply imposed vertices to the response graph."""
        try:
            print(f"Applying {source} with data: {data}")
            if data != "":
                # Convert to a numpy array
                arr_data = np.array(data.split(","), dtype=float)
                print(arr_data)
                self._ctrl.rgt_obj.list_data["given_potential_list"]["data"] = arr_data
                self._ctrl.rgt_obj.list_data["given_potential_list"]["value"] = 1
        except Exception as err:
            logging.exception("Upload Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_finished(1, False, ["Upload Error", f"Unable to read your data. Try this format for vertex position and its potential: [position-1, potential-1], [position-2, potential-2], ..."])

    @Slot(str, str)
    def upload_file_data(self, file_path: str, param_type: str):
        """Upload a CSV file and return True if successful."""
        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            self.start_task()
            self._ctrl.submit_job(1, "Upload CSV", (file_path, param_type,), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Upload Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Error occurred!"))
            self._ctrl.handle_finished(1, False, ["Upload Error", f"Fatal error while trying to upload {param_type}."])

    @Slot()
    def run_response_analyzer(self):
        """Run the response analyzer and send a progress signal."""

        if self._ctrl.wait_flag:
            logging.info("Please Wait: Another task is running!", extra={'user': 'RGT Logs'})
            self._ctrl.showAlertSignal.emit("Please Wait", "Another task is running!")
            return

        try:
            if (not self._ctrl.rgt_obj.edges_uploaded) or (not self._ctrl.rgt_obj.vertices_uploaded):
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
            if self._ctrl.rgt_obj.list_data["calculated_vertex_potentials"]["data"] is None or self._ctrl.rgt_obj.list_data["calculated_edge_currents"]["data"] is None:
                self._ctrl.handle_finished(1, False,["Download Error", "Please run the 'Compute Response' first."])
                return

            self.start_task()
            self._ctrl.submit_job(1, "Save Results", (self._ctrl.rgt_obj,), True)
        except Exception as err:
            self.stop_task()
            logging.exception("Download Error: %s", err, extra={'user': 'RGT Logs'})
            self._ctrl.handle_progress_update(ProgressData(type="error", sender="RGT", message=f"Fatal error occurred!"))
            self._ctrl.handle_finished(1, False, ["Download Error", "Fatal error while trying to save results to file."])
