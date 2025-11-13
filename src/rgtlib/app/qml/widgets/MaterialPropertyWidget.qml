import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: materialPropertyWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: false
    visible: networkController.graph_is_ready()

    Text {
        text: "Material Properties"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }



    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            materialPropertyWidget.visible = false//networkController.graph_is_ready();
        }
    }

}