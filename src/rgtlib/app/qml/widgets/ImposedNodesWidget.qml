import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: imposedNodesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 100
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    visible: networkController.graph_data_uploaded()

    property int rdoWidthSize: 75

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
            onCheckedButtonChanged: {
                if (currentCheckedButton !== checkedButton) {
                    currentCheckedButton = checkedButton;
                    //var val = checkedButton === rdoDefault ? 0 : 1;
                }
            }
        }

        RadioButton {
            id: rdoDefault
            text: "Default"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this
        }

        RadioButton {
            id: rdoCustom
            text: "Custom"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this
        }


        RadioButton {
            id: rdoFile
            text: "File"
            Layout.preferredWidth: rdoWidthSize
            ButtonGroup.group: btnGrpType
            onClicked: btnGrpType.checkedButton = this
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