import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: responseTypeWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: false//!imageController.display_image()
    visible: true


    Text {
        text: "Response Types"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }



    Connections {
        //target:
    }

}