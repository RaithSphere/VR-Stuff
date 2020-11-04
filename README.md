# NeosVR Heartrate Monitor

`NeosVR-HRM` is a Python script that listens to data from Bluetooth Low Energy (BLE) heart rate sensors 

## Supported Devices
`NeosVR-HRM` should support any devices that use the service UUID "180d" and with characteristic "2a37", below is a list of known working devices that have been tested

Device | Picture | Link
--- | --- | ---
XOSS Chest Strap | --- | [Amazon US](https://www.amazon.com/XOSS-Monitor-Bluetooth-Wireless-Accessories/dp/B0822SFPTF/ref=sr_1_10?dchild=1&keywords=Xoss&qid=1604338218&sr=8-10&th=1) - [Amazon UK](https://www.amazon.co.uk/XOSS-Monitor-Bluetooth-Waterproof-Computers/dp/B087LWS3BN/ref=sr_1_7?dchild=1&keywords=Xoss&qid=1604476420&sr=8-7)
CooSpo Heart Rate Monitor | --- | [Amazon UK](https://www.amazon.co.uk/CooSpo-Monitor-Bluetooth-Training-concept2/dp/B07SFTNXSD/)
Polar H9 | --- |  [Amazon UK](https://www.amazon.co.uk/POLAR-Unisexs-Sensor-Bluetooth-Waterproof-Monitor/dp/B08411DQ96)
Polar H10 | --- | [Amazon UK](https://www.amazon.co.uk/Polar-Monitor-Bluetooth-Waterproof-Sensor/dp/B07PM54P4N)

## Requirements
* Python 3.6 Due to Bleak Requirements in Windows - Do not use versions higher
* Pip
* SimpleWebSocketServer
* pexpect
* BleakClient - Windows Only
* asyncio - Windows Only

## Instructions
* Clone this repo: `git clone https://github.com/RaithSphere/NeosVR-HRM`
* Attach the HRM to its strap and put it on.
* Ensure no other applications or devices are connected (listening) to the HRM.
* Scan for your device MAC Address using discover.py (Windows Only).
* Run the command "python -m pip install -r requirements.txt" - If you are using Linux make sure its Python 3.6 the command is linked to
* Add your MAC Address to Config.example and rename to Config.conf
* Start the script by doing **python3 HRM.py** or **python HRM.py**

## Windows Only
In addition to the above you will also need to run the command
* python -m pip install BleakClient asyncio

## Config File
In the config file you need to set port & Bluetooth MAC, 
<BR>Leave B to 1 by default the websocket port is 8123 so you would connect to ws://myip:8123 - E.G ws://localhost:8123

## LogiX
The data output from the websocket is 4 bytes, 8 bytes, 4 bytes, 1 byte - HR, HRV, BATTERY, CONNECTION STATUS
Connection Status will return either 0 or 1, 1 being the sensor has a connection to the body.

## Contributions
If you want to Contribute please feel free to fork this repo

## Thanks and Other Stuff
Ryuvi for the Initial idea, websocket code and HRV
<BR>3x1t_5tyl3, Goodvibes and MattyK for being the initial testers.
<BR>Fabien (fg1) for the Intital code I based off
<BR>Carte Noir for the coffee for keeping me going

## License

Copyright 2018 Christopher Brown.
[MIT Licensed](https://chbrown.github.io/licenses/MIT/#2018).