import logging
import asyncio
import platform
import math
import statistics

from bleak import BleakClient
from bleak import _logger as logger

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
BT_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

Connected = False

FinalSamples = 24

HR = -1
HRV = 0
RRAvg = [0 for i in range(FinalSamples)]
BT = -1
CT = False

datafile = open("hrbt.txt","w")

def processhr(s,d):
	byte0 = d[0]
	res = {}
	res["hrv_uint8"] = (byte0 & 1) == 0
	sensor_contact = (byte0 >> 1) == 8
	if sensor_contact:
		res["sensor_contact"] = "Contact detected"
	else:
		res["sensor_contact"] = "No contact detected"

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

	global CT
	CT = sensor_contact
	print (res["hr"]);
	writeout(res["hr"],HRV,None,None)

async def run(address):
	async with BleakClient(address) as client:
		x = await client.is_connected()
		print("Connected, steaming data...")

		await client.start_notify(HR_UUID,processhr)

		while True:
			global BT
			global CT

			BT = int.from_bytes(await client.read_gatt_char(BT_UUID), byteorder = "big")
			writeout(None,None,BT,CT)
			await asyncio.sleep(1.0)

		await asyncio.sleep(86400.00)

		await client.stop_notify(HR_UUID)

def connect(loop):
	Connected = True

	loop.run_until_complete(run(address))

if __name__ == "__main__":
	print("--Starting NeosHeart Data Collection Process--")

	import os

	os.environ["PYTHONASYNCIODEBUG"] = str(1)
	address = "FD:CF:5F:4C:74:83"

	TwentyfourBeatAvg = [0 for i in range(FinalSamples*2)]

	def writeout(hr,hrv,bt,ct):
		if hr is None and hrv is None and bt is None and ct is None:
			datafile.seek(0)
			datafile.write(str("0000.00000000.0000.0"))
			datafile.truncate()
		else:
			datafile.seek(13 if hr is None else 0)
			datafile.write(".{:4s}.{:1s}".format(str(bt),"1" if ct is True else "0") if hr is None else "{:4s}.{:8.4f}".format(str(hr),hrv))

	loop = asyncio.get_event_loop()

	writeout(None,None,None,None)

	while not Connected:
		try:
			connect(loop)
		except KeyboardInterrupt:
			print("Ending...")
			datafile.close()
			break
		except Exception as e:
			print(e)
