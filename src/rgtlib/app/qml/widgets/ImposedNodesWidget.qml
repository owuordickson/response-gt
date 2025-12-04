import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: imposedNodesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 210
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()

    property int valueRole: Qt.UserRole + 4
    property int lblWidthSize: 100
    property int rdoWidthSize: 75
    property int spbWidthSize: 75
    property int cmbWidthSize: 180

    Text {
        text: "Impose Potential"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    ColumnLayout {
        Layout.alignment: Qt.AlignVCenter
        spacing: 10

        ButtonGroup {
            id: btnGrpType
            property bool currentCheckedButton: rdoDefault
            exclusive: true
            checkedButton: rdoDefault
            onCheckedButtonChanged: {
                if (currentCheckedButton !== checkedButton) {
                    currentCheckedButton = checkedButton;
                    if (checkedButton === rdoDefault) {
                        colDefault.enabled = true;
                        taVerts.enabled = false;
                        rectVerts.border.width = 0;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoCustom) {
                        colDefault.enabled = false;
                        taVerts.enabled = true;
                        rectVerts.border.width = 1;
                        btnUpload.enabled = false;
                    } else if (checkedButton === rdoFile) {
                        colDefault.enabled = false;
                        taVerts.enabled = false;
                        rectVerts.border.width = 0;
                        btnUpload.enabled = true;
                    }
                }
            }
        }


        RowLayout {

            Label {
                text: "Direction:"
                Layout.preferredWidth: rdoWidthSize
            }

            ComboBox {
                id: cmbDirection
                Layout.minimumWidth: cmbWidthSize
                model: [
                    "Top-Bottom",
                    "Bottom-Top",
                    "Left-Right",
                    "Right-Left"
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
                id: rdoDefault
                text: "Default"
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this
            }

            ColumnLayout {
                id: colDefault

                Repeater {
                    model: rgtPotentialOptions
                    delegate: RowLayout {
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignLeft
                        property int mainIndex: index
                        visible: model.visible === 1

                        Label {
                            Layout.preferredWidth: lblWidthSize
                            text: model.text
                            font.pixelSize: 10
                            color: "#2266ff"
                        }

                        SpinBox {
                            id: spinbox
                            Layout.preferredWidth: spbWidthSize

                            // Model values are floats (e.g., 0.00123)
                            property real realMin: model.minValue
                            property real realMax: model.maxValue
                            property real realStep: 0.01             // or 1
                            property real realValue: model.value    // actual decimal

                            // SpinBox INTERNAL integer range
                            from: 0
                            to: Math.round((realMax - realMin) / realStep)
                            // Map realValue → SpinBox integer
                            value: Math.round((realValue - realMin) / realStep)
                            // Convert SpinBox integer → real value (displayed)
                            textFromValue: function (v) {
                                return Number(realMin + v * realStep).toFixed(2)   // format as 2 decimals
                            }

                            // Convert text → integer value
                            valueFromText: function (txt) {
                                let r = Number(txt)
                                return Math.round((r - realMin) / realStep)
                            }

                            onValueChanged: {
                                realValue = realMin + value * realStep
                                updateValue(realValue)      // ← your real update method
                            }
                        }

                        function updateValue(val) {
                            if (model.value !== val) {
                                const index = rgtPotentialOptions.index(mainIndex, 0);
                                rgtPotentialOptions.setData(index, val, valueRole);
                                //networkController.;
                            }
                        }

                    }
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
                        placeholderText: "enter/paste potentials and positions"

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