import QtQuick
import QtQuick.Controls


MenuBar {

    Menu {
        title: mainController.get_app_title();
        MenuItem { text: "&About"; }//onTriggered: dialogAbout.open(); }
        MenuItem { id:mnuHelp; text: "ResponseGT Help"; enabled: true; }//onTriggered: dialogAbout.open() }
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
            MenuItem {id:mnuExportEdges; text: "Response U"; enabled: false; onTriggered: console.log("Export U") }
            MenuItem {id:mnuExportNodes; text: "Response V"; enabled: false; onTriggered: console.log("Export I") }
        }
    }


    Connections {
        //target:
    }

}

