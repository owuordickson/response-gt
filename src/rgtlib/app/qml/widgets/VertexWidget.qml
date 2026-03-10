import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    Layout.leftMargin: 10
    Layout.preferredHeight: 50
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: false

    Label {
        text: "Vertex Parameters"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }

}