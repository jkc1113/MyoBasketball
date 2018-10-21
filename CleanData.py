from ConnectToMySQL import FakeDatabase
from SnapshotDB import Movement,Snapshot
import jsonpickle

db = FakeDatabase('data.txt')
data = db.parseDataFromFile()

for mv in data:
    for snap in mv.snaps:
        if( not (snap.orientation and snap.emg_data and snap.gyroscope and
                 snap.acceleration and snap.roll and snap.pitch and snap.yaw ) ):
                 mv.snaps.remove(snap)


maxSnaps = 0
minSnaps = len(data[0].snaps)
for mv in data:
    t = len(mv.snaps)
    if t < minSnaps:
        minSnaps = t
    if t > maxSnaps:
        maxSnaps = t
print minSnaps
print maxSnaps

for mv in data:
    t = len(mv.snaps)
    clipLow = (t-minSnaps)/2 + (t-minSnaps)%2
    clipHigh = (t-minSnaps)/2
    mv.snaps = mv.snaps[clipLow:t-clipHigh]

with open('data.txt', 'w') as f:
    f.write(jsonpickle.encode(data))

maxSnaps = 0
minSnaps = len(data[0].snaps)
for mv in data:
    t = len(mv.snaps)
    if t < minSnaps:
        minSnaps = t
    if t > maxSnaps:
        maxSnaps = t
print minSnaps
print maxSnaps
