import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    id: uploadedFilesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 50
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()



    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            uploadedFilesWidget.visible = networkController.graph_data_uploaded();
        }
    }

}