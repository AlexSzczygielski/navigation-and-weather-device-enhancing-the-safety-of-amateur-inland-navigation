//cv_create_roi_panel.qml
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
        spacing: 20
        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

        //Time and Date
        ColumnLayout {
            spacing: 2
            Layout.alignment: Qt.AlignHCenter

            Button {
                id: cv_roi
                text: "Create ROI"

                onClicked: {
                    backend.run_cv()
                }
            }

            StatusIndicator {
                id: maskStatus
                readyText: "Mask loaded"
                notReadyText: "Mask not loaded"
                notReadyIcon: ""
            }
        }

        Image {
            id: cv_roi_photo
            Layout.topMargin: 30
            //source: "qrc:/assets/model.png"
            source: ""
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 700
            Layout.preferredHeight: 400
        }
    }

    // ROI Creation update
    Connections {
        target: backend
        function onImageUpdated(base_64_str){
            cv_roi_photo.source = "data:image/jpg;base64," + base_64_str
            maskStatus.isReady = true
        }
    }

    Component.onCompleted: {
        var img = backend.get_roi_img()
        if (img) {
            cv_roi_photo.source = "data:image/jpg;base64," + img
            maskStatus.isReady = true
        }
    }
}