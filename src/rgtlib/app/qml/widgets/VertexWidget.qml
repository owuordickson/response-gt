import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Theme 1.0


ColumnLayout {
    Layout.leftMargin: 10
    Layout.preferredHeight: 50
    Layout.preferredWidth: parent.width
    Layout.alignment: Qt.AlignVCenter | Qt.AlignTop
    visible: false

    property int dirValueRole: Qt.UserRole + 4
    property int lblWidthSize: 100
    property int spbWidthSize: 150

    Label {
        text: "Vertex Parameters"
        color: Theme.text
        font.pixelSize: 12
        font.bold: true
        Layout.alignment: Qt.AlignHCenter
    }

    Repeater {
        model: rgtPotentialOptions
        Loader {
            active: model.visible === 1 && model.id === 'selected_vertex_proportion'   // <-- Only create the delegate if visible

            sourceComponent: RowLayout {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft
                property int mainIndex: index
                visible: model.visible === 1

                Label {
                    Layout.preferredWidth: lblWidthSize
                    text: model.text
                    font.pixelSize: 11
                    color: Theme.blue
                }

                SpinBox {
                    id: spinbox
                    Layout.preferredWidth: spbWidthSize

                    // Model values are floats (e.g., 0.00123)
                    property real realMin: model.minValue
                    property real realMax: model.maxValue
                    property real realStep: 0.01             // or 1
                    property real realValue: model.value    // actual decimal

                    // SpinBox INTERNAL integer range
                    from: 0
                    to: Math.round((realMax - realMin) / realStep)
                    // Map realValue → SpinBox integer
                    value: Math.round((realValue - realMin) / realStep)
                    // Convert SpinBox integer → real value (displayed)
                    textFromValue: function (v) {
                        return Number(realMin + v * realStep).toFixed(2)   // format as 2 decimals
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

                function updateValue(val) {
                    if (model.value !== val) {
                        const index = rgtPotentialOptions.index(mainIndex, 0);
                        rgtPotentialOptions.setData(index, val, dirValueRole);
                        //networkController.;
                    }
                }

            }
        }
    }

}