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
                            backend.run_cv()
                        }
                    }

                    Item {Layout.preferredHeight: 20}
                    Button {
                        id: cvPipeStop
                        text: "Stop CV"

                        onClicked: {
                            backend.run_cv()
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
            //source: "qrc:/assets/model.png"
            source: ""
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter 
            Layout.maximumWidth: 550
            Layout.maximumHeight: 400
        }
    }

    // ROI Creation update
    Connections {
        target: backend
        function onImageUpdated(base_64_str){
            cv_frame.source = "data:image/jpg;base64," + base_64_str
            maskStatus.isReady = true
        }
    }

    Component.onCompleted: {
        var img = backend.get_roi_img()
        if (img) {
            cv_frame.source = "data:image/jpg;base64," + img
            maskStatus.isReady = true
            cvInputIndicator.isReady = true
        }
    }
}