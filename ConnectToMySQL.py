import jsonpickle

class FakeDatabase:
    def __init__(self, fname):
        self.fname = fname

    def parseDataFromFile(self):
        with open(self.fname, 'r') as f:
            f.read
            return jsonpickle.decode(f.read())

    def dumpToFile(self,data):
        with open(self.fname, 'w') as f:
            f.write(jsonpickle.encode(data))
