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

import math

class Object:
    render = []
    translateAndRotate = []
    def __init__(self, center:tuple, color: tuple, renderEdge=False, invertFace=False, lock=False, renderAll=True, translateAndRotate=True, ThreeD=True):
        if ThreeD:
            if renderAll:
                Object.render.append(self) 
            if translateAndRotate:
                Object.translateAndRotate.append(self)
        self.renderEdge = renderEdge
        self.invertFace = invertFace
        self.vertices = []
        self.edges = []
        self.faces = []
        self.color = color
        self.lock = lock
        if ThreeD:
            #form the center of the scren
            class Center():
                def __init__(self):
                    self.x = center[0]
                    self.y = -center[1]
                    self.z = center[2]
        
            self.center = Center()
    
    def CalculatePointsFromCenter(self):
        pass

class Light(Object):
    lights = []
    def __init__(self, center:tuple, lightIntensity=1, color=(255, 255, 255), lock=False):
        Object.__init__(self, center, color, False, False, lock, False, True)
        Light.lights.append(self)
        self.intensity = lightIntensity


class Line(Object):

    def __init__(self, startPoint: tuple, endPoint, color=(255, 255, 255), length=1, lock=False, render=True, translateAndRotate=True):

        self.startPoint = startPoint
        self.endPoint = endPoint
        self.lenght = length

        if isinstance(self.endPoint, tuple):
            self.center = ((endPoint[0] - startPoint[0])/2 + startPoint[0], (endPoint[1] - startPoint[1])/2 + startPoint[1], (endPoint[2] - startPoint[2])/2 + startPoint[2])
        elif isinstance(self.endPoint, Vector):
            self.center = (startPoint[0] + (startPoint[0] + self.lenght * self.endPoint.normalizedComp.x) / 2, startPoint[1] + (startPoint[1] + self.lenght * self.endPoint.normalizedComp.y) / 2, startPoint[2] + (startPoint[2] + self.lenght * self.endPoint.normalizedComp.z) / 2)

        Object.__init__(self, self.center, color, True,  False, lock, render, translateAndRotate)
        self.CalculatePointsFromCenter()

    def CalculatePointsFromCenter(self):

        Object.CalculatePointsFromCenter(self)

        self.vertices = [n for n in range(2)]
        self.edges = [n for n in range(1)]

        if isinstance(self.endPoint, tuple):
            self.vertices[0] = self.startPoint
            self.vertices[1] = ((self.endPoint[0] - self.startPoint[0]) * (self.lenght - 1) + self.endPoint[0], (self.endPoint[1] - self.startPoint[1]) * (self.lenght - 1) + self.endPoint[1], (self.endPoint[2] - self.startPoint[2]) * (self.lenght - 1) + self.endPoint[2])
        elif isinstance(self.endPoint, Vector):
            self.vertices[0] = (self.startPoint[0] + self.lenght * self.endPoint.normalizedComp.x, self.startPoint[1] + self.lenght * self.endPoint.normalizedComp.y, self.startPoint[2] + self.lenght * self.endPoint.normalizedComp.z)
            self.vertices[1] = (self.startPoint[0] - self.lenght * self.endPoint.normalizedComp.x, self.startPoint[1] - self.lenght * self.endPoint.normalizedComp.y, self.startPoint[2] - self.lenght * self.endPoint.normalizedComp.z)

        self.edges[0] = (0, 1)

class Vector(Line):

    def __init__(self, endPoint: tuple, startPoint=(0, 0, 0), color=(255, 255, 255), length=1, lock=False):
        
        Line.__init__(self, startPoint, endPoint, color, length, lock, False, False)
        
        class Components:
            def __init__(self, xComp: float, yComp: float, zComp: float):
                self.x = xComp
                self.y = yComp
                self.z = zComp

        self.comp = Components(endPoint[0] - startPoint[0], endPoint[1] - startPoint[1], endPoint[2] - startPoint[2])
        self.norme = self.getNorme()
        self.normalizedComp = Components(self.comp.x/self.norme, self.comp.y/self.norme, self.comp.z/self.norme)
    
    def Normalize(self):

        normalizedVector = (self.comp.x/self.norme, self.comp.y/self.norme, self.comp.z/self.norme)
        self.comp.x = normalizedVector[0]
        self.comp.y = normalizedVector[1]
        self.comp.z = normalizedVector[2]
        self.norme = self.getNorme()

    def getNorme(self):

        norme = math.sqrt(math.pow(self.comp.x,2) + math.pow(self.comp.y,2) + math.pow(self.comp.z,2))
        return norme
    
    def getAsTuple(self, normalized=False):

        if not normalized:
            coord = (self.comp.x, self.comp.y, self.comp.z)
        else:
            coord = (self.normalizedComp.x, self.normalizedComp.y, self.normalizedComp.z)
        return coord
    
class Shape(Object):  

    def __init__(self, center: tuple, size, color: tuple, invertFace=False, lock=False):

        Object.__init__(self, center, color, False, invertFace, lock)

        class Size():
            def __init__(self):
                
                if isinstance(size, tuple):
                    self.x = size[0]
                    self.y = size[1]
                    self.z = size[2]
                else:
                    self.x = size
                    self.y = size
                    self.z = size

        self.size = Size()

        class SizeBy2():
            def __init__(self, size):
                self.size = size
                self.x = self.size.x/2
                self.y = self.size.y/2
                self.z = self.size.z/2
                    
        self.sizeBy2 = SizeBy2(self.size)

class Cube(Shape):

    def __init__(self, center: tuple, size: float, color: tuple, invertFace=False, lock=False):

        Shape.__init__(self, center, (size, size, size), color, invertFace, lock)
        self.CalculatePointsFromCenter()

    def CalculatePointsFromCenter(self):

        Object.CalculatePointsFromCenter(self)

        self.vertices = [n for n in range(8)]
        self.edges = [n for n in range(12)]
        self.faces = [n for n in range(12)]
        self.sizeBy2.y *= -1
        
        self.vertices[0] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[1] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[2] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[3] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[4] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[5] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[6] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[7] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z)

        self.edges[0] = (0,1)
        self.edges[1] = (1,2)
        self.edges[2] = (2,3)
        self.edges[3] = (3,0)
        self.edges[4] = (4,5)
        self.edges[5] = (5,6)
        self.edges[6] = (6,7)
        self.edges[7] = (7,4)
        self.edges[8] = (0,4)
        self.edges[9] = (1,5)
        self.edges[10] = (2,6)
        self.edges[11] = (3,7)

        self.faces[0] = (0, 2, 1)
        self.faces[1] = (0, 3, 2)
        self.faces[2] = (1, 6, 5)
        self.faces[3] = (1, 2, 6)
        self.faces[4] = (5, 7, 4)
        self.faces[5] = (5, 6, 7)
        self.faces[6] = (4, 3, 0)
        self.faces[7] = (4, 7, 3)
        self.faces[8] = (3, 7, 6)
        self.faces[9] = (3, 6, 2)
        self.faces[10] = (0, 1, 5)
        self.faces[11] = (0, 5, 4)
 

class Pyramide(Shape):

    def __init__(self, center: tuple, size: tuple, color: tuple, invertFace=False, lock=False):

        Shape.__init__(self, center, size, color, invertFace, lock)
        self.CalculatePointsFromCenter()

    def CalculatePointsFromCenter(self):

        Object.CalculatePointsFromCenter(self)

        self.vertices = [n for n in range(5)]
        self.edges = [n for n in range(8)]
        self.faces = [n for n in range(6)]
        
        self.vertices[0] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[1] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z)
        self.vertices[2] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[3] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[4] = (self.center.x, self.center.y - self.sizeBy2.y, self.center.z)

        self.edges[0] = (0,1)
        self.edges[1] = (1,2)
        self.edges[2] = (2,3)
        self.edges[3] = (3,0)
        self.edges[4] = (0,4)
        self.edges[5] = (1,4)
        self.edges[6] = (2,4)
        self.edges[7] = (3,4)

        self.faces[0] = (0, 4, 1)
        self.faces[1] = (1, 4, 2)
        self.faces[2] = (2, 4, 3)
        self.faces[3] = (3, 4, 0)
        self.faces[4] = (0, 1, 2)
        self.faces[5] = (0, 2, 3)
    

class Tetrahedron(Shape):

    def __init__(self, center: tuple, size: tuple, color: tuple, invertFace=False, lock=False):

        Shape.__init__(self, center, size, color, invertFace, lock)
        self.CalculatePointFromCenter()

    def CalculatePointFromCenter(self):

        Object.CalculatePointsFromCenter(self)

        self.vertices = [n for n in range(4)]
        self.edges = [n for n in range(6)]
        self.faces = [n for n in range(4)]
        
        self.vertices[0] = (self.center.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z)
        self.vertices[1] = (self.center.x - (math.sqrt(3)/2)*self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - (1/2)*self.sizeBy2.z)
        self.vertices[2] = (self.center.x + (math.sqrt(3)/2)*self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - (1/2)*self.sizeBy2.z)
        self.vertices[3] = (self.center.x, self.center.y - self.sizeBy2.y, self.center.z)

        self.edges[0] = (0,1)
        self.edges[1] = (1,2)
        self.edges[2] = (2,0)
        self.edges[3] = (0,3)
        self.edges[4] = (1,3)
        self.edges[5] = (2,3)

        self.faces[0] = (0, 3, 1)
        self.faces[1] = (1, 3, 2)
        self.faces[2] = (2, 3, 0)
        self.faces[3] = (0, 1, 2)
    