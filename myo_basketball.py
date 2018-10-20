from __future__ import print_function
from myo.utils import TimeInterval
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

  def output(self):
    if not self.interval.check_and_reset():
      return

    parts = []
    parts.append('orientation: ')
    if self.orientation:
      for comp in self.orientation:
          parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
    parts.append('\n')
    parts.append(str(self.pose).ljust(10))
    parts.append('\n')
    parts.append(self.gyroscope)
    parts.append('\n')
    parts.append(self.acceleration)
    parts.append('\n')
    parts.append('EMG: ' if self.emg_enabled else ' ')
    #parts.append('L' if self.locked else ' ')
    #parts.append(self.rssi or 'NORSSI')

    if self.emg:
      for comp in self.emg:
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
    self.orientation = event.orientation
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



if __name__ == '__main__':
  myo.init(sdk_path='./myosdk')
  hub = myo.Hub()
  listener = Listener()
  while hub.run(listener.on_event, 50):
    print("\n")
    pass
