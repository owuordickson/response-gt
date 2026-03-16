import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic as Basic
import QtQuick.Controls.Imagine as Imagine
import Theme 1.0

ColumnLayout {
    Layout.leftMargin: 10
    Layout.preferredHeight: 210
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: false

    property int dirValueRole: Qt.UserRole + 4
    property int lblWidthSize: 90
    property int rdoWidthSize: 75
    property int spbWidthSize: 95
    property int cmbWidthSize: 125
    property int taWidthSize: 190

    Label {
        text: "Impose Potential"
        color: Theme.text
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
                    networkController.remove_data("given_potential_list");
                    networkController.remove_data("vertex_list");
                    currentCheckedButton = checkedButton;
                    if (checkedButton === rdoDefault) {
                        colDefault.enabled = true;
                        taVerts.enabled = false;
                        rectVerts.border.width = 0;
                        rowFile.enabled = false;
                    } else if (checkedButton === rdoCustom) {
                        networkController.apply_imposed_vertices("Custom", taVerts.text);
                        colDefault.enabled = false;
                        taVerts.enabled = true;
                        rectVerts.border.width = 1;
                        rowFile.enabled = false;
                    } else if (checkedButton === rdoFile) {
                        colDefault.enabled = false;
                        taVerts.enabled = false;
                        rectVerts.border.width = 0;
                        rowFile.enabled = true;
                    }
                }
            }
        }


        RowLayout {

            Basic.RadioButton {
                id: rdoDefault
                text: "Default"
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this

                indicator: Rectangle {
                    width: 14
                    height: 14
                    radius: 7
                    y: (rdoDefault.height - height) / 2   // center vertically
                    border.color: rdoDefault.checked ? Theme.dodgerBlue : Theme.text
                    border.width: 2
                    color: "transparent"

                    Rectangle {
                        visible: rdoDefault.checked
                        width: 8
                        height: 8
                        radius: 4
                        anchors.centerIn: parent
                        color: Theme.darkGray
                    }
                }
                contentItem: Label {
                    text: rdoDefault.text
                    font: rdoDefault.font
                    color: Theme.text
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: rdoDefault.indicator.width + 6
                }
            }

            ColumnLayout {
                id: colDefault

                Repeater {
                    model: rgtPotentialOptions
                    Loader {
                        active: model.visible === 1   // <-- Only create the delegate if visible

                        sourceComponent: RowLayout {
                            Layout.fillWidth: true
                            Layout.alignment: Qt.AlignLeft
                            property int mainIndex: index
                            visible: model.visible === 1

                            Label {
                                Layout.preferredWidth: lblWidthSize
                                text: model.text + (model.id === 'selected_vertex_proportion' ? "\nwith Imposed Potential" : "")
                                font.pixelSize: 9
                                color: Theme.blue
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
                                    rgtPotentialOptions.setData(index, val, dirValueRole);
                                    //networkController.;
                                }
                            }

                        }
                    }
                }


                RowLayout {

                    Label {
                        Layout.preferredWidth: lblWidthSize
                        text: "Potential Direction"
                        font.pixelSize: 9
                        color: Theme.blue
                    }

                    ComboBox {
                        id: cmbDirection
                        Layout.minimumWidth: spbWidthSize
                        model: rgtPotentialDirections
                        textRole: "text"
                        currentIndex: 0

                        // Fires only when the user selects a new option
                        onActivated: (index) => {
                            // Update all to 0, only current to 1
                            for (let i = 0; i < rgtPotentialDirections.rowCount(); ++i) {
                                let val = i === index ? 1 : 0;
                                let idx = rgtPotentialDirections.index(i, 0);
                                rgtPotentialDirections.setData(idx, val, dirValueRole);
                            }
                        }
                    }

                }

            }

        }


        RowLayout {

            Basic.RadioButton {
                id: rdoCustom
                text: "Custom"
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this

                indicator: Rectangle {
                    width: 14
                    height: 14
                    radius: 7
                    y: (rdoCustom.height - height) / 2   // center vertically
                    border.color: rdoCustom.checked ? Theme.dodgerBlue : Theme.text
                    border.width: 2
                    color: "transparent"

                    Rectangle {
                        visible: rdoCustom.checked
                        width: 8
                        height: 8
                        radius: 4
                        anchors.centerIn: parent
                        color: Theme.darkGray
                    }
                }
                contentItem: Label {
                    text: rdoCustom.text
                    font: rdoCustom.font
                    color: Theme.text
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: rdoCustom.indicator.width + 6
                }
            }

            Rectangle {
                id: rectVerts
                //width: taWidthSize
                Layout.minimumWidth: taWidthSize
                height: 48
                color: "transparent"
                border.width: 1
                border.color: Theme.darkGrey
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
                        placeholderText: "Type/paste vertex positions and their corresponding potentials. Format: [position, potential] -> [30, 1], [20, -1]"

                        // Access the internal Text item used for the placeholder and bind its wrapMode
                        property Text placeholderTextItem: children.length > 0 ? children[0] : null

                        Binding {
                            when: taVerts.placeholderTextItem !== null
                            target: taVerts.placeholderTextItem
                            property: "wrapMode"
                            value: Text.WordWrap
                        }

                        Binding {
                            when: taVerts.placeholderTextItem !== null
                            target: taVerts.placeholderTextItem
                            property: "width"
                            value: taVerts.width - taVerts.leftPadding - taVerts.rightPadding
                        }

                        // When focus leaves the TextArea
                        onEditingFinished: {
                            // Add your custom logic here
                            networkController.apply_imposed_vertices("Custom", taVerts.text);
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

            Basic.RadioButton {
                id: rdoFile
                text: "File "
                Layout.preferredWidth: rdoWidthSize
                ButtonGroup.group: btnGrpType
                onClicked: btnGrpType.checkedButton = this

                indicator: Rectangle {
                    width: 14
                    height: 14
                    radius: 7
                    y: (rdoFile.height - height) / 2   // center vertically
                    border.color: rdoFile.checked ? Theme.dodgerBlue : Theme.text
                    border.width: 2
                    color: "transparent"

                    Rectangle {
                        visible: rdoFile.checked
                        width: 8
                        height: 8
                        radius: 4
                        anchors.centerIn: parent
                        color: Theme.darkGray
                    }
                }
                contentItem: Label {
                    text: rdoFile.text
                    font: rdoFile.font
                    color: Theme.text
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: rdoFile.indicator.width + 6
                }
            }

            RowLayout {
                id: rowFile

                ComboBox {
                    id: cmbPotentialList
                    Layout.minimumWidth: cmbWidthSize
                    model: [
                        "Potential List",
                        "Vertex List"
                    ]
                    currentIndex: 0
                }

                Imagine.Button {
                    id: btnPotentialUpload
                    text: "Upload"
                    onClicked: {
                        let file_desc = cmbPotentialList.model[cmbPotentialList.currentIndex];
                        dlgFileData.file_type = file_desc;
                        dlgFileData.open();
                    }
                }

            }
        }

    }


}