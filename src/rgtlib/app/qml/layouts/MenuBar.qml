import QtQuick
import QtQuick.Controls


MenuBar {

    Menu {
        title: mainController.get_app_title();
        MenuItem {
            text: "&About"; onTriggered: dlgAbout.open(); }
        MenuItem {
            id:
                mnuHelp; text: "ResponseGT Help"; enabled: true; onTriggered: {dlgAbout.open(); mainController.get_about_details();}
        }
        MenuSeparator {
        }
        MenuItem {
            text: "&Quit"; onTriggered: Qt.quit(); }
    }
    Menu {
        title: "File"
        Menu {
            id: mnuImportGraphFrom
            title: "Import network from..."
            MenuItem {
                id: mnuImportNodes; text: "Vertex Positions (CSV)"; enabled: true; onTriggered: {
                    dlgFileData.file_type = "vertices";
                    dlgFileData.open();
                }
            }
            MenuItem {
                id: mnuImportEdges; text: "Edge List (CSV)"; enabled: true; onTriggered: {
                    dlgFileData.file_type = "edges";
                    dlgFileData.open();
                }
            }
        }
        MenuItem {
            id:
                mnuDownloadResults; text: "Download Results"; enabled: false; onTriggered: networkController.export_response_to_file()
        }
    }
    Menu {
        title: "Compute"
        MenuItem {
            id:
                mnuRunResponse; text: "Compute Response"; enabled: false; onTriggered: networkController.run_response_analyzer()
        }
        MenuItem {
            id: mnuDeleteAll; text: "Clear Workspace"; enabled: false; onTriggered: mainController.reset_rgt_obj()
        }
    }


    Connections {
        target: networkController

        function onImageChangedSignal() {
            // Force refresh
            mnuImportNodes.enabled = networkController.enable_vertex_positions_upload();
            mnuImportEdges.enabled = networkController.enable_edge_list_upload();
            mnuDownloadResults.enabled = networkController.graph_data_uploaded();
            mnuRunResponse.enabled = networkController.graph_data_uploaded();
            mnuDeleteAll.enabled = networkController.graph_data_uploaded();
        }
    }

}

