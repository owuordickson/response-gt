import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Rectangle {
    id: networkNavControls
    height: 32
    Layout.fillHeight: false
    Layout.fillWidth: true
    color: "transparent"
    visible: false

    RowLayout {
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        ColumnLayout {

            /*Label {
                text: "Response Type"
                color: Theme.text
            }*/

            ResponseTypeWidget{}
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            networkNavControls.visible = networkController.graph_is_ready();
        }
    }

}