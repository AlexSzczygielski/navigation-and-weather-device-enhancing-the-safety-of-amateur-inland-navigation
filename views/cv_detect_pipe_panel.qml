import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

//Left Data
RowLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true

    //Middle Section
    ColumnLayout{
        Layout.fillWidth: true
        Layout.fillHeight: true
        spacing: 1
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        ColumnLayout {
            spacing: 2
            Layout.alignment: Qt.AlignHCenter

            Rectangle { 
                color: "transparent"
                border.color: "#00bfa5"
                implicitWidth: 170
                border.width: 3
                Layout.fillHeight: true 

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 6
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                    Item {Layout.preferredHeight: 40}
                    StatusIndicator {
                        id: maskStatus
                        readyText: "Mask loaded"
                        notReadyText: "Mask not loaded"
                        notReadyIcon: ""
                    }

                    Item {Layout.preferredHeight: 20}
                    StatusIndicator {
                        id: cvSysStatus
                        readyText: "CV system ready"
                        notReadyText: "CV system not ready"
                        notReadyIcon: "🚫"
                    }

                    Item {Layout.preferredHeight: 20}
                    StatusIndicator {
                        id: detectedPeopleStatus
                        readyText: "Detected People: "
                        notReadyText: "Detected People: 0"
                        notReadyIcon: ""
                        readyIcon: ""
                    }

                    Item {Layout.preferredHeight: 20}
                    StatusIndicator {
                        id: mobAlert
                        readyText: "Man Overboard!"
                        notReadyText: "No MOB Alert"
                        notReadyIcon: "💤"
                        readyIcon: "🚨"
                    }

                    Item {Layout.preferredHeight: 20}
                    Button {
                        id: cvPipeStart
                        text: "Start CV"

                        onClicked: {
                            cv_backend.run_cv_mob_detect_pipe()
                        }
                    }

                    Item {Layout.preferredHeight: 20}
                    Button {
                        id: cvPipeStop
                        text: "Stop CV"

                        onClicked: {
                            cv_backend.run_cv()
                        }
                    }
                    Item {Layout.fillHeight: true}
                }
            }
        }
    }

    ColumnLayout {
        spacing: 2
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        StatusIndicator {
            id: cvInputIndicator
            readyText: "CV Input: "
            notReadyText: "No CV Input"
            notReadyIcon: "💤"
            readyIcon: ""
            fontSize: 40
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
}