import jsonpickle

class FakeDatabase:
    def __init__(self, fname):
        self.fname = fname

    def parseDataFromFile(self):
        with open(self.fname, 'r') as f:
            return jsonpickle.decode(f.read())

    def dumpToFile(self,data):
        summedData = []
        with open(self.fname, 'r') as f:
            string = f.read()
            if len(string) is not 0:
                summedData = jsonpickle.decode(string)
        summedData.append(data)
        with open(self.fname, 'w') as f:
            f.write(jsonpickle.encode(summedData))
