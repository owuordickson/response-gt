import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material as Material

Rectangle {
    id: welcomeContainer
    Layout.fillWidth: true
    Layout.fillHeight: true
    color: "transparent"
    visible: true //!imageController.display_image()

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
                //padding: 5
                enabled: true
                //onClicked: imageFileDialog.open()
            }

            Material.Button {
                id: btnAddEdges
                Layout.preferredWidth: 115
                //Layout.preferredHeight: 32
                text: "Edge list"
                //padding: 5
                enabled: true
                //onClicked: imageFileDialog.open()
            }

            /*Button {
                id: btnAddNodes
                Layout.preferredWidth: 100
                Layout.preferredHeight: 32
                text: ""
                enabled: true
                //onClicked: imageFileDialog.open()

                Rectangle {
                    anchors.fill: parent
                    radius: 5
                    color: "#808080"

                    Label {
                        text: "Vertex positions"
                        color: "white"
                        font.bold: true
                        font.pixelSize: 10
                        anchors.centerIn: parent
                    }
                }
            }

            Button {
                id: btnAddEdges
                Layout.preferredWidth: 100
                Layout.preferredHeight: 32
                text: ""
                enabled: false
                //onClicked: imageFileDialog.open()

                Rectangle {
                    anchors.fill: parent
                    radius: 5
                    color: "#808080"

                    Label {
                        text: "Edge list"
                        color: "white"
                        font.bold: true
                        font.pixelSize: 10
                        anchors.centerIn: parent
                    }
                }
            }*/

        }


    }

}