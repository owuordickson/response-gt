# SPDX-License-Identifier: GNU GPL v3

"""
Entry points that allow users to execute GUI program
"""

import sys
import logging
from .app.gui_app import PySideApp


logger = logging.getLogger("RGT App")
# FORMAT = '%(asctime)s; %(user)s. %(levelname)s: %(message)s'
FORMAT = '%(asctime)s; %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def main_gui() -> None:
    """
    Start the graphical user interface application.
    :return:
    """
    # Initialize log collection
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", stream=sys.stdout)
    logging.info("RGT application started running...", extra={'user': 'RGT Logs'})

    # Start GUI app
    PySideApp.start()

    # Log to show the App stopped
    logging.info("RGT application stopped running.", extra={'user': 'RGT Logs'})
