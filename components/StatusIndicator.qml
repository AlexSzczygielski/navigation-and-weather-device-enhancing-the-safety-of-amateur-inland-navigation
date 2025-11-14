//StatusIndicator.qml
//Text indicating if something is ready

import QtQuick 2.15
import QtQuick.Controls 2.15

Row {
    id: root
    spacing: 2

    property bool isReady: false
    property string readyText: "Ready"
    property string notReadyText: "Not ready"
    property color readyColor: "green"
    property color notReadyColor: "grey"
    property string readyIcon: "✅"
    property string notReadyIcon: "❌"
    property int fontSize: 14

    Text {
        id: statusText
        text: root.isReady ? (root.readyIcon + " " + root.readyText)
                           : (root.notReadyIcon + " " + root.notReadyText)

        color: root.isReady ? root.readyColor : root.notReadyColor
        font.pixelSize: root.fontSize
    }
}