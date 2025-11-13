from PIL import Image, ImageQt  # Import ImageQt for conversion
from PySide6.QtGui import QPixmap
from PySide6.QtQuick import QQuickImageProvider


class ImageProvider(QQuickImageProvider):

    def __init__(self, main_controller):
        super().__init__(QQuickImageProvider.ImageType.Pixmap)
        self._pixmap = QPixmap()
        self._main_ctrl = main_controller
        self._main_ctrl.network_ctrl.changeImageSignal.connect(self.handle_change_image)

    def handle_change_image(self):
        if self._main_ctrl.rgt_obj is None:
            self._main_ctrl.network_ctrl._graph_loaded = False
            self._main_ctrl.network_ctrl.imageChangedSignal.emit()
            return

        if self._main_ctrl.rgt_obj.network_img is None:
            self._main_ctrl.network_ctrl._graph_loaded = False
            self._main_ctrl.network_ctrl.imageChangedSignal.emit()
            return

        img_cv = self._main_ctrl.rgt_obj.network_img
        img = Image.fromarray(img_cv)
        self._pixmap = ImageQt.toqpixmap(img)

        # Acknowledge the image load and send the signal to update QML
        self._main_ctrl.network_ctrl._graph_loaded = True
        self._main_ctrl.network_ctrl.imageChangedSignal.emit()
        print(f"Image loaded: {self._main_ctrl.rgt_obj.network_img.shape}")

    def requestPixmap(self, img_id, requested_size, size):
        return self._pixmap
