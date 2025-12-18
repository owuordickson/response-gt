# SPDX-License-Identifier: GNU GPL v3

"""
Base worker class for executing all resource-intensive StructuralGT tasks.
"""

import os
import logging
from sgtlib.modules import ProgressData, TaskResult, verify_path, csv_to_numpy
from ...compute.response_analyzer import ALLOWED_GRAPH_FILE_EXTENSIONS


class BaseWorker:

    def __init__(self):
        self._progress_queue = None

    @property
    def progress_queue(self):
        return self._progress_queue

    def _update_progress(self, status_data: ProgressData):
        """
        Send the update_progress signal to all listeners.
        Progress-value (0-100), progress-message (str)
        Args:
            status_data: ProgressData object that contains the percentage and status message of the current task.

        Returns:

        """
        if self._progress_queue is None:
            return
        self._progress_queue.put(("progress", status_data))

    def attach_progress_queue(self, queue):
        """Attach or replace the progress queue (status_queue)."""
        if self._progress_queue is None:
            self._progress_queue = queue

    def task_save_results(self, rgt_obj):
        """"""
        try:
            self._update_progress(ProgressData(percent=25, sender="RGT", message=f"Saving Response Data..."))
            success = rgt_obj.save_results_to_file()
            self._update_progress(ProgressData(percent=95, sender="RGT", message=f"Saving Response Data..."))
            if not success:
                raise ValueError("Error while saving results!")
            task_data = TaskResult(task_id="Save Results", status="Finished", message="Response files successfully saved in 'Output Dir'")
            return True, task_data
        except Exception as err:
            logging.exception("Error: %s", err, extra={'user': 'RGT Logs'})
            return False, ["Download Failed", "Error while saving results!"]

    def task_compute_response(self, rgt_obj):
        """"""
        try:
            rgt_obj.abort = False
            rgt_obj.add_listener(self._update_progress)
            rgt_obj.run_analyzer()
            if rgt_obj.abort:
                raise ValueError("Process aborted")
            rgt_obj.remove_listener(self._update_progress)
            task_data = TaskResult(task_id="Compute Response", status="Finished", message="AC Response computed successfully!", data=rgt_obj)
            return True, task_data
        except ValueError as err:
            logging.exception("Task Aborted: %s", err, extra={'user': 'RGT Logs'})
            # Clean up listeners before exiting
            rgt_obj.remove_listener(self._update_progress)
            return False, ["Computation Aborted", "Error occurred while computing ac-response. Re-upload the CSV files and try again. If error persists then close "
                                                   "the app and try again."]
        except Exception as err:
            logging.exception("Error: %s", err, extra={'user': 'RGT Logs'})
            self._update_progress(ProgressData(type="error", sender="RGT", message=f"Error encountered! Try again."))
            # Clean up listeners before exiting
            rgt_obj.remove_listener(self._update_progress)
            # Emit failure signal (aborted)
            return False, ["Computation Failed", "Error occurred while computing ac-response. Re-upload the CSV files and try again. If error persists then close "
                                                   "the app and try again."]

    def task_upload_csv(self, file_path: str, upload_type: str):
        """"""
        try:
            # 1. Verify if the file exists
            self._update_progress(ProgressData(percent=25, sender="RGT", message=f"Reading File..."))
            success, result = verify_path(file_path)
            if success:
                file_path = result
            else:
                raise ValueError("File Error")

            # 2. Check if the file extension is allowed
            self._update_progress(ProgressData(percent=35, sender="RGT", message=f"Reading File..."))
            file_ext = os.path.splitext(file_path)[1].lower()
            allowed_ext = tuple(ext[1:] if ext.startswith('*.') else ext for ext in ALLOWED_GRAPH_FILE_EXTENSIONS)
            if file_ext not in allowed_ext:
                throw_msg = f"File extension {file_ext} is not allowed. Allowed extensions are {allowed_ext}"
                raise ValueError(throw_msg)

            # 3. Read the file and return graph data
            self._update_progress(ProgressData(percent=50, sender="RGT", message=f"Reading File..."))
            graph_data = csv_to_numpy(file_path)
            self._update_progress(ProgressData(percent=95, sender="RGT", message=f"Reading File..."))
            task_data = TaskResult(task_id="Upload CSV", status="Finished", message="CSV file successfully uploaded!", data=[upload_type, file_path,  graph_data])
            return True, task_data
        except ValueError as err:
            logging.exception("Task Aborted: %s", err, extra={'user': 'RGT Logs'})
            return False, ["File Upload Failed", f"Error while reading file {file_path}!"]
        except Exception as err:
            logging.exception("File Error: %s", err, extra={'user': 'RGT Logs'})
            return False, ["File Error", f"Error reading {file_path}! Try again."]
