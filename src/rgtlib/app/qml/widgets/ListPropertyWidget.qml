import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: listResponsePropWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 56
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    visible: networkController.graph_data_uploaded()

    property int lblWidthSize: 75
    property int cbWidthSize: 125

    Text {
        text: "Response Properties"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    RowLayout {
        Layout.alignment: Qt.AlignVCenter

        Label {
            Layout.preferredWidth: lblWidthSize
            text: "File: "
        }

        ComboBox {
            Layout.minimumWidth: cbWidthSize
        }

        Button {
            id: btnListUpload
            text: "Upload"
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            listResponsePropWidget.visible = networkController.graph_data_uploaded();
        }
    }

}