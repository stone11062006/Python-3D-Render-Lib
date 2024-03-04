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

import pygame
import math

from Models.BasicObjects import Object, Vector, Light, Line
from Renderer.Matrix import RotationMatix, Matrix
from Renderer.OrigineVector import OrigineVector, Axe

class Renderer():

    def __init__(self, screenDimension: tuple, focalDistance: float, lightingSystem=True):

        class ScreenDimension():
            def __init__(self):
                self.width = screenDimension[0]
                self.height = screenDimension[1]

        self.lightingSystem = lightingSystem
        self.screenDimension = ScreenDimension()
        self.FOV = focalDistance
        self.origine = (0, 0, 0)
        self.rotationAngle = (0, 0, 0)
        self.OV = OrigineVector()
        
        self.display = pygame.display.set_mode((self.screenDimension.width, self.screenDimension.height))
        pygame.init()

    def Render(self, object:Object, renderFace:bool = True):

        if not isinstance(object, Light):

            displayCoord = [n for n in range(len(object.vertices))]  
            n = 0  

            notValidVertexs = [n for n in range(0)]
            i = 0
            for vertex in object.vertices:
                if vertex[2] > -self.FOV :
                    X = (vertex[0]/(self.FOV + vertex[2])) * self.FOV + self.display.get_width()/2
                    Y = (vertex[1]/(self.FOV + vertex[2])) * self.FOV + self.display.get_height()/2
                    displayCoord[n] = (X, Y)
                else:
                    notValidVertexs.append(vertex)
                    displayCoord[n] = ("", "")
                n += 1

            if not renderFace:
                for edge in object.edges:
                    if displayCoord[edge[0]] != ("", "") and displayCoord[edge[1]] != ("", "") and displayCoord[edge[0]] > (0, 0) and displayCoord[edge[0]] < (self.display.get_width(), self.display.get_height()) and displayCoord[edge[1]] > (0, 0) and displayCoord[edge[1]] < (self.display.get_width(), self.display.get_height()):
                        pygame.draw.line(self.display, object.color, displayCoord[edge[0]], displayCoord[edge[1]])

            else:
                for face in self.GetFacesByDistances(object.faces, object.vertices):
                    if displayCoord[face[0]] != ("", "") and displayCoord[face[0]] > (0, 0) and displayCoord[face[0]] < (self.display.get_width(), self.display.get_height()) and   displayCoord[face[1]] != ("", "") and displayCoord[face[1]] > (0, 0) and displayCoord[face[1]] < (self.display.get_width(), self.display.get_height()) and  displayCoord[face[2]] != ("", "") and displayCoord[face[2]] > (0, 0) and displayCoord[face[2]] < (self.display.get_width(), self.display.get_height()):
                    
                        if (self.RotateClockwise(face, displayCoord) and not object.invertFace) or (not self.RotateClockwise(face, displayCoord) and object.invertFace):

                            if self.lightingSystem:
                                pygame.draw.polygon(self.display, self.GetLighting(face, object.vertices, object.color, (object.center.x, object.center.y, object.center.z), object.invertFace), (displayCoord[face[0]], displayCoord[face[1]], displayCoord[face[2]]))
                            else:
                                pygame.draw.polygon(self.display, object.color, (displayCoord[face[0]], displayCoord[face[1]], displayCoord[face[2]]))
        
        else:
            
            if object.center.z > -self.FOV:
                X = (object.center.x/(self.FOV + object.center.z)) * self.FOV + self.display.get_width()/2
                Y = (object.center.y/(self.FOV + object.center.z)) * self.FOV + self.display.get_height()/2
                displayCoord = (X, Y)
            else:
                displayCoord = ("", "")

            if displayCoord != ("", "") and displayCoord > (0, 0) and displayCoord < (self.display.get_width(), self.display.get_height()):
                pygame.draw.circle(self.display, object.color, displayCoord, 10)

    def TranslateAndRotate(self, object:Object):
        if not object.lock:
            self.Translate(object, self.origine)
            if self.rotationAngle[0] != 0:
                self.Rotate(object, Axe.X, self.rotationAngle[0], (0, 0, -self.FOV), False, False)
            if self.rotationAngle[1] != 0:
                self.Rotate(object, Axe.Y, self.rotationAngle[1], (0, 0, -self.FOV), False, True)

    
    def Translate(self, object:Object, trans: tuple):

        object.center.x -= trans[0]
        object.center.y -= trans[1]
        object.center.z -= trans[2]
        n = 0
        for vertex in object.vertices:
            res = tuple(map(lambda i, j: i - j, vertex, self.origine))
            object.vertices[n] = res
            n += 1

    def Rotate(self, object: Object, axe: Axe, angle: float, rotateAround="", lockSelfRotation=True, universalAxes:bool = True):

        coorAroundPoint = (0, 0, 0)
        if isinstance(rotateAround, Object):
            coorAroundPoint = (rotateAround.center.x, rotateAround.center.y, rotateAround.center.z)
        if isinstance(rotateAround, tuple):
            coorAroundPoint = rotateAround
        if isinstance(rotateAround, str):
            coorAroundPoint = (object.center.x, object.center.y, object.center.z)

        if universalAxes == False:
            rotMat = RotationMatix(axe, angle, self.OV)
        else:
            rotMat = RotationMatix(axe, angle, self.OV, True)

        vertexMat = Matrix([[object.center.x - coorAroundPoint[0]], [object.center.y - coorAroundPoint[1]], [object.center.z - coorAroundPoint[2]]])
        newPoint = rotMat.MultiplyBy(vertexMat)
        object.center.x = newPoint[0][0] + coorAroundPoint[0]
        object.center.y = newPoint[1][0] + coorAroundPoint[1]
        object.center.z = newPoint[2][0] + coorAroundPoint[2]

        #if not lockSelfRotation:
        newPoint = [n for n in range(len(object.vertices))]
        n = 0
        for vertex in object.vertices:
            vertexMat = Matrix([[vertex[0] - coorAroundPoint[0]], [vertex[1]- coorAroundPoint[1]], [vertex[2]- coorAroundPoint[2]]])
            newPoint[n] = rotMat.MultiplyBy(vertexMat)
            object.vertices[n] = (newPoint[n][0][0] + coorAroundPoint[0], newPoint[n][1][0] + coorAroundPoint[1], newPoint[n][2][0] + coorAroundPoint[2])
            n += 1
        #else:
        #    object.CalculatePointsFromCenter()
        #    self.Rotate(object, Axe.X, self.rotationAngle[0], "", False)
        #    self.Rotate(object, Axe.Y, self.rotationAngle[1], "", False)

    def GetVertexConnection(self, object: Object, vertexIndex:int):

        connectedEdges = [n for n in range(0)]
        i = 0
        for edge in object.edges:
            if edge[0] == vertexIndex or edge[1] == vertexIndex:
                connectedEdges.append(edge)

        return connectedEdges
    
    def ResetOrigineAndRotation(self):
        self.origine = (0, 0, 0)
        self.rotationAngle = (0, 0, 0) 

    def CleanScreen(self):
        self.display.fill((0,0,0))

    def RotateClockwise(self, face: tuple, projectedVertices):

        a = projectedVertices[face[0]][0]
        b = projectedVertices[face[0]][1]
        c = projectedVertices[face[1]][0]
        d = projectedVertices[face[1]][1]
        e = projectedVertices[face[2]][0]
        f = projectedVertices[face[2]][1]

        if (d - b) == 0:
            
            x = (a + c)/2
            if (d - f) == 0:
                d += 0.0001
            y = (-((c - e) / (d - f)) * x) + ((c * c - e * e + d * d - f * f)/(2 * (d - f)))

        elif (d - f) == 0:

            x = (e + c)/2
            y = (-((c - a) / (d - b)) * x) + ((c * c - a * a + d * d - b * b)/(2 * (d - b)))

        elif ((c - e) / (d - f)) - ((c - a) / (d - b)) == 0:

            return False
        
        else:

            x = ((((c * c - e * e + d * d - f * f) / (2 * (d - f))) - ((c * c - a * a + d * d - b * b) / (2 * (d - b)))) / (((c - e) / (d - f)) - ((c - a) / (d - b))))
            y = (-((c - a) / (d - b)) * x) + ((c * c - a * a + d * d - b * b)/(2 * (d - b)))

        circleCenter = (x, y)

        aTan1 = math.atan2(a - x, b - y)
        aTan2 = math.atan2(c - x, d - y)
        aTan3 = math.atan2(e - x, f - y)

        if (aTan1 > aTan2 and aTan1 > aTan3 and aTan3 > aTan2) or (aTan2 > aTan1 and aTan2 > aTan3 and aTan1 > aTan3) or (aTan3 > aTan1 and aTan3 > aTan2 and aTan1 < aTan2):
             
           return False
        
        else:
            return True
    
    def RenderAll(self):

        objList = Object.render
        duplicatedObjList = objList.copy()
        objByDistance = [i for i in range(len(duplicatedObjList))]
        indexAndDist= [n for n in range(len(duplicatedObjList))]
        i = 0
        for obj in duplicatedObjList:
            if isinstance(obj, Object):
                distance = math.sqrt(math.pow(obj.center.x, 2) + math.pow(obj.center.y, 2) + math.pow(obj.center.z + self.FOV, 2))
                indexAndDist[i] = (i, distance)
            else:
                print("notObjectInListExeptionError")
                indexAndDist[i] = (0, 0)
            i += 1
        indexAndDist.sort(key=lambda x: x[1], reverse=True)

        i = 0
        for ind in indexAndDist:
            objByDistance[i] = duplicatedObjList[ind[0]]
            i += 1

        for o in objByDistance:
            if isinstance(o, Object):
                    self.Render(o, not o.renderEdge)
            else:
                print("notObjectInListExeptionError")
    
    def TranslateAndRotateAll(self):

        moveList = Object.translateAndRotate
        duplicatedObjList = moveList.copy()
        for obj in duplicatedObjList:
            if isinstance(obj, Object):
                self.TranslateAndRotate(obj)
        duplicatedObjList.clear()
        self.ResetOrigineAndRotation()

    def GetLighting(self, face: tuple, vertices, color:tuple, center: tuple, invertFace:bool):
        global newColor
        lights = Light.lights
        dupLight = lights.copy()

        newColor = (5*color[0]/255, 5*color[1]/255, 5*color[2]/255)
        newColor0 = 5*color[0]/255
        newColor1 = 5*color[1]/255
        newColor2 = 5*color[2]/255

        normal = self.GetFaceNormal(face, vertices, center, invertFace)
        normal.Normalize()

        for light in dupLight:
            if isinstance(light, Light):

                faceCenter = self.GetFaceCenter(face, vertices)
                lightCo = (faceCenter[0] - light.center.x, faceCenter[1] - light.center.y, faceCenter[2] - light.center.z)
                dotProduct = lightCo[0] * normal.getAsTuple()[0] + lightCo[1] * normal.getAsTuple()[1] + lightCo[2] * normal.getAsTuple()[2]
                angle = math.acos(dotProduct/math.sqrt(math.pow(lightCo[0], 2) + math.pow(lightCo[1], 2) + math.pow(lightCo[2], 2)))

                angle -= math.pi
                if math.cos(angle) < 0:
                    angle = math.pi/2

                newColor0 += ((math.sqrt(light.intensity) * (1 + color[0]) * light.color[0] * math.cos(angle)))/260
                newColor1 += ((math.sqrt(light.intensity) * (1 + color[1]) * light.color[1] * math.cos(angle)))/260
                newColor2 += ((math.sqrt(light.intensity) * (1 + color[2]) * light.color[2] * math.cos(angle)))/260
                newColor = (newColor0, newColor1, newColor2)

                #line = Line(faceCenter, (light.center.x, light.center.y, light.center.z), (255, 0, 0), 1, False, False, False)
                #self.Render(line, False)

        if newColor[0] > 255:
            newColor0 = 255
        if newColor[1] > 255:
            newColor1 = 255
        if newColor[2] > 255:
            newColor2 = 255
        newColor = (newColor0, newColor1, newColor2)
        return newColor

    def GetFaceNormal(self, face: tuple, vertices, center: tuple, invertFace:bool):

        a = vertices[face[0]][0]
        b = vertices[face[0]][1]
        c = vertices[face[0]][2]
        d = vertices[face[1]][0]
        e = vertices[face[1]][1]
        f = vertices[face[1]][2]
        g = vertices[face[2]][0]
        h = vertices[face[2]][1]
        i = vertices[face[2]][2]


        if i == 0:
            i = 0.0001
        if a == 0:
            a = 0.0002
        if e == 0:
            e = 0.0003
        if b == 0:
            b = 0.0004
        if d == 0:
            d = 0.0005
        if h == 0:
            h = 0.0006
        if f == 0:
            f = 0.0007
        if c == 0:
            c = 0.0008
        if g == 0:
            g = 0.0009

        if (1 - ((d*b)/(e*a))) == 0:
            d += 0.0001

        if (1 - ((((g*b)/(i*a))-(h/i)) * ((((d*c)/(e*a))-(f/e))/(1 - ((d*b)/(e*a)))) + ((g*c)/(i*a)))) == 0:
            g += 0.0001
        
        faceCenter = self.GetFaceCenter(face, vertices)

        t = (((((g*b)/(i*a))-(h/i)) * (((d/(e*a))-(1/e))/(1 - ((d*b)/(e*a)))) + (g/(i*a)) - (1/i)) / (1 - ((((g*b)/(i*a))-(h/i)) * ((((d*c)/(e*a))-(f/e))/(1 - ((d*b)/(e*a)))) + ((g*c)/(i*a))))) * 1
        u = ((((((d*c)/(e*a)) - (f/e)) / (1 - ((d*b)/(e*a)))) * t) + ((((d/(e*a)) - (1/e)) / (1 - ((d*b)/(e*a)))) * 1))
        v = (((-b/a) * u) - ((c/a) * t) - (1/a))
        vector1 = Vector((v, u, t))
        vector2 = Vector((-v, -u, -t))
        vector1A = Vector((vector1.getAsTuple()[0] + faceCenter[0], vector1.getAsTuple()[1] + faceCenter[1], vector1.getAsTuple()[2] + faceCenter[2]), (0, 0, -self.FOV))
        vector2A = Vector((vector2.getAsTuple()[0] + faceCenter[0], vector2.getAsTuple()[1] + faceCenter[1], vector2.getAsTuple()[2] + faceCenter[2]), (0, 0, -self.FOV))
        if vector1A.norme < vector2A.norme:
            if not invertFace:
                vector1.Normalize()
                #line = Line(faceCenter, (vector1.getAsTuple()[0] + faceCenter[0], vector1.getAsTuple()[1] + faceCenter[1], vector1.getAsTuple()[2] + faceCenter[2]), (255, 255, 255), 80, False, False, False)
                #self.Render(line, False)
                return vector1
            else:
                vector2.Normalize()
                #line = Line(faceCenter, (vector2.getAsTuple()[0] + faceCenter[0], vector2.getAsTuple()[1] + faceCenter[1], vector2.getAsTuple()[2] + faceCenter[2]), (255, 255, 255), 80, False, False, False)
                #self.Render(line, False)
                return vector2
        else:
            if not invertFace:
                vector2.Normalize()
                #line = Line(faceCenter, (vector2.getAsTuple()[0] + faceCenter[0], vector2.getAsTuple()[1] + faceCenter[1], vector2.getAsTuple()[2] + faceCenter[2]), (255, 255, 255), 80, False, False, False)
                #self.Render(line, False)
                return vector2
            else:
                vector1.Normalize()
                #line = Line(faceCenter, (vector1.getAsTuple()[0] + faceCenter[0], vector1.getAsTuple()[1] + faceCenter[1], vector1.getAsTuple()[2] + faceCenter[2]), (255, 255, 255), 80, False, False, False)
                #self.Render(line, False)
                return vector1

    def GetFaceCenter(self, face:tuple, vertices):
        
        a = vertices[face[0]][0]
        b = vertices[face[0]][1]
        c = vertices[face[0]][2]
        d = vertices[face[1]][0]
        e = vertices[face[1]][1]
        f = vertices[face[1]][2]
        g = vertices[face[2]][0]
        h = vertices[face[2]][1]
        i = vertices[face[2]][2]

        if a == ((d + g)/2):
            a += 0.0001
        if e == ((b + h)/2):
            e += 0.0001
        if b == ((e + h)/2):
            b += 0.0001
        if d == ((a + g)/2):
            d += 0.0001
        
        if ((((d + g)/2) - a)*(((b + h)/2) - e) - (((e + h)/2) - b)*(((a + g)/2) - d)) == 0:
            b += 0.0005
            d += 0.0005

        w = ((((a + g)/2) - d)*(b - e) + (((b + h)/2) - e)*(d - a))/((((d + g)/2) - a)*(((b + h)/2) - e) - (((e + h)/2) - b)*(((a + g)/2) - d))

        faceCenter = (a + w*(((d + g)/2) - a), b + w*(((e + h)/2) - b), c + w*(((f + i)/2) - c))
        return faceCenter
    
    def GetFacesByDistances(self, facesList:list, vertices):
        indexAndDistList = []
        i = 0
        for face in facesList:
            faceCenter = self.GetFaceCenter(face, vertices)
            distance = math.sqrt(math.pow(faceCenter[0], 2) + math.pow(faceCenter[1], 2) + math.pow(faceCenter[2] + self.FOV, 2))
            indexAndDistList.append((i, distance))
            i += 1
        indexAndDistList.sort(key=lambda x: x[1], reverse=True)
        faceInOrder = [n for n in range(len(indexAndDistList))]
        i = 0
        for p in indexAndDistList:
            faceInOrder[i] = facesList[p[0]]
            i += 1
        return faceInOrder

