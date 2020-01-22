import os, platform,sys

#loads FreeCAD 0.18 path in Windows, too support linux soon
def LOADPATH():
    computer = platform.architecture()
    if computer[0] == '32bit':
        try:
            sys.path.append(os.environ["PROGRAMFILES"]+"/FreeCAD 0.18/bin")
        except Exception("Misconfigured, Not Installed, or not FreeCAD 0.18"):
            print("Path not found")
            exit(-1)
    elif computer[0] == '64bit':
        try:
            sys.path.append(os.environ["ProgramW6432"]+"/FreeCAD 0.18/bin")
        except Exception("Misconfigured, Not Installed, or not FreeCAD 0.18"):
            print("Path not found")
            exit(-1)
    else:
        raise Exception("Unsupported")
        exit(-1)

#engine profile .txt -> list array
import csv
class Parser():

    def __init__(self, datafile: str):
        csv_reader = csv.reader(open(datafile, "r"), delimiter = ",")
        f = []
        for row in csv_reader:
            f.append(row)
        index1 = 0
        while index1 < len(f):
            index2 = 0
            while index2 < len(f[index1]):
                f[index1][index2] = float(f[index1][index2])
                index2 += 1
            index1 += 1
        self.f = f

    def getPoints(self):
        return self.f

#geometry functions
def translate(array: list, distx=0.0, disty=0.0):
    c = array.copy()
    def translatept(point, distx, disty):
        assert len(point) == 2
        return [point[0] + distx, point[1] + disty]
    index = 0

    while index < len(array):
        #print("{0}, {1}".format(array[index], translatept(array[index], distx, disty)))
        array[index] = translatept(array[index], distx, disty)
        #print(array[index])
        index += 1
        assert c != array
    return array

def resize(array:list, distx=0.0, disty=0.0):
    c = array.copy()

    def translatept(point, distx, disty):
        assert len(point) == 2
        return [point[0] * distx, point[1] * disty]

    index = 0
    while index < len(array):
        #print("{0}, {1}".format(array[index], translatept(array[index], distx, disty)))
        array[index] = translatept(array[index], distx, disty)
        # print(array[index])
        index += 1
        assert c != array
    return array

#debug visualizations
import matplotlib.pyplot as plt
def plot(collections: list):
    x = []
    y = []
    for sublist in collections:
        for point in sublist:
            x.append(point[0])
            y.append(point[1])
    plt.scatter(x=x, y=y)
    plt.show()

#part geometries
def createEnginePoints(datafile:str, factor = 0.0):
    rocketCEAprofile = Parser(datafile=datafile).getPoints()
   # assert rocketCEAprofile is list
    assert len(rocketCEAprofile) > 0
    assert len(rocketCEAprofile[0]) > 0
    startx = abs(rocketCEAprofile[0][0])
    starty = abs(rocketCEAprofile[0][1])
    innerprofile = resize(translate(array=rocketCEAprofile.copy(), distx=startx), distx=factor, disty=factor)
    #assert innerprofile != rocketCEAprofile
    outerprofile = resize(translate(array=rocketCEAprofile.copy(), distx=startx, disty=starty), distx=factor, disty=factor)
    assert innerprofile != outerprofile
    lineleft = [
        innerprofile[0],
        outerprofile[0]
    ]
    lineright = [
        innerprofile[-1],
        outerprofile[-1]
    ]
    return {
        "innerprofile":innerprofile,
        "outerprofile":outerprofile,
        "lineleft":lineleft,
        "lineright":lineright
    }

LOADPATH()
#build the part
import FreeCAD, Part, Draft
from FreeCAD import Base
#freecad automated functions
#creates list of freecad vectors
def makeVectors(array: list):
    vectorList = []
    for point in array:
        vectorList.append(Base.Vector(point[0], point[1], 0))

    return vectorList


DEFAULTSAVEPATH = "C:\\users\\jonathan martini\\desktop\\"
def buildNozzle(points: dict, saveas: str = DEFAULTSAVEPATH+"defaultREngine.stp"):
    vec = makeVectors(points["innerprofile"])
    vec2 = makeVectors(points["outerprofile"])
    vec3 = makeVectors(points["lineleft"])
    vec4 = makeVectors(points["lineright"])
    poly1 = Part.makePolygon(vec)
    poly2 = Part.makePolygon(vec2)
    poly3 = Part.makePolygon(vec3)
    poly4 = Part.makePolygon(vec4)
    wire = Part.Wire([poly1,poly2,poly3,poly4])
    print(wire.isClosed())
    face = Part.Face(wire)
    solid = face.revolve(Base.Vector(1,0,0), Base.Vector(360,0,0))
    solid.exportStep(saveas)



if __name__ == "__main__":

    geometry = createEnginePoints(datafile="profile.data", factor=3)
    #assert geometry["innerprofile"] != geometry["outerprofile"]
    #plot([
    #    geometry["innerprofile"],
     #   geometry["outerprofile"],
    #    geometry["lineleft"],
    #    geometry["lineright"]
    #])
    buildNozzle(geometry)





