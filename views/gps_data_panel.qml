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
                    text: "Position:"
                }

                DataRow{
                    descriptionText: "Latitude:"
                    notReadyText: "Dummy data"
                }

                DataRow{
                    descriptionText: "Longitude:"
                    notReadyText: "Dummy data"
                }

                DataRow{
                    descriptionText: "Altitude:"
                    notReadyText: "Dummy data"
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
                    descriptionText: "GPS fix:"
                    readyText: "OK"
                    notReadyText: "None"
                }
                
                DataRow{
                    descriptionText: "Satelites:"
                    readyText: ""
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
                    descriptionText: "Speed:"
                    readyText: ""
                    notReadyText: "None"
                }

                DataRow{
                    descriptionText: "Heading:"
                    readyText: ""
                    notReadyText: "None"
                }
            }
        }
    }
}