import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material as Material

Rectangle {
    id: welcomeContainer
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "transparent"
    visible: !networkController.graph_is_ready()

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 5

        Label {
            id: lblWelcome
            Layout.alignment: Qt.AlignHCenter
            text: "ResponseGT"
            color: "#2266ff"
            //font.bold: true
            font.pixelSize: 19
        }

        Label {
            id: lblQuick
            //Layout.leftMargin: 5
            Layout.alignment: Qt.AlignHCenter
            text: "Upload your graph network"
            color: "#808080"
            font.bold: true
            font.pixelSize: 14
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter

            Material.Button {
                id: btnAddNodes
                Layout.preferredWidth: 135
                //Layout.preferredHeight: 32
                text: "Vertex positions"
                enabled: networkController.enable_vertex_positions_upload()
                onClicked: dlgFileVertices.open()
            }

            Material.Button {
                id: btnAddEdges
                Layout.preferredWidth: 115
                //Layout.preferredHeight: 32
                text: "Edge list"
                enabled: networkController.enable_edge_list_upload()
                onClicked: dlgFileEdges.open()
            }

        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            welcomeContainer.visible = !networkController.graph_is_ready();
            btnAddNodes.enabled = networkController.enable_vertex_positions_upload();
            btnAddEdges.enabled = networkController.enable_edge_list_upload();
        }

    }

}