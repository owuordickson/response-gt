import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0
import "../widgets"

Rectangle {
    width: parent.width
    height: parent.height
    radius: 10
    color: Theme.background
    border.color: Theme.gray

    ColumnLayout {
        anchors.fill: parent

        Label {
            id: lblNoNetwork
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            text: "No graph network to show!\nUpload CSV files of vertex/node\n positions and edge list."
            color: Theme.darkGrey
            visible: !networkController.graph_data_uploaded()
        }


        UploadedFilesWidget{id: uploadedFilesWidget}


        ResponseParameterWidget{id: elecParamWidget}


        ResponseDataWidget{id: elecDataWidget}


        ImposedNodesWidget{id: elecImposedPotentialsWidget}

        MechanicalParameterWidget{id: mechanicalParamWidget}

        VertexWidget{id: vertexWidget}

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            lblNoNetwork.visible = !networkController.graph_data_uploaded();
            uploadedFilesWidget.visible = networkController.graph_data_uploaded();
            elecParamWidget.visible = networkController.graph_data_uploaded() && networkController.is_electrical_response();
            elecDataWidget.visible = networkController.graph_data_uploaded() && networkController.is_electrical_response();
            elecImposedPotentialsWidget.visible = networkController.graph_data_uploaded() && networkController.is_electrical_response();

            mechanicalParamWidget.visible = networkController.graph_data_uploaded() && networkController.is_mechanical_response();
            vertexWidget.visible = networkController.graph_data_uploaded() && networkController.is_mechanical_response();
        }
    }

}
