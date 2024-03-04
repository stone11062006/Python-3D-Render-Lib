#    Python-3D-Render-Lib Copyright (C) 2024  Hanchard Pierre
#
#    Python-3D-Render-Lib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Python-3D-Render-Lib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Python-3D-Render-Lib.  If not, see <https://www.gnu.org/licenses/>.

from Models.BasicObjects import Shape
import os

#this file must be in the same folder than the obj files

class CustomModel(Shape):

    def __init__(self, fileName:str, center:tuple, size=1, objectName:str="", color=(255, 255, 255), clockWiseRendering=True, lock=False):

        Shape.__init__(self, center, size, color, not clockWiseRendering, lock)
        self.size.y *= -1
        self.fileName = fileName
        path = os.path.abspath(os.path.dirname(__file__))
        file = open(path + "\\" + self.fileName, "r")
        if objectName == "":
            getData = True
        else:
            getData = False

        smallestFace = 100000000
        tempFaces = []

        for x in file:
            line = x
            line = line.rstrip()
            alphaStr = ""
            for m in line:
                if m.isalpha():
                    alphaStr = alphaStr + m
                if m == " ":
                    break
            if alphaStr == "o":
                if objectName != "":
                    if line == "o " + objectName:
                        getData = True
                    else:
                        getData = False
            
            if getData:
                if alphaStr == "v":
                    #print("vertex")
                    newVert = [p for p in range(3)]
                    i = -1
                    coord = ""
                    for l in line:
                        if l == " ":
                            if i != -1:
                                newVert[i] = float(coord) 
                            i += 1
                            coord = ""
                        else:
                            coord = coord + l
                    newVert[2] = float(coord) 
                    newVert[0] = newVert[0] * self.size.x + self.center.x
                    newVert[1] = newVert[1] * self.size.y + self.center.y
                    newVert[2] = newVert[2] * self.size.z + self.center.z
                    self.vertices.append(tuple(newVert))
                    print("v " + str(newVert))
                elif alphaStr == "vt":
                    #print("texture coord")
                    pass
                elif alphaStr == "f":
                    newFace = []
                    i = -1
                    n = 0
                    faceCoord = ""
                    for l in line:
                        if l == " ":
                            if i != -1:
                                newFace.append(int(faceCoord))
                                if newFace[i] < smallestFace:
                                    smallestFace = newFace[i]
                            i += 1
                            n = 0
                            faceCoord = ""
                        elif l == "/":
                            n += 1
                        elif n == 0:
                            faceCoord = faceCoord + l
                    newFace.append(int(faceCoord))
                    if len(newFace) != 3:
                        modifiedFaces = self.getTri(newFace)
                        for face in modifiedFaces:
                            tempFaces.append(face)
                    else:
                        tempFaces.append(newFace)

        for face in tempFaces:
            face[0] = face[0] - smallestFace
            face[1] = face[1] - smallestFace
            face[2] = face[2] - smallestFace
            self.faces.append(tuple(face))
            print("f " + str(face))
        file.close()

    def getTri(self, notTriFace:list):
        newTri = [n for n in range(len(notTriFace) - 2)]
        i = 0
        for face in newTri:
            face = [notTriFace[0], notTriFace[i + 1], notTriFace[i + 2]]
            newTri[i] = face
            i += 1
        return newTri
