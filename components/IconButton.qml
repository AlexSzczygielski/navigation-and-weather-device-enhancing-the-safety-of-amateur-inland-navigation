import QtQuick 2.15
import QtQuick.Controls 2.15

ToolButton {
    id: root
    //properties
    property string iconSource: ""
    property int iconSize: 50 

    property bool selected: false

    signal iconClicked()

    //Icon setup
    icon.source: iconSource
    icon.width: iconSize
    icon.height: iconSize

    //Background setup
    background: Rectangle {
      color: root.selected ? "#2980b9" : "#2c3e50"
      radius: 10
    }
    
    onClicked: iconClicked()
}