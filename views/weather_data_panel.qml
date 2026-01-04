//weather_data_panel.qml
/*
Weather data panel loaded inside main.qml.
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
    property int firstColumnWidth: 230
    property string rectangleColor: "#00bfa5"
    property int divisionHeight: 5
    property int dataRowSpacing: 12
    property string notAvailableText: "API OFF"

    Button{
        anchors.centerIn: parent
        text: "Start Weather API"
        onClicked: weather_backend.start_weather_worker()
    }
}