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

from Models.BasicObjects import *

class FourDObject(Object):
    def __init__(self, center: tuple, color: tuple, renderEdge=True, invertFace=False, lock=False, renderAll=True, translateAndRotate=True):
        Object.__init__(self, center, color, renderEdge, invertFace, lock, renderAll, translateAndRotate, False)
        #form the center of the scren
        class Center():
            def __init__(self):
                self.x = center[0]
                self.y = -center[1]
                self.z = center[2]
                self.w = center[3]
        
        self.center = Center()

class FourDShapes(FourDObject):

    def __init__(self, center: tuple, size, color: tuple, invertFace=False, lock=False):

        FourDObject.__init__(self, center, color, False, invertFace, lock)

        class Size():
            def __init__(self):
                
                if isinstance(size, tuple):
                    self.x = size[0]
                    self.y = size[1]
                    self.z = size[2]
                    self.w = size[3]
                else:
                    self.x = size
                    self.y = size
                    self.z = size
                    self.w = size

        self.size = Size()

        class SizeBy2():
            def __init__(self, size):
                self.size = size
                self.x = self.size.x/2
                self.y = self.size.y/2
                self.z = self.size.z/2
                self.w = self.size.z/2
                    
        self.sizeBy2 = SizeBy2(self.size)

class FourDCube(FourDShapes):

    def __init__(self, center: tuple, size: float, color: tuple):

        FourDShapes.__init__(self, center, (size, size, size, size), color, False, False)
        self.CalculatePointsFromCenter()

    def CalculatePointsFromCenter(self):

        Object.CalculatePointsFromCenter(self)

        self.vertices = [n for n in range(16)]
        self.edges = [n for n in range(32)]
        self.faces = [n for n in range(12)]
        self.sizeBy2.y *= -1
        
        self.vertices[0] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[1] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[2] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[3] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[4] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[5] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[6] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[7] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w - self.sizeBy2.w)
        self.vertices[8] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[9] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[10] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[11] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z - self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[12] = (self.center.x - self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[13] = (self.center.x + self.sizeBy2.x, self.center.y - self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[14] = (self.center.x + self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w + self.sizeBy2.w)
        self.vertices[15] = (self.center.x - self.sizeBy2.x, self.center.y + self.sizeBy2.y, self.center.z + self.sizeBy2.z, self.center.w + self.sizeBy2.w)

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
        self.edges[12] = (8,9)
        self.edges[13] = (9,10)
        self.edges[14] = (10,11)
        self.edges[15] = (11,8)
        self.edges[16] = (12,13)
        self.edges[17] = (13,14)
        self.edges[18] = (14,15)
        self.edges[19] = (15,12)
        self.edges[20] = (8,12)
        self.edges[21] = (9,13)
        self.edges[22] = (10,14)
        self.edges[23] = (11,15)
        self.edges[24] = (0,8)
        self.edges[25] = (1,9)
        self.edges[26] = (2,10)
        self.edges[27] = (3,11)
        self.edges[28] = (4,12)
        self.edges[29] = (5,13)
        self.edges[30] = (6,14)
        self.edges[31] = (7,15)

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
 