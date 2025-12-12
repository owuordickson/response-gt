import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    id: materialPropertyWidget
    Layout.leftMargin: 10
    Layout.preferredHeight: 150
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter
    visible: networkController.graph_data_uploaded()

    property int propsValueRole: Qt.UserRole + 4
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
                property int mainIndex: index

                Label {
                    Layout.preferredWidth: lblWidthSize
                    color: Theme.text
                    text: model.text
                    font.pixelSize: 11
                    color: Theme.black
                }


                SpinBox {
                    id: spinbox
                    Layout.minimumWidth: spbWidthSize

                    // Model values are floats (e.g., 0.00123)
                    property real realMin: model.minValue
                    property real realMax: model.maxValue
                    property real realStep: 0.1             // or 1
                    property real realValue: model.value    // actual decimal

                    // SpinBox INTERNAL integer range
                    from: 0
                    to: Math.round((realMax - realMin) / realStep)
                    // Map realValue → SpinBox integer
                    value: Math.round((realValue - realMin) / realStep)
                    // Convert SpinBox integer → real value (displayed)
                    textFromValue: function (v) {
                        return Number(realMin + v * realStep).toFixed(3)   // format as 3 decimals
                    }

                    // Convert text → integer value
                    valueFromText: function (txt) {
                        let r = Number(txt)
                        return Math.round((r - realMin) / realStep)
                    }

                    onValueChanged: {
                        realValue = realMin + value * realStep
                        updateValue(realValue)      // ← your real update method
                    }
                }


                ComboBox {
                    id: cmbMetric
                    Layout.preferredWidth: cmbWidthSize
                    model: metricsModel
                    textRole: "text"
                    currentIndex: getCurrentIndex()

                    // Fires only when the user selects a new option
                    onActivated: (index) => {
                        // Get the selected multiplier
                        const idx = metricsModel.index(index, 0);
                        let multi_val = metricsModel.data(idx, multiplierRole);
                        updateMultiplier(multi_val);
                    }

                    function getCurrentIndex() {
                        const main_idx = rgtDCParams.index(mainIndex, 0);
                        let sel_multi_val = rgtDCParams.data(main_idx, multiplierRole);

                        for (let row = 0; row < metricsModel.rowCount(); row++) {
                            const idx = metricsModel.index(row, 0);
                            let multi_val = metricsModel.data(idx, multiplierRole);
                            if (sel_multi_val === multi_val) return row;
                        }
                        return 5;
                    }
                }


                function updateValue(val) {
                    if (model.value !== val) {
                        const index = rgtDCParams.index(mainIndex, 0);
                        rgtDCParams.setData(index, val, propsValueRole);
                        //networkController.;
                    }
                }


                function updateMultiplier(val) {
                    if (model.multiplier !== val) {
                        const index = rgtDCParams.index(mainIndex, 0);
                        rgtDCParams.setData(index, val, multiplierRole);
                        //networkController.;
                    }
                }

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