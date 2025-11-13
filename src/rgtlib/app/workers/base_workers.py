# SPDX-License-Identifier: GNU GPL v3

"""
Base worker class for executing all resource-intensive StructuralGT tasks.
"""

import logging
from sgtlib.modules import ProgressData, TaskResult


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

    def task_save_images(self, ntwk_p, img_idx):
        """"""
        try:
            self._update_progress(ProgressData(percent=25, sender="GT", message=f"Saving Images..."))
            ntwk_p.save_images_to_file(img_pos=img_idx)
            self._update_progress(ProgressData(percent=95, sender="GT", message=f"Saving Images..."))
            task_data = TaskResult(task_id="Save Images", status="Finished",
                                   message="Image files successfully saved in 'Output Dir'")
            return True, task_data
        except Exception as err:
            logging.exception("Error: %s", err, extra={'user': 'SGT Logs'})
            return False, ["Save Images Failed", "Error while saving images!"]

    def task_export_graph(self, ntwk_p):
        """"""
        try:
            # 1. Get filename
            self._update_progress(ProgressData(percent=25, sender="GT", message=f"Exporting Graph..."))
            filename, out_dir = ntwk_p.get_filenames()

            # 2. Save graph data to the file
            self._update_progress(ProgressData(percent=30, sender="GT", message=f"Exporting Graph..."))
            ntwk_p.graph_obj.save_graph_to_file(filename, out_dir)
            self._update_progress(ProgressData(percent=95, sender="GT", message=f"Exporting Graph..."))
            task_data = TaskResult(task_id="Export Graph", status="Finished",
                                   message="Graph successfully exported to file and saved in 'Output Dir'")
            return True, task_data
        except Exception as err:
            logging.exception("Error: %s", err, extra={'user': 'SGT Logs'})
            return False, ["Export Graph Failed", "Error while exporting graph!"]

    def task_extract_graph(self, ntwk_p):
        """"""
        try:
            ntwk_p.abort = False
            ntwk_p.add_listener(self._update_progress)
            ntwk_p.apply_img_filters()
            ntwk_p.build_graph_network()
            if ntwk_p.abort:
                raise ValueError("Process aborted")
            ntwk_p.remove_listener(self._update_progress)
            task_data = TaskResult(task_id="Extract Graph", status="Finished", message="Graph extracted successfully!", data=ntwk_p)
            return True, task_data
        except ValueError as err:
            logging.exception("Task Aborted: %s", err, extra={'user': 'SGT Logs'})
            # Clean up listeners before exiting
            ntwk_p.remove_listener(self._update_progress)
            return False, ["Extract Graph Aborted", "Graph extraction aborted due to error! "
                                                                          "Change image filters and/or graph settings "
                                                                          "and try again. If error persists then close "
                                                                          "the app and try again."]
        except Exception as err:
            logging.exception("Error: %s", err, extra={'user': 'SGT Logs'})
            self._update_progress(ProgressData(type="error", sender="GT", message=f"Error encountered! Try again."))
            # Clean up listeners before exiting
            ntwk_p.remove_listener(self._update_progress)
            # Emit failure signal (aborted)
            return False, ["Extract Graph Failed", "Graph extraction aborted due to error! "
                                                                          "Change image filters and/or graph settings "
                                                                          "and try again. If error persists then close "
                                                                          "the app and try again."]
