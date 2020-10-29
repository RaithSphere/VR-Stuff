import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
BT_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

Connected = False

datafile = open("hrbt.txt","w")

def processhr(s,d):
	HeartRate = int.from_bytes(d, byteorder = "big")
	writeout(HeartRate,None)
	print("HR:",HeartRate)

async def run(address):
	async with BleakClient(address) as client:
		x = await client.is_connected()
		print("Connected, steaming data...")

		await client.start_notify(HR_UUID,processhr)

		while True:
			Battery = int.from_bytes(await client.read_gatt_char(BT_UUID), byteorder = "big")
			print("BT:", Battery)
			writeout(None,Battery)
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
	address = "fA:c7:42:49:e3:14"

	HeartRate = -1
	Battery = -1	

	def writeout(hr,bt):
		if hr is None and not bt is None:
			datafile.seek(5)
			datafile.write("{:4s}".format(str(bt)))

		if bt is None and not hr is None:
			datafile.seek(0)
			datafile.write("{:4s}".format(str(hr)))

		if hr is None and bt is None:
			datafile.seek(0)
			datafile.write(str("0000.0000"))
			datafile.truncate()

	loop = asyncio.get_event_loop()

	writeout(None,None)

	while not Connected:
		try:
			connect(loop)
		except KeyboardInterrupt:
			print("Ending...")
			datafile.close()
			break
		except Exception as e:
			print(e)
