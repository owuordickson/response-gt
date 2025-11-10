import QtQuick
import QtQuick.Controls


MenuBar {

    Menu {
        title: projectController.get_sgt_title()
        MenuItem { text: "&About"; }//onTriggered: dialogAbout.open(); }
        MenuItem { id:mnuHelp; text: "ResponseGT Help"; enabled: true; }//onTriggered: dialogAbout.open() }
        MenuSeparator{}
        MenuItem { text: "&Quit"; onTriggered: Qt.quit(); }
    }
    Menu {
        title: "File"
        Menu {
            id: mnuImportGraphFrom
            title: "Import graph from..."
            MenuItem {id: mnuImportCSV; text:"CSV (adj. matrix, edge list, xyz)"; enabled: true; }//onTriggered: graphFileDialog.open()}
            MenuItem {id: mnuImportGSD; text:"GSD/HOOMD"; enabled: true; }//onTriggered: graphFileDialog.open()}
        }
    }


}

