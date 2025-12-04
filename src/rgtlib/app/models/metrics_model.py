from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex


class MetricsModel(QAbstractListModel):
    #IdRole = Qt.ItemDataRole.UserRole + 1
    TextRole = Qt.ItemDataRole.UserRole + 3
    ValueRole = Qt.ItemDataRole.UserRole + 4
    MultiplierRole = Qt.ItemDataRole.UserRole + 12

    def __init__(self, lst_data: list, parent=None):
        super().__init__(parent)
        self._items = lst_data

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        #if role == MetricsModel.IdRole:
        #    return item["id"]
        if role == MetricsModel.TextRole:
            return item["text"]
        elif role == MetricsModel.ValueRole:
            return item["value"]
        elif role == MetricsModel.MultiplierRole:
            return item["multiplier"]
        return None

    """def reset_data(self, new_data):
        self.beginResetModel()
        self._items = new_data
        self.endResetModel()
        self.dataChanged.emit(self.index(0,0), self.index(len(new_data), 0),
                              [MetricsModel.TextRole, MetricsModel.ValueRole, MetricsModel.MultiplierRole])"""

    def roleNames(self):
        return {
            #MetricsModel.IdRole: b"id",
            MetricsModel.TextRole: b"text",
            MetricsModel.ValueRole: b"value",
            MetricsModel.MultiplierRole: b"multiplier",
        }
