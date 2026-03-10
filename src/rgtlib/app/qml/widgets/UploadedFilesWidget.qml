import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic as Basic
import Theme 1.0


ColumnLayout {
    id: uploadedFilesWidget
    Layout.leftMargin: 10
    Layout.topMargin: 10
    Layout.preferredHeight: 100
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter | Qt.AlignTop
    visible: networkController.graph_data_uploaded()

    Label {
        text: "Uploaded Data"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }


    Rectangle {
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        width: 220
        height: 100
        color: Theme.veryLightGray
        radius: 4

        Flickable {
            id: flickable
            anchors.fill: parent
            anchors.margins: 2
            anchors.leftMargin: 15
            clip: true
            contentWidth: parent.width          // vertical-only scrolling
            contentHeight: colFiles.implicitHeight + 25

            ColumnLayout {
                id: colFiles
                //Layout.alignment: Qt.AlignHCenter
                Layout.leftMargin: 10
                width: flickable.width - 20
                //anchors.horizontalCenter: flickable.horizontalCenter
                spacing: 2

                Repeater {
                    model: rgtFiles

                    Loader {
                        // Only create delegate when needed
                        active: model.value === 1 || model.value === -1

                        sourceComponent: Rectangle {
                            property int mainIndex: index
                            width: colFiles.width
                            height: 21
                            color: "transparent"

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 4
                                spacing: 5

                                Label {
                                    Layout.fillWidth: true
                                    text: model.text + ' (' + model.type + ')'
                                    font.pixelSize: 10
                                    color: model.value === 1 ? Theme.darkGray : Theme.red
                                    //verticalAlignment: Text.AlignVCenter
                                }

                                Basic.Button {
                                    text: ""
                                    icon.source: "../assets/icons/delete_icon.png"
                                    icon.height: 18
                                    icon.color: model.value === 1 ? Theme.darkGray : Theme.red
                                    background: Rectangle {
                                        color: "transparent"
                                    }

                                    onClicked: {
                                        networkController.remove_data(model.id);
                                    }
                                }
                            }
                        }
                    }
                }
            }

            ScrollBar.vertical: ScrollBar { // Attach vertical scrollbar
                //parent: flickable
                policy: ScrollBar.AsNeeded // Show scrollbar only when needed
            }
        }
    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            uploadedFilesWidget.visible = networkController.graph_data_uploaded();
        }
    }

}