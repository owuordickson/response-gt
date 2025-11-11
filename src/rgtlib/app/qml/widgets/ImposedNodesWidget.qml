import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: imposedNodesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    visible: true

    Text {
        text: "Imposed Vertices"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }



    Connections {
        //target:
    }

}