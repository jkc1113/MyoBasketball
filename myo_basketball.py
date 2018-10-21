from __future__ import print_function
from myo.utils import TimeInterval
from SnapshotDB import Snapshot
from SnapshotDB import Movement
import myo
import myo.types
import sys
from ConnectToMySQL import FakeDatabase
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

        s1 = Snapshot(self.orientation, self.emg, self.gyroscope,
                      self.acceleration, self.roll, self.pitch, self.yaw)
        #print(s1)
        if( s1.orientation and s1.emg and s1.gyroscope and
                 s1.acceleration and s1.roll and s1.pitch and s1.yaw ):
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

    def post_mov(self, data):
        post = FakeDatabase('data.txt')
        post.dumpToFile(data)

    def read_data(self):
        post = FakeDatabase('data.txt')
        return post.parseDataFromFile()


if __name__ == '__main__':
    myo.init(sdk_path='./myosdk')
    hub = myo.Hub()
    listener = Listener()
    collectingData = True
    while collectingData is True:
        listener.snap = []
        x = False
        while hub.run(listener.on_event, 5):
            if(x is False):
                ms = time.time() * 1000
                x = True
            if((time.time() *1000)- ms > 1000):
                break
            pass
        mov_type = raw_input("What did you do? (0-Shoot  1-BouncePass  2-ChestPass  3-OverheadPass  4-Showoff)")
        mov_type = int(mov_type)
        if mov_type < 5:
            listener.post_mov(Movement(listener.snap, mov_type))
            print('data added')
        collectingData = raw_input("Collect more data?(Y/N)") is 'Y'
