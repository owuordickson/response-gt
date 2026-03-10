import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic as Basic
import Theme 1.0


RowLayout {
    id: responseTypeWidget
    //Layout.leftMargin: 10
    //Layout.preferredHeight: 36
    Layout.preferredWidth: 175
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
    visible: false

    property int idRole: Qt.UserRole + 1
    property int valueRole: Qt.UserRole + 4
    property int rdoWidthSize: 75


    ButtonGroup {
        id: btnGrpResponseType
        property bool currentCheckedButton: rdoElectrical
        exclusive: true
        onCheckedButtonChanged: {
            if (currentCheckedButton !== checkedButton) {
                currentCheckedButton = checkedButton;
                var val = checkedButton === rdoElectrical ? 0 : 1;
                var index = rgtResponseOptions.index(0, 0);
                rgtResponseOptions.setData(index, val, valueRole);
                networkController.toggle_response_type();
            }
        }
    }


    Basic.RadioButton {
        id: rdoElectrical
        text: "Electrical"
        Layout.preferredWidth: rdoWidthSize
        ButtonGroup.group: btnGrpResponseType
        onClicked: btnGrpResponseType.checkedButton = this

        indicator: Rectangle {
            width: 14
            height: 14
            radius: 7
            y: (rdoElectrical.height - height) / 2   // center vertically
            border.color: rdoElectrical.checked ? Theme.dodgerBlue : Theme.text
            border.width: 2
            color: "transparent"

            Rectangle {
                visible: rdoElectrical.checked
                width: 8
                height: 8
                radius: 4
                anchors.centerIn: parent
                color: Theme.darkGray
            }
        }
        contentItem: Label {
            text: rdoElectrical.text
            font: rdoElectrical.font
            color: Theme.text
            verticalAlignment: Text.AlignVCenter
            leftPadding: rdoElectrical.indicator.width + 6
        }
    }


    Basic.RadioButton {
        id: rdoMechanical
        text: "Mechanical"
        Layout.preferredWidth: rdoWidthSize
        ButtonGroup.group: btnGrpResponseType
        onClicked: btnGrpResponseType.checkedButton = this

        indicator: Rectangle {
            width: 14
            height: 14
            radius: 7
            y: (rdoMechanical.height - height) / 2   // center vertically
            border.color: rdoMechanical.checked ? Theme.dodgerBlue : Theme.text
            border.width: 2
            color: "transparent"

            Rectangle {
                visible: rdoMechanical.checked
                width: 8
                height: 8
                radius: 4
                anchors.centerIn: parent
                color: Theme.darkGray
            }
        }
        contentItem: Label {
            text: rdoMechanical.text
            font: rdoMechanical.font
            color: Theme.text
            verticalAlignment: Text.AlignVCenter
            leftPadding: rdoMechanical.indicator.width + 6
        }
    }


    function initializeSelections() {
        for (let row = 0; row < rgtResponseOptions.rowCount(); row++) {
            let index = rgtResponseOptions.index(row, 0);
            let item_id = rgtResponseOptions.data(index, idRole);  // IdRole
            let item_val = rgtResponseOptions.data(index, valueRole); // ValueRole

            if (item_id === "response_type") {
                btnGrpResponseType.checkedButton = item_val === 0 ? rdoElectrical : rdoMechanical;
            }
        }
    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            responseTypeWidget.visible = networkController.graph_data_uploaded();
            initializeSelections();
        }
    }

}

