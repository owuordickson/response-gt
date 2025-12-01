import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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


    Text {
        text: "Response Types"
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
                    var index = rgtACParams.index(0, 0);
                    rgtACParams.setData(index, val, valueRole);
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
        }


        RadioButton {
            id: rdoDynamic
            text: "Dynamic"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this
        }
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
            responseTypeWidget.visible = networkController.graph_data_uploaded();
            responseTypeWidget.enabled = networkController.graph_data_uploaded();
            initializeSelections();
        }
    }

}