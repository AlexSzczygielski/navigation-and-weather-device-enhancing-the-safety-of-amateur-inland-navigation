import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    width: 80
    height: 80
    radius: 10
    color: root.selected ? "#2980b9" : "#2c3e50"

    property string iconSource: "../assets/camera100.svg"
    property int iconSize: 50
    property bool selected: false

    signal iconClicked()

    Image {
        id: iconImage
        source: root.iconSource
        width: root.iconSize
        height: root.iconSize
        anchors.centerIn: parent
        fillMode: Image.PreserveAspectFit
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.iconClicked()
    }
}