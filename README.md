# NeosVR Heartrate Monitor

`NeosVR-HRM` is a Python script that listens to data from Bluetooth Low Energy (BLE) heart rate sensors 

## Requirements
* Python 3.6 Due to Bleak Requirements in Windows
* Pip
* SimpleWebSocketServer
* BleakClient - Windows Only
* asyncio - Windows Only


## Instructions
* Clone this repo: `git clone https://github.com/RaithSphere/NeosVR-HRM`
* Attach the HRM to its strap and put it on.
* Ensure no other applications or devices are connected (listening) to the HRM.
* Scan for your device MAC Address.
* Run the command "python -m pip install -r requirements.txt" - If you are using Linux make sure its Python 3.6 the command is linked to
* Add your MAC Address to Config.example and rename to Config.conf
* Start the script by doing **python3 HRM.py** or **python HRM.py**

## Windows Only
In addition to the above you will also need to run the command
* python -m pip install BleakClient asyncio

## Config File
In the config file you need to set port & Bluetooth MAC, 
Leave B to 1 by default the websocket port is 8123 so you would connect to ws://myip:8123 - E.G ws://localhost:8123

## LogiX
The data output from the websocket is 4 bytes, 8 bytes, 4 bytes, 1 byte - HR, HRV, BATTERY, CONNECTION STATUS
CONNECTION STATUS 2: "No contact detected"
CONNECTION STATUS 3: "Contact detected"
CONNECTION STATUS ANY OTHER: "Sensor contact not supported"

## Contributions

If you want to Contribute please feel free to fork this repo

## Thanks and Other Stuff
Ryuvi for the Initial idea, websocket code and HRV
<BR>Fabien (fg1) for the Intital code I based off
<BR>Carte Noir for the coffee for keeping me going

## License

Copyright 2018 Christopher Brown.
[MIT Licensed](https://chbrown.github.io/licenses/MIT/#2018).
