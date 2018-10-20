
import myo
import time

myo.init(sdk_path='./myosdk/')

def main():
  hub = myo.Hub()
  listener = myo.ApiDeviceListener()
  with hub.run_in_background(listener.on_event):
    print("Waiting for a Myo to connect ...")
    device = listener.wait_for_single_device(2)
    if not device:
      print("No Myo connected after 2 seconds.")
      return
    print("Hello, Myo! Requesting RSSI ...")
    device.request_rssi()

    while hub.running and device.connected and not device.rssi :
      print("Waiting for RRSI...")
      time.sleep(0.001)
    print("RSSI:", device.rssi)

    print("Goodbye, Myo!")


def orientation():
    #myo.init(sdk_path='./myosdk/')
    #hub = myo.Hub()
    #listener = myo.DeviceListener()
    feed = myo.device_listener.Feed()
    hub = myo.Hub()
    hub.run(1000, feed)
    try:
        while True:
            myos = feed.get_connected_devices()
            if myos:
                print myos[0], myos[0].orientation
                time.sleep(0.5)
    finally:
        hub.stop(True)
        hub.shutdown()

    # try:
    #     device = listener.wait_for_single_device(2)
    #     if not device:
    #         print("No Myo connected after 2 seconds")
    #     print("Hello, Myo!")
    #     quat = None
    #     while hub.running and device.connected and myo.on_orientation_data:
    #         quat = device.orientation
    #     print('Orientation:', quat.x, quat.y, quat.z, quat.w)
    # finally:
    #     hub.shutdown()  # !! crucial

main()
orientation()
