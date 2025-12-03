import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: materialPropertyWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 210
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()

    property int valueRole: Qt.UserRole + 4
    property int multiplierRole: Qt.UserRole + 12

    property int lblWidthSize: 100
    property int cmbWidthSize: 64
    property int spbWidthSize: 75

    Text {
        text: "Response Parameters"
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }

    ColumnLayout {
        id: colParams
        //spacing: 10

        Repeater {
            model: rgtDCParams
            delegate: RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft
                enabled: model.visible === 1

                Label {
                    Layout.preferredWidth: lblWidthSize
                    text: model.text
                    font.pixelSize: 11
                    color: "#000000"
                }

                SpinBox {
                    id: spinbox
                    objectName: model.id
                    Layout.minimumWidth: spbWidthSize
                    //Layout.fillWidth: true
                    from: model.minValue
                    to: model.maxValue
                    stepSize: 1
                    property var currSBVal: model.value
                    value: currSBVal
                    onValueChanged: updateValue(value)
                }

                ComboBox {
                    id: cmbMetric
                    objectName: model.id
                    Layout.preferredWidth: cmbWidthSize
                    model: metricsModel
                    textRole: "text"
                    currentIndex: 5

                    // Fires only when the user selects a new option
                    onActivated: (index) => {
                        // Get the selected multiplier
                        const idx = metricsModel.index(index, 0);
                        let multi_val = metricsModel.data(idx, multiplierRole); // MultiplierRole
                        updateMultiplier(multi_val);
                    }
                }

                function updateValue(val) {
                    if (model.value !== val) {
                        var index = rgtDCParams.index(model.index, 0);
                        rgtDCParams.setData(index, val, valueRole);
                        //networkController.;
                    }
                }


                function updateMultiplier(val) {
                    if (model.multiplier !== val) {
                        var index = rgtDCParams.index(model.index, 0);
                        rgtDCParams.setData(index, val, multiplierRole);
                        //networkController.;
                    }
                }


                /*Loader {
                    id: controlLoader
                    sourceComponent: (model.id === "resistivity" || model.id === "potential_magnitude") ? spinOnly : spinAndCombo
                }


                Component {
                    id: spinOnly

                    RowLayout {
                        //Layout.fillWidth: true

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
                        //Layout.fillWidth: true

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
                            Layout.preferredWidth: cmbWidthSize
                        }

                    }

                }*/

            }
        }

    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            materialPropertyWidget.visible = networkController.graph_data_uploaded();
        }
    }

}