import imageio
import random
import math
import numpy as np

def OutputPicture(name, data, width, height):
    result = []
    for i in range(height):
        buffer = []
        for j in range(width):
            buffer.append(Point(0, 0, 0, -1))
        result.append(buffer)

    currentPos = 0
    for arr1 in result:
        for i in range(len(arr1)):
            arr1[i] = data[currentPos].toArray()
            currentPos += 1

    imageio.imwrite(name, result)

def PartitionToData(partition, center):
    size = 0
    for p in partition:
        size += len(p)

    data = []
    for i in range(size):
        data.append([])

    for i in range(len(partition)):
        for point in partition[i]:
            data[point.index] = Point(center[i].x, center[i].y, center[i].z, point.index)
    return data


class Point:
    #x, y, z are RGB here but I wanted to phrase this as a general vectorspace
    def __init__(self, x, y, z, index):
        self.x = x
        self.y = y
        self.z = z
        self.index = index

    def distanceSquare(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

    def toArray(self):
        return [np.uint8(self.x), np.uint8(self.y), np.uint8(self.z)]

    def __add__(self, other):
        if (isinstance(other, self.__class__)):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z, -1)
        else:
            throw("invalid object tried to be added to point")

    def __mul__(self, other):
        return Point(self.x * other, self.y * other, self.z * other, self.index)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return "Point at %d, %d, %d, index: %d" % (self.x, self.y, self.z, self.index)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


arr = imageio.imread('Rainbow.png')

height  = len(arr)
width = len(arr[0])

data = []
currentPos = 0
for arr1 in arr:
    for RGB in arr1:
        data.append(Point(RGB[0], RGB[1], RGB[2], currentPos))
        currentPos += 1

print("Read in image with width: %d and height: %d, total lenth: %d" % (width, height, width * height))

k = 3
clusters = []
clusterCenter = []
oldClusterCenter = []
for i in range(k):
    clusters.append([])
    clusterCenter.append(Point(random.random() * 255, random.random() * 255, random.random() * 255, -1))
    oldClusterCenter.append(Point(0,0,0, -1))


cont = True
iteration = 0
while(cont):
    iteration += 1
    print ("Starting iteration %d" % (iteration))
    clusters = []
    for i in range(k):
        clusters.append([])

    cont = False
    for i in range(len(clusterCenter)):
        if (clusterCenter[i] != oldClusterCenter[i]):
            cont = True
            break;

    for x in data:
        smallestDistance = 100000000
        smallestIndex = -1

        for i in range(len(clusterCenter)):
            distance = x.distanceSquare(clusterCenter[i])
            if (distance < smallestDistance):
                smallestIndex = i
                smallestDistance = distance

        clusters[smallestIndex].append(x)

    error = 0
    for i in range(len(clusters)):
        sum = Point(0, 0, 0, -1)
        for x in clusters[i]:
            sum += x

        oldClusterCenter[i] = clusterCenter[i]
        clusterCenter[i] = (1/float(len(clusters[i]))) * sum

        for x in clusters[i]:
            error += math.sqrt(x.distanceSquare(clusterCenter[i]))

    print("current error %f" % (error))
    OutputPicture("Rainbowk%dI%d.png" % (k, iteration), PartitionToData(clusters, clusterCenter), width, height)
