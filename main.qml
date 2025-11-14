//main.qml
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

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
            IconButton{
                id: loaderHome
                iconSource: "qrc:/assets/home.svg"
                selected: true
                Component.onCompleted: allButtons.push(loaderHome)

                onIconClicked: {
                    resetSelection()
                    loaderHome.selected = true
                    mainLoader.source = "qrc:/views/home.qml"
                }
            }

            IconButton{
                id: loaderNavi
                iconSource: "qrc:/assets/navi.svg"
                Component.onCompleted: allButtons.push(loaderNavi)
            }

            IconButton{
                id: loaderSett
                iconSource: "qrc:/assets/settings.svg"
                Component.onCompleted: allButtons.push(loaderSett.item)
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
            Layout.preferredWidth: 80
            spacing: 16
            //Left Icons Bar

            //Loading icons from IconButton.qml
            IconButton{
                id: loaderCvRoi
                iconSource: "qrc:/assets/camera100.svg"
                Component.onCompleted: allButtons.push(loaderCvRoi)

                onIconClicked: {
                    resetSelection()
                    loaderCvRoi.selected = true
                    mainLoader.source = "qrc:/views/cv_create_roi_panel.qml"
                }
            }

            IconButton{
                id: loaderCvDetection
                iconSource: "qrc:/assets/camera100.svg"
                Component.onCompleted: allButtons.push(loaderCvDetection)

                onIconClicked: {
                    resetSelection()
                    loaderCvDetection.selected = true
                    mainLoader.source = "qrc:/views/cv_detect_pipe_panel.qml"
                }
            }

            IconButton{
                id: loaderSett2
                iconSource: "qrc:/assets/settings.svg"
                onIconClicked: allButtons.push(loaderSett2)
            }
        }        
    }
}
