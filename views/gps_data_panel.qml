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

ColumnLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true
    property int borderWidth: 3
    property int firstColumnWidth: 170
    property string rectangleColor: "#00bfa5"
    property int divisionHeight: 5
    property int dataRowSpacing: 12
    property string notAvailableText: "n/a"

    //Properties for input signals
    property bool isThreadRunning: false
    property string latitude: notAvailableText
    property string longitude: notAvailableText
    property string altitude: notAvailableText
    property string gpsFix: notAvailableText
    property string satelitesNumber: notAvailableText
    property string speed: notAvailableText
    property string heading: notAvailableText

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

                Label{
                    font.bold: true
                    text: "GPS Thread Status:"
                }

                DataRow{
                    id: gpsThreadRunStatus
                    descriptionText: ""
                    notReadyText: "Not running"
                    readyText: "Running"
                }

                Button{
                    text: isThreadRunning ? "STOP GPS" : "START GPS"
                    onClicked: gps_backend.start_gnss_worker()
                }

                Rectangle{
                    color: rectangleColor
                    height: divisionHeight
                    Layout.fillWidth: true
                }
                

                Label{
                    font.bold: true
                    text: "Position:"
                }

                DataRow{
                    id: latRow
                    descriptionText: "Latitude: " 
                    readyText: latitude
                    notReadyText: "Empty device"
                }

                DataRow{
                    id: longRow
                    descriptionText: "Longitude:"
                    readyText: longitude
                    notReadyText: "Empty device"
                }

                DataRow{
                    id: altRow
                    descriptionText: "Altitude:"
                    readyText: altitude
                    notReadyText: "Empty device"
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
                    readyText: "OK"
                    notReadyText: "None"
                }
                
                DataRow{
                    id: satRow
                    descriptionText: "Satelites:"
                    readyText: satelitesNumber
                    notReadyText: "None"
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
                    notReadyText: "Empty device"
                }

                DataRow{
                    id: headRow
                    descriptionText: "Heading:"
                    readyText: heading
                    notReadyText: "Empty device"
                }
            }
        }
    }

    Connections{
        target: gps_backend
        function onRunningStatusUpdated(isRunning) {
            gpsThreadRunStatus.ready = isRunning
            isThreadRunning = isRunning
        }

        function onLatitudeUpdated(value) {
            latRow.notReadyText = value
            latRow.ready = true
        }

        function onLongitudeUpdated(value) {
            longRow.notReadyText = value
            longRow.ready = true
        }

        function onAltitudeUpdated(value) {
            altRow.notReadyText = value
            altRow.ready = true
        }

        function onGpsFixUpdated(value) {
            gpsFixRow.notReadyText = value
            gpsFixRow.ready = true
        }

        function onSatelitesNumberUpdated(value) {
            satRow.notReadyText = value
            satRow.ready = true
        }

        function onSpeedUpdated(value) {
            speedRow.notReadyText = value
            speedRow.ready = true
        }

        function onHeadingUpdated(value) {
            headRow.notReadyText = value
            headRow.ready = true
        }
    }
}