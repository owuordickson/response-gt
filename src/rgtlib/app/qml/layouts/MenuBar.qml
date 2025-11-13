import QtQuick
import QtQuick.Controls


MenuBar {

    Menu {
        title: mainController.get_app_title();
        MenuItem { text: "&About"; onTriggered: dlgAbout.open(); }
        MenuItem { id:mnuHelp; text: "ResponseGT Help"; enabled: true; onTriggered: {dlgAbout.open(); mainController.get_about_details();} }
        MenuSeparator{}
        MenuItem { text: "&Quit"; onTriggered: Qt.quit(); }
    }
    Menu {
        title: "File"
        Menu {
            id: mnuImportGraphFrom
            title: "Import network from..."
            MenuItem {id: mnuImportNodes; text:"Vertex Positions (CSV)"; enabled: true; onTriggered: dlgFileVertices.open()}
            MenuItem {id: mnuImportEdges; text:"Edge List (CSV)"; enabled: true; onTriggered: dlgFileEdges.open()}
            MenuItem {id: mnuDownloadResults; text: "Download Results"; enabled: false; onTriggered: console.log("Export Response Potentials and Currents") }
        }
        MenuSeparator{}

        MenuItem {id: mnuDeleteAll; text: "Clear Workspace"; onTriggered: mainController.reset_rgt_obj()}
    }


    Connections {
        //target:
    }

}

