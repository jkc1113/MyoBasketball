from __future__ import print_function
from myo.utils import TimeInterval
from SnapshotDB import Snapshot
import myo
import myo.types
import sys
from ConnectToGoogleCloud import DBConnection
from myo.types.myo_math import Quaternion, Vector
import keyboard
import time
snap = []
class Listener(myo.DeviceListener):
    def __init__(self):
        self.interval = TimeInterval(None, 0.01)
        self.orientation = None
        self.pose = myo.Pose.rest
        self.emg_enabled = False
        self.locked = False
        self.rssi = None
        self.emg = None
        self.acceleration = None
        self.gyroscope = None
        self.quat = None
        self.yaw = None
        self.roll = None
        self.pitch = None
        self.snap = snap

    def output(self):
        if not self.interval.check_and_reset():
          return

    #     parts = []
    #     parts.append('orientation: ')
    #     if self.orientation:
    #       for comp in self.orientation:
    #           parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
    #     parts.append('\n')
    #     parts.append(str(self.pose).ljust(10))
    #     parts.append('\n')
    #     parts.append(self.gyroscope)
    #     parts.append('\n')
    #     parts.append(self.roll)
    #     parts.append('\n')
    #     parts.append(self.pitch)
    #     parts.append('\n')
    #     parts.append(self.yaw)
    #     parts.append('\n')
    #     parts.append(self.acceleration)
    #     parts.append('\n')
    #     parts.append('EMG: ' if self.emg_enabled else ' ')
    # #parts.append('L' if self.locked else ' ')
    # #parts.append(self.rssi or 'NORSSI')
    #
    #     if self.emg:
    #         for comp in self.emg:
    #             parts.append(str(comp).ljust(5))
    #         parts.append('\n')
    #         #print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')
    #         sys.stdout.flush()
        s1 = Snapshot(self.orientation, self.emg, self.gyroscope,
                      self.acceleration, self.roll, self.pitch, self.yaw)
        #print(s1)
        self.snap.append(s1)


    def on_connected(self, event):
        event.device.request_rssi()
        event.device.stream_emg(True)
        self.emg_enabled = True
        print("connected")
        time.sleep(1)
        print(3)
        time.sleep(1)
        print(2)
        time.sleep(1)
        print(1)
        time.sleep(1)
        print("shoot")

    def on_rssi(self, event):
        self.rssi = event.rssi
        self.output()

    def on_pose(self, event):
        self.pose = event.pose
        self.output()

    def on_orientation(self, event):
        temp = []
        self.orientation = event.orientation
        if(self.orientation):
            quaternion = Quaternion(self.orientation[0], self.orientation[1]
                         ,self.orientation[2], self.orientation[3])
            self.yaw = quaternion.yaw
            self.roll = quaternion.roll
            self.pitch = quaternion.pitch
            self.acceleration = event.acceleration
            self.gyroscope = event.gyroscope
            self.output()

    def on_emg(self, event):
        self.emg = event.emg
        self.output()

    def on_unlocked(self, event):
        self.locked = False
        self.output()

    def on_locked(self, event):
        self.locked = True
        self.output()

    def post_snap(self):
        post = DBConnection()
        print(len(self.snap))
        post.storeShot(self.snap, "Jake")

if __name__ == '__main__':
    myo.init(sdk_path='./myosdk')
    hub = myo.Hub()
    listener = Listener()
    x = False

    while hub.run(listener.on_event, 5):
        if(x is False):
            ms = time.time() * 1000
            x = True
        if((time.time() *1000)- ms > 2000):
            listener.post_snap()
            break
        pass
