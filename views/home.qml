import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
//Left Data
RowLayout{
    Layout.fillWidth: true
    Layout.fillHeight: true

ColumnLayout{
    Layout.fillHeight: true
    spacing: 16
    Layout.preferredWidth: 150
    Dial {
        id: volumeDial
        from: 0
        value: 42
        to: 100
        stepSize: 1

        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: 128
        Layout.preferredHeight: 128
    }
}

// Divider
Rectangle { color: "#00bfa5"; implicitWidth: 2; Layout.fillHeight: true }

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

        Label {
            text: "12:00"
            font.pixelSize: 78
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        Label {
            text: "15/07/1410"
            font.pixelSize: 18
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }
    }

    Image {
        Layout.topMargin: 40
        source: "qrc:/assets/model.png"
        fillMode: Image.PreserveAspectFit
        Layout.alignment: Qt.AlignHCenter
        Layout.preferredWidth: 300
        Layout.preferredHeight: 300
    }
}

//Divider
Rectangle { color: "#00bfa5"; implicitWidth: 2; Layout.fillHeight: true }

ColumnLayout{
    Layout.fillHeight: true
    spacing: 16
    Layout.preferredWidth: 150
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