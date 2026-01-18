// weather_data_panel.qml
/*
Weather forecast data panel loaded inside main.qml.
Uses DataRow component from components/DataRow.qml.
*/
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "qrc:/components"

ColumnLayout {
    Layout.fillWidth: true
    Layout.fillHeight: true
    spacing: 12

    property string rectangleColor: "#00bfa5"
    property int borderWidth: 3
    property int firstColumnWidth: 200
    property int dataRowSpacing: 10
    property string notAvailableText: "N/A"
    property int coordsPrecision: 5

    Button{
        Layout.alignment: Qt.AlignHCenter
        text: "Start Weather API"
        onClicked: weather_backend.start_weather_worker()
    }
    
    // CURRENT WEATHER SECTION
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
                    text: "Current Weather"
                    font.bold: true
                    font.pointSize: 16
                }

                DataRow {
                    descriptionText: "Message:"
                    dataText: weather_backend.weather_data.message == '0' ? "Empty" :  weather_backend.weather_data.message
                }

                DataRow {
                    descriptionText: "Temperature:"
                    dataText: weather_backend.weather_data.current_temp ? weather_backend.weather_data.current_temp.toFixed(1) + " °C" : notAvailableText
                }

                DataRow {
                    descriptionText: "Feels Like:"
                    dataText: weather_backend.weather_data.current_feels_like ? weather_backend.weather_data.current_feels_like.toFixed(1) + " °C" : notAvailableText
                }

                DataRow {
                    descriptionText: "Condition:"
                    dataText: weather_backend.weather_data.current_condition ? weather_backend.weather_data.current_condition : notAvailableText
                }

                DataRow {
                    descriptionText: "Wind Speed:"
                    dataText: weather_backend.weather_data.current_wind ? weather_backend.weather_data.current_wind.toFixed(1) + " m/s" : notAvailableText
                }
            }
            ColumnLayout{
                Layout.alignment: Qt.AlignRight
                Label{
                    text: gnss_backend.gnss_data.runningStatus ? "GPS POSITION" : "GPS DATA NOT AVAILABLE - OPERATING ON LAST SESSION POSITION"
                }
                DataRow {
                    descriptionText: "City:"
                    dataText: weather_backend.weather_data.city_name ? weather_backend.weather_data.city_name : notAvailableText
                }
                DataRow {
                    descriptionText: "Country:"
                    dataText: weather_backend.weather_data.country ? weather_backend.weather_data.country : notAvailableText
                }
                
                DataRow{
                    descriptionText: "Latitude: " 
                    dataText: {
                        if(weather_backend.weather_data.lat) {
                            weather_backend.weather_data.lat >= 0 ? weather_backend.weather_data.lat.toFixed(coordsPrecision) + " N" : (-weather_backend.weather_data.lat).toFixed(coordsPrecision) + " S"
                        }
                        else {notAvailableText}
                    }
                }

                DataRow{
                    descriptionText: "Longitude:"
                    dataText: {
                        if(weather_backend.weather_data.lon) {
                            weather_backend.weather_data.lon >= 0 ? weather_backend.weather_data.lon.toFixed(coordsPrecision) + " E" : (-weather_backend.weather_data.lon).toFixed(coordsPrecision) + " W"
                        }
                        else {notAvailableText}
                    }
                }
            }
        }
    }

    // FORECAST SECTION
    Rectangle {
        color: "transparent"
        border.color: rectangleColor
        border.width: borderWidth
        Layout.fillWidth: true
        Layout.fillHeight: true

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: dataRowSpacing

            Label {
                text: "3-Hour Forecast"
                font.bold: true
                font.pointSize: 16
            }

            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                orientation: ListView.Vertical
                spacing: 10
                clip: true
                model: weather_backend.weather_data.forecast

                delegate: Rectangle {
                    width: 500
                    height: 50
                    color: "transparent"
                    Column{
                        width: parent.width
                        height: parent.height
                        spacing: 6
                        Label { text: modelData.dt_txt }
                        Row {
                            width: parent.width
                            height: parent.height
                            spacing: 6
                            Label {
                                text: "Wind: "
                                font.bold: true
                                font.pointSize: 12
                            }
                            DataRow {
                                descriptionText: "Wind Speed:"
                                dataText: modelData.wind ? modelData.wind.toFixed(1) + " m/s" : notAvailableText
                            }
                            
                            DataRow {
                                descriptionText: "Wind Direction:"
                                dataText: modelData.wind_deg ? modelData.wind_deg + "" : notAvailableText
                            }
                            
                            DataRow {
                                descriptionText: "Wind Gusts:"
                                dataText: modelData.wind_gust ? modelData.wind_gust.toFixed(1) + "m/s" : notAvailableText
                            }

                            DataRow {
                                descriptionText: "Temperature:"
                                dataText: modelData.temp ? modelData.temp.toFixed(1) + " °C" : notAvailableText
                            }
                        }
                    }
                }
            }
        }
    }
}