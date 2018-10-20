from ConnectToGoogleCloud import DBConnection
from SnapshotDB import Snapshot
import jsonpickle

class DBTest:
    def test1(self):
        s1 = Snapshot([1,1,1,1],[1,2,3,4,5,6,7,8],[1,2,3],[3,2,1],90,90,90)
        s2 = Snapshot([2,1,2,1],[1,2,3,4,5,6,7,8],[1,2,3],[3,2,1],45,45,45)
        s3 = Snapshot([1,1,3,2],[1,2,3,4,5,6,7,8],[1,2,3],[3,2,1],45,90,0)
        shot = [s1,s2,s3]

        database = DBConnection()
        database.storeMovement(shot,'Shot')

    def test2(self):
        database = DBConnection()
        movements = database.getMovements('Jordan')
        print jsonpickle.encode(shots)
test = DBTest()
test.test1()
test.test2()
