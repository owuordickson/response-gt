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
    property int cmbWidthSize: 180

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
                        cmbDirection.enabled = true;
                        taVerts.enabled = false;
                        rectVerts.border.width = 0;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoCustom) {
                        cmbDirection.enabled = false;
                        taVerts.enabled = true;
                        rectVerts.border.width = 1;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoFile) {
                        cmbDirection.enabled = false;
                        taVerts.enabled = false;
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
                id: cmbDirection
                Layout.minimumWidth: cmbWidthSize
                model: [
                    "Top-Bottom",
                    "Left-Right"
                ]
                currentIndex: 0

                // Fires only when the user selects a new option
                onActivated: (index) => {
                    let resp_direction = cmbDirection.model[index];
                    networkController.apply_imposed_vertices("default", resp_direction);
                }
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
                //width: cmbWidthSize
                Layout.minimumWidth: cmbWidthSize
                height: 48
                color: "transparent"
                border.width: 1
                border.color: "#808080"
                radius: 4

                Flickable {
                    id: flickable
                    anchors.fill: parent
                    anchors.margins: 2
                    contentWidth: parent.width // Important for vertical-only scrolling
                    contentHeight: taVerts.implicitHeight

                    TextArea.flickable: TextArea {
                        id: taVerts
                        width: flickable.width // Ensure TextArea fills Flickable's width
                        wrapMode: TextArea.Wrap
                        font.pixelSize: 9
                        placeholderText: "enter vertex positions or copy/paste..."

                        // When focus leaves the TextArea
                        onEditingFinished: {
                            // Add your custom logic here
                            networkController.apply_imposed_vertices("custom", taVerts.text);
                        }

                        // Trigger when Enter is pressed
                        Keys.onReturnPressed: (event) => {
                            // Prevent new line
                            event.accepted = true

                            // Manually trigger the finish event
                            taVerts.editingFinished()  // Requires Qt 6.6+
                        }
                    }

                    ScrollBar.vertical: ScrollBar { // Attach vertical scrollbar
                        parent: flickable
                        policy: ScrollBar.AsNeeded // Show scrollbar only when needed
                    }

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
                onClicked: {
                    dlgFileData.file_type = "imposed_vertices";
                    dlgFileData.open();
                }
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