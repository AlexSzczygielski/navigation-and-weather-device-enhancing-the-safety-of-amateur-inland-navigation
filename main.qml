//main.qml
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

ApplicationWindow {
    Connections {
        target: backend
    }
    onClosing: {
        backend.shutdown_all()
    }
    id: app
    visible: true
    width: 1024
    height: 600
    title: "Yacht System GUI"
    //color: "#0b1d2a"
    color: Material.background

    property bool nightMode: true

    Material.theme: nightMode ? Material.Dark : Material.Light
    Material.background: nightMode ? "#0b1d2a" : "#f5f5f5"
    Material.foreground: nightMode ? "#e0f2f1" : "#212121"
    Material.primary: "#00bfa5"
    Material.accent: "#00bfa5"

    property int iconSize: 50
    //property int currentPage: 0
    property var allButtons: []

    function resetSelection(){
        //resets all of the selected buttons
        for (let b of allButtons) {
            if (b) b.selected = false
        }
    }
//////////////CHANGHE//////////////////////////////////
     Rectangle {
        width: 50
        height: 50
        color: "red"
        radius: 10
        Text {
            anchors.centerIn: parent
            text: "X"
            color: "white"
            font.pixelSize: 20
        }
        MouseArea {
            anchors.fill: parent
            onClicked: {
                Qt.quit()  // This will quit the app when the button is clicked
            }
        }
    }
////////////////////!!!!!!!?/////////////////////////////

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
                nightMode: app.nightMode
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
                nightMode: app.nightMode
                iconSource: "qrc:/assets/navi.svg"
                Component.onCompleted: allButtons.push(loaderNavi)
                onIconClicked: {
                    resetSelection()
                    loaderNavi.selected = true
                    mainLoader.source = "qrc:/views/gps_data_panel.qml"
                }
            }

            IconButton{
                id: loaderSett
                nightMode: app.nightMode
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
                nightMode: app.nightMode
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
                nightMode: app.nightMode
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
                nightMode: app.nightMode
                iconSource: "qrc:/assets/settings.svg"
                onIconClicked: allButtons.push(loaderSett2)
            }
        }        
    }
}
