# NeosVR Heartrate Monitor

[![PyPI](https://img.shields.io/pypi/pyversions/discord.py.svg)]()

Heart rate monitor system made for NeosVR using websockets

Before installing and running your own instance of NeosVR-HRM, you will first need to install the following:

* Python 3.6
* Pip

**Knowlege of LogiX in NeosVR is required to make this work**

## Using NeosVR Heartrate Monitor

In the config file you need to set port & Bluetooth MAC, leave B to 1 by default the websocket port is 8123 so you would connect to ws://myip:8123, the system can try and auto detect your BT MAC address for your monitor but isn't really advised

If you decide to use NeosVR Heartrate Monitor you start the script by doing **python3 HRM.py** 

The data output from the websocket is 4 bytes, 8 bytes, 4 bytes, 1 byte - HR, HRV, BATTERY, CONNECTION STATUS
<BR>CONNECTION STATUS 2: "No contact detected"
<BR>CONNECTION STATUS 3: "Contact detected"
<BR>CONNECTION STATUS ANY OTHER: "Sensor contact not supported"

## Contributions

If you want to Contribute to middy please feel free to fork this repo

## Thanks and Other Stuff
<BR>Ryuvi for the Initial idea, websocket code and HRV
<BR>Fabien (fg1) for the Intital code I based off
<BR>Carte Noir for the coffee for keeping me going
