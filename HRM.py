# Copyright 2020 by RaithSphere
# With thanks to Ryuvi
# All rights reserved.
# This file is part of the NeosVR-HRM,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import os
import sys
import time
import logging
import pexpect
import math
import argparse
import configparser
import statistics
import threading
import socket
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from sys import platform

# For windows we are using BleakClient 
if platform == "win32" or platform == "win64":
   from bleak import BleakClient
   from bleak import _logger as logger
   import asyncio
   HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
   BT_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

datafile = open("hrbt.txt","w")

logging.basicConfig(format="%(asctime)-15s  %(message)s")
log = logging.getLogger("HeartRateLogger")

FinalSamples = 24

HR = -1
HRV = 0
RRAvg = [0 for i in range(FinalSamples)]
BT = -1
CT = False
TwentyfourBeatAvg = [0 for i in range(FinalSamples*2)]

log.setLevel(logging.INFO)
log.info("Starting Script")

if os.path.isfile('Config.conf'):
    log.info("Found config file")
else:
    log.error("ERROR: Unable to find config file Config.conf, check the filename")
    exit()

class SimpleEcho(WebSocket):

    def handleMessage(self):
        hrbt = open("hrbt.txt","r")
        data = hrbt.read()
        self.sendMessage(data)
        hrbt.close()

    def handleConnected(self):
        log.info(self.address, 'connected')

    def handleClose(self):
        log.info(self.address, 'closed')


def parse_args():
    """
    Command line argument parsing
    """
    parser = argparse.ArgumentParser(description="Bluetooth heart rate monitor data logger")
    parser.add_argument("-m", metavar='MAC', type=str, help="MAC address of BLE device (default: auto-discovery)")
    parser.add_argument("-b", action='store_true', help="Check battery level")
    parser.add_argument("-g", metavar='PATH', type=str, help="gatttool path (default: system available)", default="gatttool")
    parser.add_argument("-H", metavar='HR_HANDLE', type=str, help="Gatttool handle used for HR notifications (default: none)")
    parser.add_argument("-v", action='store_true', help="Verbose output")
    parser.add_argument("-d", action='store_true', help="Enable debug of gatttool")
    parser.add_argument("-p", action='store_true', help="Set the port")


    confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Config.conf")
    if os.path.exists(confpath):

        config = configparser.ConfigParser()
        config.read([confpath])
        config = dict(config.items("config"))

        # We compare here the configuration given in the config file with the
        # configuration of the parser.
        args = vars(parser.parse_args([]))
        err = False
        for key in config.keys():
            if key not in args:
                log.error("Configuration file error: invalid key '" + key + "'.")
                err = True
        if err:
            sys.exit(1)

        parser.set_defaults(**config)

    return parser.parse_args()

def get_ble_hr_mac():
    """
    Scans BLE devices and returs the address of the first device found.
    """

    while 1:
        log.info("Trying to find a BLE device")
        hci = pexpect.spawn("hcitool lescan")
        try:
            hci.expect("([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", timeout=20)
            addr = hci.match.group(0)
            hci.close()
            break

        except pexpect.TIMEOUT:
            time.sleep(20)
            continue

        except KeyboardInterrupt:
            log.info("Received keyboard interrupt. Quitting cleanly.")
            hci.close()
            return None

    # We wait for the 'hcitool lescan' to finish
    time.sleep(1)
    return addr

def cli():
    """
    Entry point for the command line interface
    """
    log.info("Starting CLI Thread")

    if platform == "linux" or platform == "linux2":
        log.info("Detected Platform Linux")
        main_linux(args.m, args.g, args.b, args.H, args.d)

def connect(loop):
	loop.run_until_complete(main_windows(args.m))

async def main_windows(address=None):
	async with BleakClient(address) as client:
		log.info("Connected, steaming data...")

		await client.start_notify(HR_UUID,processhr)

		while True:
			global BT
			global CT

			BT = int.from_bytes(await client.read_gatt_char(BT_UUID), byteorder = "big")
			writeout(None,None,BT,CT)
			await asyncio.sleep(1.0)

		await asyncio.sleep(86400.00)

		await client.stop_notify(HR_UUID)

def processhr(s,d):
	byte0 = d[0]
	res = {}
	res["hrv_uint8"] = (byte0 & 1) == 0
	sensor_contact = (byte0 >> 1) & 3

	global CT

	if sensor_contact == 2:
		res["sensor_contact"] = "No contact detected"
		CT = False
	elif sensor_contact == 3:
		res["sensor_contact"] = "Contact detected"
		CT = True
	else:
		res["sensor_contact"] = "Sensor contact not supported"

	res["ee_status"] = ((byte0 >> 3) & 1) == 1
	res["rr_interval"] = ((byte0 >> 4) & 1) == 1

	if res["hrv_uint8"]:
		res["hr"] = d[1]
		i = 2
	else:
		res["hr"] = (d[2] << 8) | d[1]
		i = 3

	if res["ee_status"]:
		res["ee"] = (d[i + 1] << 8) | d[i]
		i += 2

	if res["rr_interval"]:
		res["rr"] = []
		while i < len(d):
			# Note: Need to divide the value by 1024 to get in seconds
			res["rr"].append((d[i + 1] << 8) | d[i])
			i += 2

	global HRV
	if res["rr_interval"]:
		for i in res["rr"]:
			TwentyfourBeatAvg.insert(0,i)
			del TwentyfourBeatAvg[-1]

		global RRAvg
		for i in range(FinalSamples):
			n = i*2
			nextn = TwentyfourBeatAvg[n+1] if TwentyfourBeatAvg[n+1] != 0 else TwentyfourBeatAvg[n]
			RRAvg[i] = pow(TwentyfourBeatAvg[n]-nextn,2)

		HRV = math.sqrt(statistics.mean(RRAvg))

	writeout(res["hr"],HRV,None,None)

def main_linux(addr=None, gatttool="gatttool", check_battery=False, hr_handle=None, debug_gatttool=False):
    """
    main routine to which orchestrates everything
    """
    hr_ctl_handle = None
    retry = True
    while retry:

        while 1:
            log.info("Establishing connection to " + addr)
            gt = pexpect.spawn(gatttool + " -b " + addr + " -t random --interactive")
            if debug_gatttool:
                gt.logfile = sys.stdout

            gt.expect(r"\[LE\]>")
            gt.sendline("connect")

            try:
                i = gt.expect(["Connection successful.", r"\[CON\]"], timeout=30)
                if i == 0:
                    gt.expect(r"\[LE\]>", timeout=30)

            except pexpect.TIMEOUT:
                log.info("Connection timeout. Retrying.")
                continue

            except KeyboardInterrupt:
                log.info("Received keyboard interrupt. Quitting cleanly.")
                retry = False
                break
            break

        if not retry:
            break

        log.info("Connected to " + addr)

        if check_battery:
            gt.sendline("char-read-uuid 00002a19-0000-1000-8000-00805f9b34fb")
            try:
                gt.expect("value: ([0-9a-f]+)")
                battery_level = gt.match.group(1)
                log.info("Battery level: " + str(int(battery_level, 16)))
                BT = str(int(battery_level, 16))
            except pexpect.TIMEOUT:
                log.error("Couldn't read battery level.")

        if hr_handle == None:
            # We determine which handle we should read for getting the heart rate
            # measurement characteristic.
            gt.sendline("char-desc")

            while 1:
                try:
                    gt.expect(r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=60)  # Had to increase the timeout from 10 for Wahoo Tickr X
                except pexpect.TIMEOUT:
                    break
                handle = gt.match.group(1).decode()
                uuid = gt.match.group(2).decode()

                if uuid == "00002902" and hr_handle:
                    log.debug("Scanning 00002902 for hr_ctl_handle")
                    hr_ctl_handle = handle
                    break

                elif uuid == "00002a37":
                    log.debug("Scanning 00002a37 for hr_handle")
                    hr_handle = handle

            if hr_handle == None:
                log.error("Couldn't find the heart rate measurement handle?!")
                return

        if hr_ctl_handle:
            # We send the request to get HRM notifications
            log.info("Starting Heart Data Collection Process")
            gt.sendline("char-write-req " + hr_ctl_handle + " 0100")

        global CT
        writeout(None,None,BT,CT)

        # Time period between two measures. This will be updated automatically.
        period = 1.
        last_measure = time.time() - period
        hr_expect = "Notification handle = " + hr_handle + " value: ([0-9a-f ]+)"

        while 1:
            try:
                gt.expect(hr_expect, timeout=10)

            except pexpect.TIMEOUT:
                # If the timer expires, it means that we have lost the
                # connection with the HR monitor
                log.warn("Connection lost with " + addr + ". Reconnecting.")
                writeout(0,0,0,0)
                time.sleep(1)
                break

            except KeyboardInterrupt:
                writeout(0,0,0,0)
                log.info("Received keyboard interrupt. Quitting cleanly.")
                retry = False
                clithread.join()
                break

            # We measure here the time between two measures. As the sensor
            # sometimes sends a small burst, we have a simple low-pass filter
            # to smooth the measure.
            tmeasure = time.time()
            period = period + 1 / 16. * ((tmeasure - last_measure) - period)
            last_measure = tmeasure

            # Get data from gatttool
            datahex = gt.match.group(1).strip()
            data = map(lambda x: int(x, 16), datahex.split(b' '))
            res = interpret(list(data))

            log.debug(res)

    # We quit close the BLE connection properly
    gt.sendline("quit")
    try:
        gt.wait()
    except:
        pass

def interpret(data):
    """
    data is a list of integers corresponding to readings from the BLE HR monitor
    """

    byte0 = data[0]
    res = {}
    res["hrv_uint8"] = (byte0 & 1) == 0
    sensor_contact = (byte0 >> 1) == 8

    global CT

    if sensor_contact == 2:
        res["sensor_contact"] = "No contact detected"
        CT = False
    elif sensor_contact == 3:
        res["sensor_contact"] = "Contact detected"
        CT = True
    else:
        res["sensor_contact"] = "Sensor contact not supported"


    CT = sensor_contact

    res["ee_status"] = ((byte0 >> 3) & 1) == 1
    res["rr_interval"] = ((byte0 >> 4) & 1) == 1

    if res["hrv_uint8"]:
        res["hr"] = data[1]
        i = 2
    else:
        res["hr"] = (data[2] << 8) | data[1]
        i = 3

    if res["ee_status"]:
        res["ee"] = (data[i + 1] << 8) | data[i]
        i += 2

    if res["rr_interval"]:
        res["rr"] = []
        while i < len(data):
            # Note: Need to divide the value by 1024 to get in seconds
            res["rr"].append((data[i + 1] << 8) | data[i])
            i += 2

    global HRV
    if res["rr_interval"]:
       for i in res["rr"]:
                TwentyfourBeatAvg.insert(0,i)
                del TwentyfourBeatAvg[-1]
       global RRAvg
       for i in range(FinalSamples):
                n = i*2
                nextn = TwentyfourBeatAvg[n+1] if TwentyfourBeatAvg[n+1] != 0 else TwentyfourBeatAvg[n]
                RRAvg[i] = pow(TwentyfourBeatAvg[n]-nextn,2)
       HRV = math.sqrt(statistics.mean(RRAvg))

    writeout(res["hr"],HRV,None,None)

    return res

def writeout(hr,hrv,bt,ct):
	if hr is None and hrv is None and bt is None and ct is None:
		datafile.seek(0)
		datafile.write(str("0000.00000000.0000.0"))
		datafile.truncate()
	else:
		datafile.seek(13 if hr is None else 0)
		datafile.write(".{:4s}.{:1s}".format(str(bt),"1" if ct is True else "0") if hr is None else "{:4s}.{:8.4f}".format(str(hr),hrv))

def http(webport):
    server = SimpleWebSocketServer('', webport, SimpleEcho)
    server.serveforever()

if __name__ == "__main__":

    args = parse_args()

    if args.g != "gatttool" and not os.path.exists(args.g):
        log.critical("Couldn't find gatttool path!")
        sys.exit(1)

    # Increase verbose level
    if args.v:
        log.setLevel(logging.DEBUG)
        log.info("Log level set to DEBUG")
    else:
        log.setLevel(logging.INFO)
        log.info("Log Level set to INFOMATIVE")

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    log.info("SimpleEcho Started ws://%s:%s" % (local_ip, args.p))
	
    wthread = threading.Thread(target=http, args=(args.p,), daemon=True)
    wthread.start()


    if platform == "darwin":
        log.info("Detected Platform Darwin - Unsupported - Terminating Process")
        quit()
    elif platform == "win32" or platform == "win64":
        log.info("Detected Platform Windows - Experimental")
        log.info("Connecting to " + args.m)
        loop = asyncio.get_event_loop()
        connect(loop)
    elif platform == "linux" or platform == "linux2":
        clithread = threading.Thread(target=cli, daemon=True)
        clithread.start()

    while True:
        time.sleep(10)
        user_input = input("[Bluetooth Control]: ")

        if user_input == "quit":
            log.info("Exiting HRM")
            exit(0)
        elif user_input == "help":
            log.info("System Commands")
            log.info("---------------")
            log.info("Quit - Exit the program and terminate process")
            log.info("Help - Shows this help ")
        else:
            print("This is not a correct command.")
