import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs as QuickDialogs

QuickDialogs.FileDialog {
    id: graphFileDialog
    title: "Open file"
    nameFilters: [networkController.get_file_extensions()]
    onAccepted: networkController.upload_edge_list(graphFileDialog.selectedFile)
}