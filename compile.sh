#Compile script
#If linux,run in venv
if [[ "$(uname -s)" == "Linux" ]]; then
	source yolo/bin/activate
fi


rm qml_rc.py
pyrcc5 qml.qrc -o qml_rc.py
python3 main.py
