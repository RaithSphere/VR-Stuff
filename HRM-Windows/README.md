# NeosVR Heartrate Monitor Windows Version

<B>WINDOWS 11 NOTE - ENABLE ADVANCED MODE ON BLUETOOTH DEVICES DISCOVERY!!!!</B>

`HRM-Windows` is a C# script that listens to data from Bluetooth Low Energy (BLE) heart rate sensors 

# Supported Devices
<BR><B>Supported OS</B>: Windows 
  
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

# Instructions
<BR>Pair your Heartrate Meter to Windows as you would any normal bluetooth device
<BR>The websocket port is 8123 so you would connect to ws://myip:8123 - E.G ws://localhost:8123

# Ingame Programming
The data output from the websocket is 4 bytes, 8 bytes, 4 bytes, 1 byte - HR, HRV, BATTERY, CONNECTION STATUS
Connection Status will return either 0 or 1, 1 being the sensor has a connection to the body.

# Contributions
If you want to Contribute please feel free to fork this repo

# Thanks and Other Stuff
Ryuvi for the Initial idea, websocket code and HRV
<BR>ThomFox for the basic windows code!
<BR>Carte Noir for the coffee for keeping me going

# License
Copyright 2022 RaithSphere.
[MIT Licensed](https://github.com/RaithSphere/VR-Stuff/blob/main/HRM/LICENSE).
