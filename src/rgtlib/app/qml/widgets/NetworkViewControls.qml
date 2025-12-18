import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Imagine as Imagine


Rectangle {
    id: networkViewControls
    height: 32
    Layout.fillHeight: false
    Layout.fillWidth: true
    color: "transparent"
    visible: networkController.graph_is_ready()

    RowLayout {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        Imagine.Button {
            //id: btnRunAnalyzer
            //Layout.preferredWidth: 135
            text: "Re-compute Response"
            onClicked: networkController.run_response_analyzer()
            //Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            networkViewControls.visible = networkController.graph_is_ready();
        }
    }


}