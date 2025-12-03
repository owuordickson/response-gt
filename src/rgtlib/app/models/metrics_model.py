from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex


class MetricsModel(QAbstractListModel):
    TextRole = Qt.ItemDataRole.UserRole + 3
    ValueRole = Qt.ItemDataRole.UserRole + 4
    MultiplierRole = Qt.ItemDataRole.UserRole + 12

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = [
            {"text": "10⁻¹²", "value": 1e-12, "multiplier": -12},   # picometer
            {"text": "10⁻⁹", "value": 1e-9, "multiplier": -9},      # nanometer
            {"text": "10⁻⁶", "value": 1e-6, "multiplier": -6},      # micrometer
            {"text": "10⁻³", "value": 1e-3, "multiplier": -3},      # millimeter
            {"text": "10⁻²", "value": 1e-2, "multiplier": -2},      # centimeter
            # {"text": "10⁻¹", "value": 1e-1, "multiplier": -1},    # decimeter
            {"text": "10⁰", "value": 1.0, "multiplier": 0},         # meter
            # {"text": "10¹", "value": 1e1, "multiplier": 1},       # dekameter
            # {"text": "10²", "value": 1e2, "multiplier": 2},       # hectometer
            {"text": "10³", "value": 1e3, "multiplier": 3},         # kilometer
            {"text": "10⁶", "value": 1e6, "multiplier": 6},         # megameter
            {"text": "10⁹", "value": 1e9, "multiplier": 9},         # gigameter
            {"text": "10¹²", "value": 1e12, "multiplier": 12},      # terameter
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        if role == MetricsModel.TextRole:
            return item["text"]
        elif role == MetricsModel.ValueRole:
            return item["value"]
        elif role == MetricsModel.MultiplierRole:
            return item["multiplier"]

        return None

    def roleNames(self):
        return {
            MetricsModel.TextRole: b"text",
            MetricsModel.ValueRole: b"value",
            MetricsModel.MultiplierRole: b"multiplier",
        }
