import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: responseTypeWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 75
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: networkController.graph_is_ready()
    visible: networkController.graph_is_ready()

    property int idRole: Qt.UserRole + 1
    property int valueRole: Qt.UserRole + 4
    property int btnWidthSize: 100

    ButtonGroup {
        id: btnGrpType
        property bool currentCheckedButton: rdoStatic
        property bool clickedChange: false
        exclusive: true
        onCheckedButtonChanged: {
            if (clickedChange) {
                clickedChange = false
                return
            }

            if (currentCheckedButton !== checkedButton) {
                currentCheckedButton = checkedButton;
                var val = checkedButton === rdoStatic ? 0 : 1;
                var index = rgtACParams.index(0, 0);
                rgtACParams.setData(index, val, valueRole);
                networkController.apply_changes();
            }
        }
        onClicked: {
            clickedChange = true;
            currentCheckedButton = checkedButton;
            var val = checkedButton === rdoStatic ? 0 : 1;
            var index = rgtACParams.index(0, 0);
            rgtACParams.setData(index, val, valueRole);
            networkController.apply_changes();
        }
    }


    Text {
        text: "Response Types"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    RadioButton {
        id: rdoStatic
        text: "Static"
        Layout.preferredWidth: btnWidthSize
        ButtonGroup.group: btnGrpType
        onClicked: btnGrpType.checkedButton = this
    }


    RadioButton {
        id: rdoDynamic
        text: "Dynamic"
        Layout.preferredWidth: btnWidthSize
        ButtonGroup.group: btnGrpType
        onClicked: btnGrpType.checkedButton = this
    }


    function initializeSelections() {
        for (let row = 0; row < rgtACParams.rowCount(); row++) {
            var index = rgtACParams.index(row, 0);
            let item_id = rgtACParams.data(index, idRole);  // IdRole
            let item_val = rgtACParams.data(index, valueRole); // ValueRole

            if (item_id === "response_type") {
                btnGrpType.checkedButton = item_val === 0 ? rdoStatic : rdoDynamic;
            }
        }
    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            responseTypeWidget.visible = networkController.graph_is_ready();
            responseTypeWidget.enabled = networkController.graph_is_ready();
            initializeSelections();
        }
    }

}