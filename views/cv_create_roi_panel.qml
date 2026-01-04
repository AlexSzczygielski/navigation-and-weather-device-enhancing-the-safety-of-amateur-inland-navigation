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
                    cv_backend.run_cv_roi_pipe()
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
            source: cv_backend.cv_data.roiImageBase64 ? cv_backend.cv_data.roiImageBase64 : ""
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 700
            Layout.preferredHeight: 400
        }
    }
}