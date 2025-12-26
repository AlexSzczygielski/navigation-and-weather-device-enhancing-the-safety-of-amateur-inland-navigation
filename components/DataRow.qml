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
    property bool isReady: false
    property string descriptionText: "?"
    property string readyText: "?"
    property string notReadyText: "?"

    spacing: 8

    //Description label (text)
    Label{ 
        text: root.descriptionText
        Layout.alignment: Qt.AlignVCenter
    }

    //Data variable text
    Text {
        text: root.isReady ? root.readyText : root.notReadyText
    }
}