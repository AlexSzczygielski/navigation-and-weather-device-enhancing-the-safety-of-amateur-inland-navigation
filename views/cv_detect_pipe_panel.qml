import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

//Left Data
RowLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true
    property string rectangleColor: "#00bfa5"
    property int borderWidth: 3
    property int firstColumnWidth: 200
    property int dataRowSpacing: 10
    property string notAvailableText: "N/A"
    property int coordsPrecision: 5
    ColumnLayout{
        ColumnLayout{
            Layout.alignment: Qt.AlignVCenter
            Button {
                id: cvPipeStart
                text: "Start CV"

                onClicked: {
                    cv_backend.run_cv_mob_detect_pipe()
                }
            }
        }

        Rectangle {
            color: "transparent"
            border.color: rectangleColor
            border.width: borderWidth
            Layout.fillWidth: true
            Layout.preferredHeight: 200

            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: dataRowSpacing
                ColumnLayout {
                    Layout.alignment: Qt.AlignLeft
                    anchors.margins: 10
                    spacing: dataRowSpacing

                    Label {
                        text: "Computer Vision Module Status:"
                        font.bold: true
                        font.pointSize: 16
                    }

                    DataRow {
                        descriptionText: "Computer Vision System:"
                        dataText: cv_backend.cv_data.runningMobPipeStatus ? "Running" :  "OFF"
                    }

                    DataRow {
                        descriptionText: "Boat Deck Mask:"
                        dataText: cv_backend.cv_data.boatDeckMaskStatus ? "Ready" :  "Not Loaded"
                    }

                    DataRow {
                        descriptionText: "Detected People:"
                        dataText: cv_backend.cv_data.detectedPeople ? cv_backend.cv_data.detectedPeople :  "OFF"
                    }

                    RowLayout {
                        Label {
                            text: "MOB ALERT:"
                            font.bold: true
                            font.pointSize: 16
                        }
                        Label {
                            text: cv_backend.cv_data.mobAlarm ? "MAN OVERBOARD DETECTED" :  "NO"
                            font.bold: true
                            font.pointSize: 20
                        }
                    }

                }
            }
        }
    }

    Image {
        id: cv_frame
        Layout.topMargin: 30
        source: cv_backend.cv_data.mobFrameBase64 ? cv_backend.cv_data.mobFrameBase64 : ""
        fillMode: Image.PreserveAspectFit
        Layout.alignment: Qt.AlignHCenter 
        Layout.maximumWidth: 550
        Layout.maximumHeight: 400
    }
}