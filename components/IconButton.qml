//IconButton.qml
import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root
    property int rectangleWidth: 80
    property int rectangleHeight: 80
    width: rectangleWidth
    height: rectangleHeight
    radius: 10

    property string backgroundColor: root.selected ? (nightMode ? "#1de9b6" : "#3498db")
                                                    : (nightMode ? "#144d4d" : "#2c3e50")
    color: backgroundColor

    property bool nightMode: false
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