import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: imposedNodesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: false
    visible: networkController.graph_is_ready()

    Text {
        text: "Imposed Vertices"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }



    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            imposedNodesWidget.visible = false//networkController.graph_is_ready();
        }
    }

}