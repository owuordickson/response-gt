import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: materialPropertyWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 250
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignTop
    enabled: false
    visible: networkController.graph_is_ready()

    property int lblWidthSize: 50
    property int cbWidthSize: 50
    property int spbWidthSize: 170

    Text {
        text: "Material Properties"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }

    ColumnLayout {
        id: colParams
        spacing: 10

        Repeater {
            model: rgtDCParams
            delegate: RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft
                visible: model.visible

                Label {
                    text: model.text
                    font.pixelSize: 11
                    color: "#000000"
                }

                Loader {
                    id: controlLoader
                    sourceComponent: (model.id === "resistivity" || model.id === "potential_magnitude") ? spinOnly : spinAndCombo
                }


                Component {
                    id: spinOnly

                    RowLayout {
                        Layout.fillWidth: true

                        SpinBox {
                            id: spinbox
                            objectName: model.id
                            Layout.minimumWidth: spbWidthSize
                            Layout.fillWidth: true
                            from: model.minValue
                            to: model.maxValue
                            stepSize: model.stepSize
                            property var currSBVal: 2//model.value
                            value: currSBVal
                            //onValueChanged: updateValue(currSBVal, value)
                        }
                    }

                }


                Component {
                    id: spinAndCombo

                    RowLayout {
                        Layout.fillWidth: true

                        SpinBox {
                            id: spinbox
                            objectName: model.id
                            Layout.minimumWidth: spbWidthSize
                            Layout.fillWidth: true
                            from: model.minValue
                            to: model.maxValue
                            stepSize: model.stepSize
                            property var currSBVal: 2//model.value
                            value: currSBVal
                            //onValueChanged: updateValue(currSBVal, value)
                        }


                        ComboBox {
                            Layout.minimumWidth: cbWidthSize
                        }

                    }

                }

            }
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            materialPropertyWidget.visible = networkController.graph_is_ready();
        }
    }

}