from __future__ import print_function
from myo.utils import TimeInterval
from SnapshotDB import Snapshot
import myo
import sys

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

  def output(self):
    if not self.interval.check_and_reset():
      return
    snap = []
    parts = []
    parts.append('orientation: ')
    if self.orientation:
      for comp in self.orientation:
          snap.append(comp)
          parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
    parts.append('\n')
    parts.append(str(self.pose).ljust(10))
    parts.append('\n')
    parts.append(self.gyroscope)
    parts.append('\n')
    parts.append(self.roll)
    parts.append('\n')
    parts.append(self.pitch)
    parts.append('\n')
    parts.append(self.yaw)
    parts.append('\n')
    parts.append(self.acceleration)
    parts.append('\n')
    parts.append('EMG: ' if self.emg_enabled else ' ')
    #parts.append('L' if self.locked else ' ')
    #parts.append(self.rssi or 'NORSSI')

    if self.emg:
      for comp in self.emg:
        snap.append(comp)
        parts.append(str(comp).ljust(5))
    parts.append('\n')
    print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')
    sys.stdout.flush()


  def on_connected(self, event):
    event.device.request_rssi()

  def on_rssi(self, event):
    self.rssi = event.rssi
    self.output()

  def on_pose(self, event):
    self.pose = event.pose
    event.device.stream_emg(True)
    self.emg_enabled = True
    self.output()

  def on_orientation(self, event):
    temp = []
    self.orientation = event.orientation
    self.quat = quat(self.orientation[0], self.orientation[1]
                     , self.orientation[2], self.orientation[3])
    if(self.orientation):
        self.quaternion = myo.Quaternion(self.quat)
        self.yaw = self.quaternion.yaw()
        self.roll = self.quaternion.roll()
        self.pitch = self.quaternion.pitch()


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

class quat:
    def __init__(self,x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.z = w

if __name__ == '__main__':
  myo.init(sdk_path='./myosdk')
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 50):
    print("\n")
    pass
