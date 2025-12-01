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
                    //var val = checkedButton === rdoDefault ? 0 : 1;
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
                //width: cbWidthSize
                Layout.minimumWidth: cbWidthSize
                height: 48


                TextArea {
                    id: txtVerts
                    anchors.fill: parent
                    wrapMode: TextArea.Wrap
                    font.pixelSize: 9
                    placeholderText: "vertex positions separated by comma..."
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
                text: "Upload"
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