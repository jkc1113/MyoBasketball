class Snapshot:
    def __init__(self,orientation,emg_data,gyroscope,acceleration,roll,pitch,yaw):
        self.orientation = orientation
        self.emg_data = emg_data
        self.gyroscope = gyroscope
        self.acceleration = acceleration
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
