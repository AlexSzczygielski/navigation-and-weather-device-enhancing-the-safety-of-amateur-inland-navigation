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
//--------- TOP BUTTONS -----------

IconButton{
    anchors.top: parent.top
    anchors.left: parent.left
    anchors.margins: 16
    rectangleWidth: 60
    rectangleHeight: 60
    iconSize: 40
    
    id: exitButton
    nightMode: app.nightMode
    iconSource: "qrc:/assets/off.svg"
    color: exitButton.selected ? ("#ff1744") : 
                                 (nightMode ? "#8e2424" : "#d32f2f")
            
    Timer {
        // Enables `animation` look
        id: exitDelay
        interval: 100
        repeat: false
        onTriggered: Qt.quit()
    }

    onIconClicked: {
        exitButton.selected = true
        exitDelay.start()
    }
}

IconButton {
    id: nightModeToggle
    anchors.top: parent.top
    anchors.right: parent.right
    anchors.margins: 16
    rectangleWidth: 60
    rectangleHeight: 60
    iconSize: 40

    nightMode: app.nightMode
    iconSource: nightMode ? "qrc:/assets/night.svg" : "qrc:/assets/day.svg"
    selected: false

    Timer {
        // Enables `animation` look
        id: animationDelay
        interval: 200
        repeat: false
        onTriggered:{
            app.nightMode = !app.nightMode
            nightModeToggle.selected = false
        }
    }

    onIconClicked: {
        selected = true
        animationDelay.start()
    }
}
//-----------------------------

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
                iconSource: "qrc:/assets/mob_system.svg"
                Component.onCompleted: allButtons.push(loaderCvDetection)

                onIconClicked: {
                    resetSelection()
                    loaderCvDetection.selected = true
                    mainLoader.source = "qrc:/views/cv_detect_pipe_panel.qml"
                }
            }

            IconButton{
                id: loaderWeather
                nightMode: app.nightMode
                iconSource: "qrc:/assets/weather.svg"
                Component.onCompleted: allButtons.push(loaderWeather)

                onIconClicked: {
                    resetSelection()
                    loaderWeather.selected = true
                    mainLoader.source = "qrc:/views/weather_data_panel.qml"
                }
            }
        }        
    }
}
