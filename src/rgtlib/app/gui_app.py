# SPDX-License-Identifier: GNU GPL v3

"""
Pyside6 implementation of ResponseGT user interface.
"""

import os
import sys
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine


class PySideApp(QObject):

    def _initialize_models(self):
        """Initialize the models and providers used by the QML engine."""
        # self._ui_engine.addImageProvider("imageProvider", self._image_provider)

    def _initialize_controllers(self):
        """Initialize the controllers used by the QML engine."""
        # self._ui_engine.rootContext().setContextProperty("mainController", self._ctrl)

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self._ui_engine = QQmlApplicationEngine()
        ## Register Controller for Dynamic Updates
        # self._ctrl = MainController(qml_app=self.app)
        ## Register Image Provider
        #self._image_provider = ImageProvider(self._ctrl)
        self._qml_file = 'qml/MainWindow.qml'

        # Set Models in QML Context
        self._initialize_models()
        self._initialize_controllers()

        ## Cleanup when the app is closing
        # self.app.aboutToQuit.connect(self._ctrl.cleanup_workers)

        # Load UI
        # Get the directory of the current script
        qml_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(qml_dir, self._qml_file)

        # Load the QML file and display it
        self._ui_engine.load(qml_path)
        if not self._ui_engine.rootObjects():
            sys.exit(-1)

    @classmethod
    def start(cls) -> None:
        """
        Initialize and run the PySide GUI application.
        """
        gui_app = cls()
        sys.exit(gui_app.app.exec())
