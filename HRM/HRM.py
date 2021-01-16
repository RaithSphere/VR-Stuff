# Copyright 2020 by RaithSphere
# With thanks to Ryuvi
# All rights reserved.
# This file is part of the NeosVR-HRM,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import argparse
import configparser
import logging
import math
import os
import socket
import statistics
import sys
import threading
import time
from sys import platform

import pexpect
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

# For windows we are using BleakClient
if platform == "win32" or platform == "win64":
    from bleak import BleakClient
    from bleak import discover
    import asyncio

    HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
    BT_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

datafile = open("../storage/hrbt.txt", "w")

logging.basicConfig(format="%(asctime)-15s  %(message)s")
log = logging.getLogger("HeartRateLogger")

FinalSamples = 24

HR = -1
HRV = 0
RRAvg = [0 for i in range(FinalSamples)]
bt = -1
ct = False
connected = False

TwentyfourBeatAvg = [0 for i in range(FinalSamples * 2)]

log.setLevel(logging.INFO)
log.info("Starting Script")


class SimpleEcho(WebSocket):
    def handleMessage(self):
        hrbt = open("../storage/hrbt.txt", "r")
        data = hrbt.read()
        self.sendMessage(data)
        hrbt.close()

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


def parse_args():
    """
    Command line argument parsing
    """
    parser = argparse.ArgumentParser(
        description="Bluetooth heart rate monitor data logger"
    )
    parser.add_argument(
        "-mac",
        metavar="MAC",
        type=str,
        help="MAC address of BLE device (default: auto-discovery)",
    )
    parser.add_argument("-battery", action="store_true", help="Check battery level")
    parser.add_argument(
        "-g",
        metavar="PATH",
        type=str,
        help="gatttool path (default: system available)",
        default="gatttool",
    )
    parser.add_argument(
        "-H",
        metavar="HR_HANDLE",
        type=str,
        help="Gatttool handle used for HR notifications (default: none)",
    )
    parser.add_argument("-v", action="store_true", help="Verbose output")
    parser.add_argument("-d", action="store_true", help="Enable debug of gatttool")
    parser.add_argument("-port", action="store_true", help="Set the port")
    parser.add_argument(
        "-s", action="store_true", help="Scan for bluetooth devices - Windows only"
    )
    parser.add_argument(
        "-a", action="store_true", help="Get List of services - Windows Only"
    )

    confpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Config.conf")
    if os.path.exists(confpath):

        config = configparser.ConfigParser()
        config.read([confpath])
        config = dict(config.items("config"))

        # We compare here the configuration given in the config file with the
        # configuration of the parser.
        arguments = vars(parser.parse_args([]))
        err = False
        for key in config.keys():
            if key not in arguments:
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

    global addr
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
        main_linux(args.mac, args.g, args.battery, args.H, args.d)


def connect(windows):
    connected = True
    windows.run_until_complete(main_windows(args.mac))


async def main_windows(address=None):
    async with BleakClient(address) as client:
        log.info("Connected, streaming data...")

        await client.start_notify(HR_UUID, processhr)

        while True:
            global bt, ct

            bt = int.from_bytes(await client.read_gatt_char(BT_UUID), byteorder="big")
            writeout(None, None, bt, ct)
            await asyncio.sleep(1.0)


def processhr(s, d):
    byte0 = d[0]
    res = {"hrv_uint8": (byte0 & 1) == 0}
    sensor_contact = (byte0 >> 1) & 3

    global ct

    if sensor_contact == 2:
        res["sensor_contact"] = "No contact detected"
        ct = False
    elif sensor_contact == 3:
        res["sensor_contact"] = "Contact detected"
        ct = True
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
            TwentyfourBeatAvg.insert(0, i)
            del TwentyfourBeatAvg[-1]

        global RRAvg
        for i in range(FinalSamples):
            n = i * 2
            nextn = (
                TwentyfourBeatAvg[n + 1]
                if TwentyfourBeatAvg[n + 1] != 0
                else TwentyfourBeatAvg[n]
            )
            RRAvg[i] = pow(TwentyfourBeatAvg[n] - nextn, 2)

        HRV = math.sqrt(statistics.mean(RRAvg))

    writeout(res["hr"], HRV, None, None)


def main_linux(
        addr=None,
        gatttool="gatttool",
        check_battery=False,
        hr_handle=None,
        debug_gatttool=False,
):
    """
    main routine to which orchestrates everything
    """
    hr_ctl_handle = None
    retry = True
    global ct, bt, gt
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
                bt = str(int(battery_level, 16))
            except pexpect.TIMEOUT:
                log.error("Couldn't read battery level.")

        if hr_handle is None:
            # We determine which handle we should read for getting the heart rate
            # measurement characteristic.
            gt.sendline("char-desc")

            while 1:
                try:
                    gt.expect(
                        r"handle: (0x[0-9a-f]+), uuid: ([0-9a-f]{8})", timeout=60
                    )  # Had to increase the timeout from 10 for Wahoo Tickr X
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

            if hr_handle is None:
                log.error("Couldn't find the heart rate measurement handle?!")
                return

        if hr_ctl_handle:
            # We send the request to get HRM notifications
            log.info("Starting Heart Data Collection Process")
            gt.sendline("char-write-req " + hr_ctl_handle + " 0100")

        # Time period between two measures. This will be updated automatically.
        period = 1.0
        last_measure = time.time() - period
        hr_expect = "Notification handle = " + hr_handle + " value: ([0-9a-f ]+)"

        while 1:
            try:
                gt.expect(hr_expect, timeout=10)

            except pexpect.TIMEOUT:
                # If the timer expires, it means that we have lost the
                # connection with the HR monitor
                log.warning("Connection lost with " + addr + ". Reconnecting.")
                writeout(0, 0, 0, 0)
                time.sleep(1)
                break

            except KeyboardInterrupt:
                writeout(0, 0, 0, 0)
                log.info("Received keyboard interrupt. Quitting cleanly.")
                retry = False
                clithread.join()
                break

            # We measure here the time between two measures. As the sensor
            # sometimes sends a small burst, we have a simple low-pass filter
            # to smooth the measure.
            tmeasure = time.time()
            period = period + 1 / 16.0 * ((tmeasure - last_measure) - period)
            last_measure = tmeasure

            # Get data from gatttool
            datahex = gt.match.group(1).strip()
            data = map(lambda x: int(x, 16), datahex.split(b" "))
            res = interpret(list(data))

            log.debug(res)
            writeout(None, None, bt, ct)

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
    res = {"hrv_uint8": (byte0 & 1) == 0}
    sensor_contact = (byte0 >> 1) & 3

    global ct

    if sensor_contact == 2:
        res["sensor_contact"] = "No contact detected"
        ct = False
    elif sensor_contact == 3:
        res["sensor_contact"] = "Contact detected"
        ct = True
    else:
        res["sensor_contact"] = "Sensor contact not supported"

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
            TwentyfourBeatAvg.insert(0, i)
            del TwentyfourBeatAvg[-1]
        global RRAvg
        for i in range(FinalSamples):
            n = i * 2
            nextn = (
                TwentyfourBeatAvg[n + 1]
                if TwentyfourBeatAvg[n + 1] != 0
                else TwentyfourBeatAvg[n]
            )
            RRAvg[i] = pow(TwentyfourBeatAvg[n] - nextn, 2)
        HRV = math.sqrt(statistics.mean(RRAvg))

    writeout(res["hr"], HRV, None, None)

    return res


def writeout(hr, hrv, battery, contact):
    if hr is None and hrv is None and battery is None and contact is None:
        datafile.seek(0)
        datafile.write(str("0000.00000000.0000.0"))
        datafile.truncate()
    else:
        datafile.seek(13 if hr is None else 0)
        datafile.write(
            ".{:4s}.{:1s}".format(str(battery), "1" if contact is True else "0")
            if hr is None
            else "{:4s}.{:8.4f}".format(str(hr), hrv)
        )


async def searchbt():
    devices = await discover()

    """ Ignore HTC or Unknown Devices """
    Devicelist = ["HTC", "Unknown", "Apple", "Google"]
    KnownDevices = ["808S", "Polar", "XOSS"]

    for d in devices:
        dx = str(d)
        if not any(x in dx for x in Devicelist):

            if any(x in dx for x in KnownDevices):
                log.info("\033[92mPossible Tracker: %s \033[0m", dx)
            else:
                log.info(dx)


async def getservices(address: str):
    async with BleakClient(address) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))

        for service in client.services:
            log.info("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                log.info(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    log.info(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )


def http(webport):
    server = SimpleWebSocketServer("", webport, SimpleEcho)
    server.serveforever()


if __name__ == "__main__":

    args = parse_args()

    if args.s and platform == "win32" or platform == "win64":
        log.info("Starting bluetooth device scan")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(searchbt())
    elif args.a and platform == "win32" or platform == "win64":
        log.info("Getting Bluetooth Services list for %s" % args.mac)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getservices(args.mac))
    else:

        if os.path.isfile("Config.conf"):
            log.info("Found config file")
        else:
            log.error(
                "ERROR: Unable to find config file Config.conf, check the filename"
            )
            exit()

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

        log.info("SimpleEcho Started ws://%s:%s" % (local_ip, args.port))
        log.info(
            "\33[1m\33[94mNotice if you are running this locally on the same PC as NeosVR Connect to ws://localhost:%s\33[0m" % args.port)

        wthread = threading.Thread(target=http, args=(args.port,), daemon=True)
        wthread.start()

        if platform == "darwin":
            log.info("Detected Platform Darwin - Unsupported - Terminating Process")
            quit()
        elif platform == "win32" or platform == "win64":
            log.info("Detected Platform Windows - Experimental")
            log.info("Connecting to " + args.mac)
            loop = asyncio.get_event_loop()
            while not connected:
                try:
                    connect(loop)
                except KeyboardInterrupt:
                    print("Ending...")
                    datafile.close()
                    break
                except Exception as e:
                    print(e)
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
