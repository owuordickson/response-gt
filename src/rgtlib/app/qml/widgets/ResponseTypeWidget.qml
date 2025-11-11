import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: responseTypeWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: false
    visible: networkController.display_image()


    Text {
        text: "Response Types"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }



    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
        }
    }

}