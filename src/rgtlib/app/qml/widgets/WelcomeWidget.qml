import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material as Material
import Theme 1.0

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
            color: Theme.blue
            //font.bold: true
            font.pixelSize: 19
        }

        Label {
            id: lblQuick
            //Layout.leftMargin: 5
            Layout.alignment: Qt.AlignHCenter
            text: "Upload your graph network"
            color: Theme.darkGrey
            font.bold: true
            font.pixelSize: 14
        }

        RowLayout {
            id: rowUploadButtons
            Layout.alignment: Qt.AlignHCenter
            visible: true

            Material.Button {
                id: btnAddNodes
                Layout.preferredWidth: 135
                //Layout.preferredHeight: 32
                text: "Vertex positions"
                enabled: networkController.enable_vertex_positions_upload()
                onClicked: {
                    dlgFileData.file_type = "vertices";
                    dlgFileData.open();
                }
            }

            Material.Button {
                id: btnAddEdges
                Layout.preferredWidth: 115
                //Layout.preferredHeight: 32
                text: "Edge list"
                enabled: networkController.enable_edge_list_upload()
                onClicked: {
                    dlgFileData.file_type = "edges";
                    dlgFileData.open();
                }
            }
        }

        RowLayout {
            id: rowResponseTypes
            Layout.alignment: Qt.AlignHCenter
            visible: false
        }

        RowLayout {
            id: rowAnalyzerButtons
            Layout.alignment: Qt.AlignHCenter
            visible: false

            Material.Button {
                id: btnRunAnalyzer
                //Layout.preferredWidth: 135
                text: "Compute Response"
                onClicked: networkController.run_response_analyzer()
            }
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            welcomeContainer.visible = !networkController.graph_is_ready();
            rowUploadButtons.visible = !networkController.graph_data_uploaded();
            rowAnalyzerButtons.visible = networkController.graph_data_uploaded();
            rowResponseType.visible = networkController.graph_data_uploaded();

            btnAddNodes.enabled = networkController.enable_vertex_positions_upload();
            btnAddEdges.enabled = networkController.enable_edge_list_upload();

            if (networkController.graph_data_uploaded()) {
                lblQuick.text = "Graph data saved";
            } else {
                lblQuick.text = "Upload your graph network";
            }
        }

    }

}