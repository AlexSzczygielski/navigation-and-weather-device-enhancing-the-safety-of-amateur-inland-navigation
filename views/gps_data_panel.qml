//gps_data_panel.qml
/*
GPS data panel loaded inside main.qml.
This qml file uses DataRow component, loaded from components/DataRow.qml.
Loading is managed by qrc file.
*/
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

RowLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true
    property int borderWidth: 3
    property int firstColumnWidth: 220
    property string rectangleColor: "#00bfa5"
    property int divisionHeight: 5
    property int dataRowSpacing: 12
    property string notAvailableText: "Dev OFF"
    property int coordsPrecision: 5

    //Properties for input signals
    property bool isThreadRunning: false
    property real latitude: gps_backend.gnss_data.latitude == "NaN" ? notAvailableText : gps_backend.gnss_data.latitude
    property real longitude
    property string altitude: notAvailableText
    property string gpsFix: notAvailableText
    property string satelitesNumber: notAvailableText
    property string speed: notAvailableText
    property string heading: notAvailableText
    property string currentMap: "file:data/temp/current_map.png"

    
        
    //Left Column Section
    Rectangle {
        color: "transparent"
        border.color: rectangleColor
        border.width: borderWidth

        Layout.preferredWidth: firstColumnWidth
        Layout.fillHeight: true 

        //Main Column Stack for the left rectangle
        ColumnLayout{
            anchors.centerIn: parent
            spacing: 20

            //Position section
            ColumnLayout {
                spacing: dataRowSpacing
                //anchors.centerIn: parent

                //Thread Status vertically to denote difference between the rest
                Label{
                    font.bold: true
                    text: "GPS Thread Status:"
                }

                Label{
                    text: isThreadRunning ? "Running" : "Not Running"
                }

                Button{
                    text: isThreadRunning ? "STOP GPS" : "START GPS"
                    //Needs backend update
                    onClicked: isThreadRunning ? gps_backend.start_gnss_worker() : gps_backend.start_gnss_worker()
                }

                Rectangle{
                    color: rectangleColor
                    height: divisionHeight
                    Layout.fillWidth: true
                }
                
                //Position section
                Label{
                    font.bold: true
                    text: "Position:"
                }

                DataRow{
                    descriptionText: "Latitude: " 
                    readyText: latitude >= 0 ? latitude.toFixed(coordsPrecision) + " N" : (-latitude).toFixed(coordsPrecision) + " S"
                    notReadyText: {
                        if(!Number.isFinite(latitude)) {
                            return notAvailableText
                        }
                        else {latitude >= 0 ? latitude.toFixed(coordsPrecision) + " N" : (-latitude).toFixed(coordsPrecision) + " S"}
                    }
                }

                DataRow{
                    id: longRow
                    descriptionText: "Longitude:"
                    readyText: longitude >= 0 ? longitude.toFixed(coordsPrecision) + " E" : (-longitude).toFixed(coordsPrecision) + " W"
                    notReadyText: notAvailableText
                }

                DataRow{
                    id: altRow
                    descriptionText: "Altitude:"
                    readyText: altitude
                    notReadyText: notAvailableText
                }
            }
            
            //Division between sections
            Rectangle{
                color: rectangleColor
                height: divisionHeight
                Layout.fillWidth: true
            }
            
            //GNSS status section
            ColumnLayout{
                spacing: dataRowSpacing
                //anchors.centerIn: parent

                Label{
                    font.bold: true
                    text: "GNSS Status:"
                }

                DataRow{
                    id: gpsFixRow
                    descriptionText: "GPS fix:"
                    readyText: Number(gpsFix) > 1 ? gpsFix + "D" : ""
                    notReadyText: notAvailableText
                }
                
                DataRow{
                    id: satRow
                    descriptionText: "Satelites:"
                    readyText: satelitesNumber
                    notReadyText: notAvailableText
                }
            }

            //Division between sections
            Rectangle{
                color: rectangleColor
                height: divisionHeight
                Layout.fillWidth: true
            }

            //Motion Section
            ColumnLayout{
                spacing: dataRowSpacing

                Label{
                    font.bold: true
                    text: "Motion:"
                }

                DataRow{
                    id: speedRow
                    descriptionText: "Speed:"
                    readyText: speed
                    notReadyText: notAvailableText
                }

                DataRow{
                    id: headRow
                    descriptionText: "Heading:"
                    readyText: heading
                    notReadyText: notAvailableText
                }
            }
        }
    }

    // Map Image
    Image{
        id: staticMap
        source: isThreadRunning ? currentMap : "qrc:/assets/empty_map.png"
        width: gps_backend.map_width
        height: gps_backend.map_height
        fillMode: Image.PreserveAspectFit
        cache: false
    }

    

    Connections{
        target: gps_backend
        function onRunningStatusUpdated(isRunning) {
            isThreadRunning = isRunning

            if(!isRunning) {
                latRow.isReady = false
                longRow.isReady = false
                altRow.isReady = false
                gpsFixRow.isReady = false
                satRow.isReady = false
                speedRow.isReady = false
                headRow.isReady = false
            }
        }

        function onMapUpdated(path) {
            staticMap.source = ""
            staticMap.source = "file:" + path
        }

        function onLatitudeUpdated(value) {
            latitude = value
            latRow.isReady = true
        }

        function onLongitudeUpdated(value) {
            longitude = value
            longRow.isReady = true
        }

        function onAltitudeUpdated(value) {
            altitude = value
            altRow.isReady = true
        }

        function onGpsFixUpdated(value) {
            gpsFix = value
            gpsFixRow.isReady = true
        }

        function onSatelitesNumberUpdated(value) {
            satelitesNumber = value
            satRow.isReady = true
        }

        function onSpeedUpdated(value) {
            speed = value
            speedRow.isReady = true
        }

        function onHeadingUpdated(value) {
            heading = value
            headRow.isReady = true
        }
    }
}