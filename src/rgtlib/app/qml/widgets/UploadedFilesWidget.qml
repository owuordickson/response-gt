import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic as Basic
import Theme 1.0


ColumnLayout {
    id: uploadedFilesWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 75
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
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
        width: 200
        height: 75
        color: "transparent"
        border.width: 1
        border.color: Theme.darkGrey
        radius: 4

        Flickable {
            id: flickable
            anchors.fill: parent
            anchors.margins: 2
            contentWidth: parent.width // Important for vertical-only scrolling
            contentHeight: colFiles.implicitHeight

            ColumnLayout.flickable: ColumnLayout {
                id: colFiles

                Repeater {
                    id: rptFiles
                    model: rgtFiles

                    Loader {
                        active: model.value === 1 || model.value === -1  // <-- Only create the delegate if visible

                        sourceComponent: Rectangle {
                            property int mainIndex: index
                            width: flickable.width
                            height: 21
                            color: "transparent"
                            //border.width: 1
                            //border.color: model.value === 1 ? Theme.green : Theme.red
                            //radius: 2

                            RowLayout {
                                anchors.fill: parent
                                anchors.margins: 4
                                spacing: 5

                                Label {
                                    Layout.fillWidth: true
                                    text: model.text + ' (' + model.type + ')'
                                    font.pixelSize: 10
                                    color: model.value === 1 ? Theme.green : Theme.red
                                }


                                Basic.Button {
                                    id: btnDelete
                                    text: ""
                                    icon.source: "../assets/icons/delete_icon.png"
                                    icon.height: 18
                                    icon.color: "transparent"   // important for PNGs
                                    background: Rectangle {
                                        color: "transparent"
                                    }
                                    onClicked: {
                                        //networkController.;
                                    }
                                }

                            }

                        }

                    }

                }
            }

            ScrollBar.vertical: ScrollBar { // Attach vertical scrollbar
                parent: flickable
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