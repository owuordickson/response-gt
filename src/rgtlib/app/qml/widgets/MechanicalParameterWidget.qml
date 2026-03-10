import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    Layout.leftMargin: 10
    Layout.preferredHeight: 150
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter | Qt.AlignTop
    visible: false

    property int dirValueRole: Qt.UserRole + 4
    property int lblWidthSize: 120
    property int cmbWidthSize: 150
    property int taWidthSize: 150

    Label {
        text: "Response Parameters"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {

        Label {
            Layout.preferredWidth: lblWidthSize
            text: "Pinned Direction:"
            font.pixelSize: 11
            color: Theme.blue
        }

        ComboBox {
            id: cmbPinnedDirection
            Layout.minimumWidth: cmbWidthSize
            model: rgtPinnedDirections
            textRole: "text"
            currentIndex: 0

            // Fires only when the user selects a new option
            onActivated: (index) => {
                // Update all to 0, only current to 1
                for (let i = 0; i < rgtPinnedDirections.rowCount(); ++i) {
                    let val = i === index ? 1 : 0;
                    let idx = rgtPinnedDirections.index(i, 0);
                    rgtPinnedDirections.setData(idx, val, dirValueRole);
                }
            }
        }

    }


    RowLayout {

        Label {
            Layout.preferredWidth: lblWidthSize
            text: "Displacement Direction:"
            font.pixelSize: 11
            color: Theme.blue
        }

        ComboBox {
            id: cmbDisplacedDirection
            Layout.minimumWidth: cmbWidthSize
            model: rgtDisplacedDirections
            textRole: "text"
            currentIndex: 1

            // Fires only when the user selects a new option
            onActivated: (index) => {
                // Update all to 0, only current to 1
                for (let i = 0; i < rgtDisplacedDirections.rowCount(); ++i) {
                    let val = i === index ? 1 : 0;
                    let idx = rgtDisplacedDirections.index(i, 0);
                    rgtDisplacedDirections.setData(idx, val, dirValueRole);
                }
            }
        }

    }

    RowLayout {

        Label {
            Layout.preferredWidth: lblWidthSize
            text: "Displacement Vector:"
            font.pixelSize: 11
            color: Theme.blue
        }

        Rectangle {
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
                contentHeight: taDispVec.implicitHeight

                TextArea.flickable: TextArea {
                    id: taDispVec
                    width: flickable.width // Ensure TextArea fills Flickable's width
                    wrapMode: TextArea.Wrap
                    font.pixelSize: 9
                    placeholderText: "Type/paste displacement vector. Format: [val, val] -> [20, -1]"

                    // Access the internal Text item used for the placeholder and bind its wrapMode
                    property Text placeholderTextItem: children.length > 0 ? children[0] : null

                    Binding {
                        when: taDispVec.placeholderTextItem !== null
                        target: taDispVec.placeholderTextItem
                        property: "wrapMode"
                        value: Text.WordWrap
                    }

                    Binding {
                        when: taDispVec.placeholderTextItem !== null
                        target: taDispVec.placeholderTextItem
                        property: "width"
                        value: taDispVec.width - taDispVec.leftPadding - taDispVec.rightPadding
                    }

                    // When focus leaves the TextArea
                    onEditingFinished: {
                        // Add your custom logic here
                        networkController.apply_displacement_vector(taDispVec.text);
                    }

                    // Trigger when Enter is pressed
                    Keys.onReturnPressed: (event) => {
                        // Prevent new line
                        event.accepted = true

                        // Manually trigger the finish event
                        taDispVec.editingFinished()  // Requires Qt 6.6+
                    }
                }

                ScrollBar.vertical: ScrollBar { // Attach vertical scrollbar
                    parent: flickable
                    policy: ScrollBar.AsNeeded // Show scrollbar only when needed
                }

            }
        }
    }

}