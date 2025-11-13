import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 1024
    height: 600
    title: "Yacht System GUI"

    property int iconSize: 50
    //property int currentPage: 0
    property var allButtons: []

    function resetSelection(){
        //resets all of the selected buttons
        for (let b of allButtons) {
            if (b) b.selected = false
        }
    }


    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        //Left Panel
        ColumnLayout{
            Layout.fillHeight: true
            Layout.preferredWidth: 100
            spacing: 16
            //Left Icons Bar

            //Loading icons from IconButton.qml
            Loader{
                id: loaderHome
                source: "qrc:/components/IconButton.qml"
                onLoaded: {
                    loaderHome.item.iconSource = "qrc:/assets/home.svg"
                    loaderHome.item.selected = true
                    //add to allButtons
                    allButtons.push(loaderHome.item)

                    loaderHome.item.clicked.connect(() => {
                        resetSelection()
                        loaderHome.item.selected = true
                        mainLoader.source = "qrc:/views/home.qml"
                    } )
                }
            }

            Loader{
                id: loaderNavi
                source: "qrc:/components/IconButton.qml"
                onLoaded: {
                    loaderNavi.item.iconSource = "qrc:/assets/navi.svg"
                    allButtons.push(loaderNavi.item)
                }
            }

            Loader{
                id: loaderSett
                source: "qrc:/components/IconButton.qml"
                onLoaded: {
                    loaderSett.item.iconSource = "qrc:/assets/settings.svg"
                    allButtons.push(loaderSett.item)
                }
            }
        }
        

        //Center Content
        Loader{
            id: mainLoader
            source: "qrc:/views/home.qml"
            Layout.fillWidth: true
            Layout.fillHeight: true
        }


        //Right Panel
        ColumnLayout{
            Layout.fillHeight: true
            Layout.preferredWidth: 100
            spacing: 16
            //Left Icons Bar

            //Loading icons from IconButton.qml
            Loader{
                id: loaderCvRoi
                source: "qrc:/components/IconButton.qml"
                onLoaded: {
                    loaderCvRoi.item.iconSource = "qrc:/assets/camera100.svg"
                    allButtons.push(loaderCvRoi.item)

                    Qt.callLater(() => {
                        loaderCvRoi.item.clicked.connect(() => {
                            resetSelection()
                            loaderCvRoi.item.selected = true
                            mainLoader.source = "qrc:/views/cv_create_roi_panel.qml"
                        } )
                    })
                }
            }

            Loader{
                id: loaderCvDetection
                source: "qrc:/components/IconButton.qml"

                onLoaded: {
                    loaderCvDetection.item.iconSource = "qrc:/assets/camera100.svg"
                    allButtons.push(loaderCvDetection.item)
                    
                    Qt.callLater(() => {
                        loaderCvDetection.item.clicked.connect(() => {
                            resetSelection()
                            loaderCvDetection.item.selected = true
                            mainLoader.source = "qrc:/views/cv_detect_pipe_panel.qml"
                        } )
                    })
                }
            }

            Loader{
                id: loaderSett2
                source: "qrc:/components/IconButton.qml"

                onLoaded: {
                    loaderSett2.item.iconSource = "qrc:/assets/settings.svg"
                    allButtons.push(loaderSett2.item)
                }
            }
        }        
    }
}
