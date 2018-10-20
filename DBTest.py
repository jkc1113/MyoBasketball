from ConnectToGoogleCloud import DBConnection
from SnapshotDB import Snapshot

s1 = Snapshot(1,1,1,1,[1,2,3,4,5,6,7,8],90,90,90)
s2 = Snapshot(2,1,2,1,[1,2,3,4,5,6,7,8],45,45,45)
s3 = Snapshot(1,1,3,2,[1,2,3,4,5,6,7,8],45,90,0)
shot = [s1,s2,s3]

database = DBConnection()
database.storeShot(shot,'Jordan')
