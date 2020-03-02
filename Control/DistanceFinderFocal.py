
class DistanceFinderFocal:

    def __init__(self, focal_length, real_length):
        self.FOCAL_LENGTH = focal_length
        self.real_length = real_length
        self.pixel_length = 1

    def setPixelLength(self,pixel_length):
        self.pixel_length = pixel_length

    def getPixelLength(self):
        return self.pixel_length

    def getDistance(self):
        distance = self.real_length * self.FOCAL_LENGTH / self.pixel_length
        return distance
