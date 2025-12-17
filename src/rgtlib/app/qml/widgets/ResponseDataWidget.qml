import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Imagine as Imagine
import Theme 1.0

ColumnLayout {
    id: listResponsePropWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 56
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()

    property int lblWidthSize: 50
    property int cmbWidthSize: 125

    Label {
        text: "Response Data"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    RowLayout {
        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter

        Label {
            color: Theme.text
            Layout.preferredWidth: lblWidthSize
            text: "File: "
        }

        ComboBox {
            id: cmbResponseList
            Layout.minimumWidth: cmbWidthSize
            model: [
                "Resistivity List",
                "Inductance List",
                "Capacitance List",
                "Leak Resistance List"
            ]
            currentIndex: 0
        }

        Imagine.Button {
            id: btnListUpload
            text: "Upload"
            onClicked: {
                let file_desc = cmbResponseList.model[cmbResponseList.currentIndex];
                dlgFileData.file_type = file_desc;
                dlgFileData.open();
            }
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