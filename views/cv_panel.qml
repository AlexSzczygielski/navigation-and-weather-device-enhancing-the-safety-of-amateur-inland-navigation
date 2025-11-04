import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
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
        }

        Image {
            id: cv_roi_photo
            Layout.topMargin: 40
            //source: "qrc:/assets/model.png"
            source: ""
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 700
            Layout.preferredHeight: 450
        }
    }

    Connections {
        target: backend
        function onImageUpdated(path) {
            cv_roi_photo.source = "file://" + path
        }
    }
}