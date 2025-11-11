import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../widgets"

Rectangle {
    width: parent.width
    height: parent.height
    radius: 10
    color: "#f0f0f0"
    border.color: "#c0c0c0"

    ColumnLayout {
        anchors.fill: parent

        Label {
            id: lblNoNetwork
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            text: "No graph network to show!\nUpload CSV files of vertex/node\n positions and edge list."
            color: "#808080"
            visible: !mainController.display_image()
        }


        ResponseTypeWidget{}


        ImposedNodesWidget{}


        MaterialPropertyWidget{}

    }


    Connections {
        target: mainController

        function onImageChangedSignal() {
            // Force refresh
            lblNoNetwork.visible = !mainController.display_image();
        }
    }

}
