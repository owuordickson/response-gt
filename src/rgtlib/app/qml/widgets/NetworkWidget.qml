import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Rectangle {
    id: imgContainer
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "transparent"
    clip: true  // Ensures only the selected area is visible
    visible: networkController.graph_is_ready()


    Flickable {
        id: flickableArea
        anchors.fill: parent
        contentWidth: imgView.width * imgView.scale
        contentHeight: imgView.height * imgView.scale
        //clip: true
        flickableDirection: Flickable.HorizontalAndVerticalFlick

        ScrollBar.vertical: ScrollBar {
            id: vScrollBar
            policy: flickableArea.contentHeight > flickableArea.height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }
        ScrollBar.horizontal: ScrollBar {
            id: hScrollBar
            policy: flickableArea.contentWidth > flickableArea.width ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }

        Image {
            id: imgView
            width: flickableArea.width
            height: flickableArea.height
            anchors.centerIn: parent
            transformOrigin: Item.Center
            fillMode: Image.PreserveAspectFit
            source: ""
        }

    }



    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            imgContainer.visible = networkController.graph_is_ready();
            imgView.source = networkController.get_pixmap();
        }
    }

}