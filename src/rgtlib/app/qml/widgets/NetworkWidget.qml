import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Rectangle {
    id: imgContainer
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "transparent"
    clip: true  // Ensures only the selected area is visible
    visible: false //imageController.display_image()

}