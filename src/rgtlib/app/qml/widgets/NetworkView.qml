import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


ColumnLayout {
    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

    // The welcome view
    WelcomeWidget{}

    // The navigation controls
    NetworkNavControls{}

    // The network container
    NetworkWidget{}

    // The network control buttons
    NetworkViewControls{}

}