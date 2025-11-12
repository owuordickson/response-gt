import QtQuick
import QtQuick.Controls


MenuBar {

    Menu {
        title: mainController.get_app_title();
        MenuItem { text: "&About"; onTriggered: dlgAbout.open(); }
        MenuItem { id:mnuHelp; text: "ResponseGT Help"; enabled: true; onTriggered: dlgAbout.open() }
        MenuSeparator{}
        MenuItem { text: "&Quit"; onTriggered: Qt.quit(); }
    }
    Menu {
        title: "File"
        Menu {
            id: mnuImportGraphFrom
            title: "Import network from..."
            MenuItem {id: mnuImportNodes; text:"Vertex Positions (CSV)"; enabled: true; }//onTriggered: graphFileDialog.open()}
            MenuItem {id: mnuImportEdges; text:"Edge List (CSV)"; enabled: true; }//onTriggered: graphFileDialog.open()}
        }
        MenuSeparator{}

        Menu {
            id: mnuExportResponseAs
            title: "Export as..."
            MenuItem {id:mnuExportEdges; text: "Vertex Potentials"; enabled: false; onTriggered: console.log("Export Potentials") }
            MenuItem {id:mnuExportNodes; text: "Edge Currents"; enabled: false; onTriggered: console.log("Export Currents") }
        }
        MenuSeparator{}

        MenuItem {id: mnuDeleteAll; text: "Clear Workspace"; onTriggered: mainController.reset_rgt_obj()}
    }


    Connections {
        //target:
    }

}

