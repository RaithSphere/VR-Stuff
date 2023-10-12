# Heartrate Monitor [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`HRM` is a Python script that listens to data from Bluetooth Low Energy (BLE) heart rate sensors 

# Supported Devices
`NeosVR-HRM` should support any devices that use the service UUID "180d" and with characteristic "2a37", below is a list of known working devices that have been tested
<BR><B>Supported OS</B>: Windows and Linux - *(This code has been tested on a Raspberry Pi Zero W and confirmed working with that)*
  
__Windows is Classified as Experimental due to issues with the way windows handles bluetooth rather poorly, a new way is being researched, please see known issues__
  
For bluetooth if your PC lacks it I personally recommend the TP-LINK UB4A/UB400 [Amazon UK](https://www.amazon.co.uk/TP-LINK-UB4A-Bluetooth-Computer-Receiver/dp/B07YLDVM6B/) or [Amazon US](https://www.amazon.com/TP-Link-Bluetooth-Receiver-Controllers-UB400/dp/B07V1SZCY6/)

HRV = Heart Rate Varibility, CT = Contact Tracking

Device | US Link | UK Link | HR | CT | HRV | Placement
--- | --- | --- | --- | --- | --- | ---
XOSS Chest Strap | [Amazon US](https://www.amazon.com/XOSS-Monitor-Bluetooth-Wireless-Accessories/dp/B0822SFPTF/ref=sr_1_2?dchild=1&keywords=xoss+hrm&sr=8-2) | [Amazon UK](https://www.amazon.co.uk/XOSS-Monitor-Bluetooth-Waterproof-Computers/dp/B087LWS3BN/ref=sr_1_7?dchild=1&keywords=Xoss&qid=1604476420&sr=8-7) | ✔️ | ✔️ | ✔️ | Chest
CooSpo Heart Rate Monitor | --- | [Amazon UK](https://www.amazon.co.uk/CooSpo-Monitor-Bluetooth-Training-concept2/dp/B07SFTNXSD/) | ✔️ | ✔️ | ✔️| Chest
Polar H9 | [Amazon US](https://www.amazon.com/POLAR-H9-Heart-Rate-Sensor/dp/B08GHH4ZKL) |  [Amazon UK](https://www.amazon.co.uk/POLAR-Unisexs-Sensor-Bluetooth-Waterproof-Monitor/dp/B08411DQ96) | ✔️ | ✔️ | ✔️ | Chest
Polar H10 | [Amazon US](https://www.amazon.com/Polar-Heart-Rate-Monitor-Women/dp/B07PM54P4N/ref=sr_1_4?dchild=1&keywords=Polar+H9&sr=8-4) | [Amazon UK](https://www.amazon.co.uk/Polar-Monitor-Bluetooth-Waterproof-Sensor/dp/B07PM54P4N) | ✔️ | ✔️ | ✔️ | Chest
XOSS Heart Rate Monitor | [Amazon US](https://www.amazon.com/XOSS-Optical-Bluetooth-Wireless-Accessories/dp/B07H3QN6JC/ref=sr_1_13?dchild=1&keywords=XOSS&qid=1605379692&sr=8-13) | [Amazon UK](https://www.amazon.co.uk/XOSS-Monitor-Bluetooth-Smart-phone-Computer/dp/B07QLQM5VG/ref=sr_1_8?dchild=1&keywords=Xoss&qid=1605379649&sr=8-8) | ✔️ | ❌ | ❌ | Wrist
Action Free Arm Heart Rate Monitor | [Ali Express](https://www.aliexpress.com/item/4000900323749.html) | [Ali Express](https://www.aliexpress.com/item/4000900323749.html) | ✔️ | ✔️ | ❌ | Arm
Wellue VisualBeat | [Amazon US](https://www.amazon.com/Wellue-VisualBeat-Bluetooth-Exercise-Waterproof/dp/B07Y744XM8) | --- | ✔️ | ❌ | ❌ | Chest
Megene - H64 | [AliExpress](https://www.aliexpress.com/item/1005001484047949.html?spm=a2g0s.9042311.0.0.51fa4c4di3HBjE) | [AliExpress](https://www.aliexpress.com/item/1005001484047949.html?spm=a2g0s.9042311.0.0.51fa4c4di3HBjE) | ✔️ | ❌ | ❌| Chest

Video guide on python setup can be found here https://www.youtube.com/watch?v=aTiyrFsqIA4

# Requirements
* [Python 3.8.6](https://www.python.org/downloads/release/python-386/) Due to Bleak Requirements in Windows - Do not use versions higher
* Pip
* SimpleWebSocketServer
* pexpect
* bleak - Windows Only
* asyncio - Windows Only

# Instructions
* Download the latest release source code - [Here](https://github.com/RaithSphere/NeosVR-Stuff/releases) or Clone this repo: `git clone https://github.com/RaithSphere/NeosVR-Stuff`
* **When installing Python make sure to check Add Python to Path**
* For Linux - Run the command "python -m pip install -r requirements.txt"
* For Windows - Run the command "python -m pip install -r win-requirements.txt"
* Attach the HRM to its strap and put it on.
* Ensure no other applications or devices are connected (listening) to the HRM.
* Before you scan you need to rename Config.example to Config.conf
* Scan for your device MAC Address using **python HRM.py -s** (Windows Only).
* Add your MAC Address to Config.conf
* Start the script by doing **python3 HRM.py** (Linux) or **python HRM.py** (Windows)


# Config File
In the config file you need to set port & Bluetooth MAC, 
<BR>Leave Battery to 1 by default the websocket port is 8123 so you would connect to ws://myip:8123 - E.G ws://localhost:8123

# In Game Programming
The data output from the websocket is 4 bytes, 8 bytes, 4 bytes, 1 byte - HR, HRV, BATTERY, CONNECTION STATUS
Connection Status will return either 0 or 1, 1 being the sensor has a connection to the body.

# Contributions
If you want to Contribute please feel free to fork this repo

# Known Issues
`bleak.exc.BleakDotNetTaskError: System.Object''DisposedException: The object has been closed. (Exception from HRESULT: 0x80000013)`

__[Bleak Author]__ This is an error from the Windows Bluetooth system. I cannot do anything about it I am afraid. If the object has been disposed in the OS code, I cannot handle anything.<BR> 
Source : https://github.com/hbldh/bleak/issues/158

# Thanks and Other Stuff
Ryuvi for the Initial idea, websocket code and HRV
<BR>3x1t_5tyl3, Goodvibes and MattyK for being the initial testers.
<BR>Fabien (fg1) for the Intital code I based off
<BR>Carte Noir for the coffee for keeping me going

# License
Copyright 2020 RaithSphere.
[MIT Licensed](https://github.com/RaithSphere/VR-Stuff/blob/main/HRM/LICENSE).
