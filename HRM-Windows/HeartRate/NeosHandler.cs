using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using Windows.Devices.Bluetooth.GenericAttributeProfile;
using Windows.Devices.Enumeration;
using Windows.Storage.Streams;

namespace HeartRate
{
    internal class NeosVR
    {
        internal static void SendData(int bpm, ContactSensorStatus status)
        {
            byte[] dataBytes = Encoding.UTF8.GetBytes(bpm.ToString());

            var isDisconnected = status == ContactSensorStatus.Contact;

            int connection = Convert.ToInt32(isDisconnected);

            Debug.WriteLine($"NeosVR - {bpm}.00000000.0000.{connection}");

        }
    }

}