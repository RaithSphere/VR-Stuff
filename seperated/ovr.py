import sys
import time
import openvr

openvr.init(openvr.VRApplication_Overlay)
ids = []

leftId = openvr.VRSystem().getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_LeftHand)
rightId = openvr.VRSystem().getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_RightHand)


def to_percent(value):
    return str(value * 100)[0:2]


def writefile(left, right):
    datafile = open("../ovr.txt", "w")
    left = (to_percent(left))
    right = (to_percent(right))
    datafile.write("{:2s}.{:2s}".format(str(left), str(right)))
    datafile.close()


while True:
    overlay = openvr.IVROverlay()
    notification = openvr.IVRNotifications()
    left_battery = openvr.VRSystem().getFloatTrackedDeviceProperty(leftId, openvr.Prop_DeviceBatteryPercentage_Float)
    right_battery = openvr.VRSystem().getFloatTrackedDeviceProperty(rightId, openvr.Prop_DeviceBatteryPercentage_Float)

    writefile(left_battery, right_battery)

    time.sleep(60)
