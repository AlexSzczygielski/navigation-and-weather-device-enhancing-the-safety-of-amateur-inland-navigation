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

    //Properties 
    property string noFixMap: "file:data/temp/current_map.png"

    
        
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
                    text: gnss_backend.gnss_data.runningStatus ? "Running" : "Not Running"
                }

                Button{
                    text: gnss_backend.gnss_data.runningStatus ? "STOP GPS" : "START GPS"
                    //Needs backend update
                    onClicked: gnss_backend.gnss_data.runningStatus ? gnss_backend.start_gnss_worker() : gnss_backend.start_gnss_worker()
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
                    dataText: {
                        if(!Number.isFinite(gnss_backend.gnss_data.latitude)) {
                            return notAvailableText
                        }
                        else {gnss_backend.gnss_data.latitude >= 0 ? gnss_backend.gnss_data.latitude.toFixed(coordsPrecision) + " N" : (-gnss_backend.gnss_data.latitude).toFixed(coordsPrecision) + " S"}
                    }
                }

                DataRow{
                    descriptionText: "Longitude:"
                    dataText: {
                        if(!Number.isFinite(gnss_backend.gnss_data.longitude)) {
                            return notAvailableText
                        }
                        else {gnss_backend.gnss_data.longitude >= 0 ? gnss_backend.gnss_data.longitude.toFixed(coordsPrecision) + " E" : (-gnss_backend.gnss_data.longitude).toFixed(coordsPrecision) + " W"}
                    }
                }

                DataRow{
                    descriptionText: "Altitude:"
                    dataText: !Number.isFinite(gnss_backend.gnss_data.altitude) ? notAvailableText : gnss_backend.gnss_data.altitude
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
                    dataText: {
                        var fix = gnss_backend.gnss_data.gpsFix;
                        return Number(fix) > 1 ? fix + "D" : notAvailableText;
                    }
                }
                
                DataRow{
                    id: satRow
                    descriptionText: "satellites:"
                    dataText: gnss_backend.gnss_data.satellitesNumber < 0 ? notAvailableText : gnss_backend.gnss_data.satellitesNumber
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
                    dataText: !Number.isFinite(gnss_backend.gnss_data.speed) ? notAvailableText : gnss_backend.gnss_data.speed
                }

                DataRow{
                    id: headRow
                    descriptionText: "Heading:"
                    dataText: !Number.isFinite(gnss_backend.gnss_data.heading) ? notAvailableText : gnss_backend.gnss_data.heading
                }
            }
        }
    }

    // Map Image
    Image{
        id: staticMap
        source: gnss_backend.gnss_data.runningStatus ? noFixMap : "qrc:/assets/empty_map.png"
        width: gnss_backend.map_width
        height: gnss_backend.map_height
        fillMode: Image.PreserveAspectFit
        cache: false
    }

    

    Connections{
        target: gnss_backend

        function onMapUpdated(path) {
            staticMap.source = ""
            staticMap.source = "file:" + path
        }
    }
}