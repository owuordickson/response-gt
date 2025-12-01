import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: imposedNodesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 120
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()

    property int rdoWidthSize: 75
    property int cbWidthSize: 180

    Text {
        text: "Imposed Vertices"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    ColumnLayout {
        Layout.alignment: Qt.AlignVCenter

        ButtonGroup {
            id: btnGrpType
            property bool currentCheckedButton: rdoDefault
            exclusive: true
            checkedButton: rdoDefault
            onCheckedButtonChanged: {
                if (currentCheckedButton !== checkedButton) {
                    currentCheckedButton = checkedButton;
                    if (checkedButton === rdoDefault) {
                        cbDirection.enabled = true;
                        txtVerts.enabled = false;
                        rectVerts.border.width = 0;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoCustom) {
                        cbDirection.enabled = false;
                        txtVerts.enabled = true;
                        rectVerts.border.width = 1;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoFile) {
                        cbDirection.enabled = false;
                        txtVerts.enabled = false;
                        rectVerts.border.width = 0;
                        btnUpload.enabled = true;
                    }
                }
            }
        }


        RowLayout {

            RadioButton {
                id: rdoDefault
                text: "Default"
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this
            }

            ComboBox {
                id: cbDirection
                Layout.minimumWidth: cbWidthSize
            }
        }


        RowLayout {

            RadioButton {
                id: rdoCustom
                text: "Custom"
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this
            }

            Rectangle {
                id: rectVerts
                //width: cbWidthSize
                Layout.minimumWidth: cbWidthSize
                height: 48
                color: "transparent"
                border.width: 1
                border.color: "#808080"
                radius: 4

                TextArea {
                    id: txtVerts
                    anchors.fill: parent
                    anchors.margins: 2
                    wrapMode: TextArea.Wrap
                    font.pixelSize: 9
                    placeholderText: "vertex positions separated by comma..."
                    //enabled: false
                }
            }
        }


        RowLayout {

            RadioButton {
                id: rdoFile
                text: "File: "
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this
            }

            Button {
                id: btnUpload
                text: "Upload"
                enabled: false
            }
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            imposedNodesWidget.visible = networkController.graph_data_uploaded();
        }
    }

}