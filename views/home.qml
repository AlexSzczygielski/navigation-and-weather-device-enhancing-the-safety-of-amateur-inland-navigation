//home.qml
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

//Left Data
RowLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true
    spacing: 10

    property int mainPrecision: 1
    property int borderWidth: 3
    property int coordsPrecision: 2
    property string notAvailableText: "Dev OFF"
    property string rectangleColor: "#00bfa5"

    property int speed: (gnss_backend.gnss_data.speed*1.94384).toFixed(coordsPrecision)

    ColumnLayout{
        Layout.fillWidth: true
        spacing: 50
        ColumnLayout{
            //Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter
            spacing: 10
            
            Dial {
                //speed data defined as view's property
                id: speedDial
                from: 0
                value: gnss_backend.gnss_data.runningStatus ? speed : 0
                to: 12
                stepSize: 1

                enabled: true

                ColumnLayout{
                    anchors.centerIn: speedDial
                    Label {
                        id: speedDialSpeedLabel
                        text: speed
                        font.pixelSize: 22
                        font.bold: true
                        color: "#00bfa5"
                        Layout.alignment: Qt.AlignHCenter
                    }

                    Label {
                        text: "knt"
                        font.pixelSize: 12
                        font.bold: true
                        color: "#179985"
                        Layout.alignment: Qt.AlignHCenter
                    }
                }
                
                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.AllButtons
                    onPressed: mouse.accepted = true
                    onWheel: wheel.accepted = true
                }

                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 128
                Layout.preferredHeight: 128
            }

            Label{
                Layout.alignment: Qt.AlignHCenter
                font.bold: true
                text: "Speed"
            }
        }

        ColumnLayout{
            Layout.fillWidth: true
            Label{
                font.bold: true
                text: "NAV DATA:"
            }

            Rectangle{
                color: "transparent"
                border.color: rectangleColor
                border.width: borderWidth

                Layout.preferredWidth: 170
                Layout.preferredHeight: 200
                
                ColumnLayout{
                    Layout.fillHeight: true
                    anchors.centerIn: parent
                    spacing: 20
                    DataRow{
                        id: headRow
                        descriptionText: "Heading:"
                        dataText: gnss_backend.gnss_data.runningStatus ? gnss_backend.gnss_data.heading : notAvailableText
                    }

                    DataRow{
                        descriptionText: "Latitude: " 
                        dataText: {
                            if(gnss_backend.gnss_data.runningStatus) {
                                gnss_backend.gnss_data.latitude >= 0 ? gnss_backend.gnss_data.latitude.toFixed(coordsPrecision) + " N" : (-gnss_backend.gnss_data.latitude).toFixed(coordsPrecision) + " S"
                            }
                            else {notAvailableText}
                        }
                    }

                    DataRow{
                        descriptionText: "Longitude:"
                        dataText: {
                            if(gnss_backend.gnss_data.runningStatus) {
                                gnss_backend.gnss_data.longitude >= 0 ? gnss_backend.gnss_data.longitude.toFixed(coordsPrecision) + " E" : (-gnss_backend.gnss_data.longitude).toFixed(coordsPrecision) + " W"
                            }
                            else {notAvailableText}
                        }
                    }

                } 
            }
        }
    }

    // Divider
    Rectangle { color: "#00bfa5"; implicitWidth: 2; Layout.fillHeight: true }

    //Middle Section
    ColumnLayout{
        Layout.preferredWidth: 80
        Layout.fillHeight: true
        spacing: 20
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        //Time and Date
        ColumnLayout {
            id: clockDate
            spacing: 2
            Layout.alignment: Qt.AlignHCenter
            property string timeText: ""
            property string dateText: ""

            Timer {
                interval: 1000    // update every second
                running: true
                repeat: true
                triggeredOnStart: true
                onTriggered: {
                    var now = new Date()

                    clockDate.timeText = now.getHours().toString().padStart(2, '0') + ":" +
                                         now.getMinutes().toString().padStart(2, '0')

                    clockDate.dateText = now.getDate().toString().padStart(2, '0') + "/" +
                                         (now.getMonth() + 1).toString().padStart(2, '0') + "/" +
                                         now.getFullYear()
                }
            }

            Label {
                text: clockDate.timeText
                font.pixelSize: 78
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            Label {
                text: clockDate.dateText
                font.pixelSize: 18
                font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }
        }

        Image {
            Layout.topMargin: 20
            source: "file:assets/model2.png"
            //fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
        }
    }

    //Divider
    Rectangle { color: "#00bfa5"; implicitWidth: 2; Layout.fillHeight: true }

    ColumnLayout{
        Layout.fillHeight: true
        Layout.fillWidth: true
        spacing: 16
        DataRow {
            descriptionText: "GPS:"
            dataText: gnss_backend.gnss_data.runningStatus ? "Running" : "OFF"
        }
        
        DataRow {
            descriptionText: "MOB Detection:"
            dataText: cv_backend.cv_data.runningMobPipeStatus ? "Running" : "OFF"
        }

        Dial {
            id: volumeDial2
            from: 0
            value: 42
            to: 100
            stepSize: 1

            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 128
            Layout.preferredHeight: 128
        }
    }
}