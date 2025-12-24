//DataRow.qml
/*
Data Row is a reusable qml component showing description text
and data that is dependent on an input.
*/
import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

RowLayout{
    id: root

    //Component variables
    // Description Label
    property string descriptionText: "?"
    // Status Indicator - data field
    property bool ready: false
    property string readyText: "?"
    property string notReadyText: "?"
    property string readyIcon: ""
    property string notReadyIcon: ""

    spacing: 8

    //Description label (text)
    Label{ 
        text: root.descriptionText
        Layout.alignment: Qt.AlignVCenter
    }

    //Data variable text
    StatusIndicator {
        readyText: root.readyText
        notReadyText: root.notReadyText
        readyIcon: root.readyIcon
        notReadyIcon: root.notReadyIcon
    }
}