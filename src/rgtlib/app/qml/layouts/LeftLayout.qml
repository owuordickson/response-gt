import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0
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
            visible: !networkController.graph_data_uploaded()
        }


        ResponseTypeWidget{}


        ResponsePropertyWidget{}


        ListPropertyWidget{}


        ImposedNodesWidget{}

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            lblNoNetwork.visible = !networkController.graph_data_uploaded();

            /*if (networkController.graph_data_uploaded()) {
                lblNoNetwork.text = "No graph network to show!\nRun 'Compute Response'.";
            } else {
                lblNoNetwork.text = "No graph network to show!\nUpload CSV files of vertex/node\n positions and edge list.";
            }*/
        }
    }

}
