using System;
using System.Diagnostics;
using System.Text;
using System.Net.Sockets;
using System.Net;
using System;

namespace HeartRate
{
    internal class NeosVR
    {
        internal static void SendData(int bpm, ContactSensorStatus status, int[] rr)
        {
            byte[] dataBytes = Encoding.UTF8.GetBytes(bpm.ToString());

            var isDisconnected = status == ContactSensorStatus.Contact;

            int connection = Convert.ToInt32(isDisconnected);

            Debug.WriteLine($"NeosVR - {bpm,-4:D}.{rr[0],8:##0.0000}.0000.{connection}");

        }
    }

}