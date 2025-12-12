import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs as QuickDialogs
import Theme 1.0

QuickDialogs.FileDialog {
    id: fileDialog

    // ---------- PARAMETERS (passed from caller) ----------
    property string file_type: ""   // "edges" or "vertices" or "parameters" etc.
    property var controller         // can be networkController or any controller

    // Default props
    title: "Open file"
    nameFilters: [controller ? controller.get_file_extensions() : "*"]

    onAccepted: {
        if ((!controller) || (file_type === "")) return;
        controller.upload_file_data(fileDialog.selectedFile, file_type);
    }
}
