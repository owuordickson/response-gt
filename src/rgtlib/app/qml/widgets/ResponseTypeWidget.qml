import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    id: responseTypeWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 56
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: networkController.graph_data_uploaded()
    visible: networkController.graph_data_uploaded()

    property int idRole: Qt.UserRole + 1
    property int valueRole: Qt.UserRole + 4
    property int rdoWidthSize: 75


    Label {
        text: "Response Types"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    RowLayout {
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter


        ButtonGroup {
            id: btnGrpType
            property bool currentCheckedButton: rdoStatic
            exclusive: true
            onCheckedButtonChanged: {
                if (currentCheckedButton !== checkedButton) {
                    currentCheckedButton = checkedButton;
                    var val = checkedButton === rdoStatic ? 0 : 1;
                    var index = rgtOptions.index(0, 0);
                    rgtOptions.setData(index, val, valueRole);
                    networkController.apply_changes();
                }
            }
        }


        RadioButton {
            id: rdoStatic
            text: "Static"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this

            indicator: Rectangle {
                width: 14
                height: 14
                radius: 7
                y: (rdoStatic.height - height) / 2   // center vertically
                border.color: rdoStatic.checked ? Theme.dodgerBlue : Theme.text
                border.width: 2
                color: "transparent"

                Rectangle {
                    visible: rdoStatic.checked
                    width: 8
                    height: 8
                    radius: 4
                    anchors.centerIn: parent
                    color: Theme.darkGray
                }
            }
            contentItem: Label {
                text: rdoStatic.text
                font: rdoStatic.font
                color: Theme.text
                verticalAlignment: Text.AlignVCenter
                leftPadding: rdoStatic.indicator.width + 6
            }
        }


        RadioButton {
            id: rdoDynamic
            text: "Dynamic"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this

            indicator: Rectangle {
                width: 14
                height: 14
                radius: 7
                y: (rdoDynamic.height - height) / 2   // center vertically
                border.color: rdoDynamic.checked ? Theme.dodgerBlue : Theme.text
                border.width: 2
                color: "transparent"

                Rectangle {
                    visible: rdoDynamic.checked
                    width: 8
                    height: 8
                    radius: 4
                    anchors.centerIn: parent
                    color: Theme.darkGray
                }
            }
            contentItem: Label {
                text: rdoDynamic.text
                font: rdoDynamic.font
                color: Theme.text
                verticalAlignment: Text.AlignVCenter
                leftPadding: rdoDynamic.indicator.width + 6
            }
        }
    }


    function initializeSelections() {
        for (let row = 0; row < rgtOptions.rowCount(); row++) {
            let index = rgtOptions.index(row, 0);
            let item_id = rgtOptions.data(index, idRole);  // IdRole
            let item_val = rgtOptions.data(index, valueRole); // ValueRole

            if (item_id === "response_type") {
                btnGrpType.checkedButton = item_val === 0 ? rdoStatic : rdoDynamic;
            }
        }
    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            responseTypeWidget.visible = networkController.graph_data_uploaded();
            responseTypeWidget.enabled = networkController.graph_data_uploaded();
            initializeSelections();
        }
    }

}