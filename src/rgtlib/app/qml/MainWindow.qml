import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "widgets"
import "layouts"
import "dialogs"

ApplicationWindow {
    id: mainWindow
    width: 1024
    height: 768
    visible: true
    title: mainController.get_app_title();
    font.family: "Arial"  // or Qt.application.font.family
    color: "#f0f0f0"

    // Top Menu Bar
    menuBar: MenuBar {}

    // Bottom Status Bar
    footer: StatusBarLayout {}

    // Main Content
    GridLayout {
        anchors.fill: parent
        rows: 1
        columns: 2


        // First row, first column - Left Navigation Pane
        Rectangle {
            id: recLeftPane
            Layout.row: 0
            Layout.column: 0
            Layout.leftMargin: 10
            Layout.rightMargin: 5
            Layout.preferredHeight: parent.height - 10
            Layout.preferredWidth: 300
            color: "#f0f0f0"
            LeftLayout {}
        }

        // First row, second column - Center Content
        Rectangle {
            id: recCenterContent
            Layout.row: 0
            Layout.column: 1
            Layout.rightMargin: 10
            Layout.preferredHeight: parent.height - 10
            Layout.preferredWidth: parent.width - 300
            Layout.fillWidth: true
            color: "#f0f0f0"
            MainLayout {}
        }

    }

    // Dialogs
    DialogAbout{id: dlgAbout}
    DialogAlert{id: dialogAlert}
    DialogFileVertices{id: dlgFileVertices}
    DialogFileEdges{id: dlgFileEdges}

}
