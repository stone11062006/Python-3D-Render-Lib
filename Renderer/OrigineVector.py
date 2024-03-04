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

from Models.BasicObjects import Vector

import math
from enum import Enum

class Axe(Enum):
    X = 0
    Y = 1
    Z = 2

Axe = Enum("Axe", ["X", "Y", "Z"])


class OrigineVector(Vector):

    def __init__(self, color=(0, 0, 0)):

        self.endPoint = (0, 0, 1)
        self.startPoint = (0, 0, 0)
        self.RotaX = 0
        self.RotaY = 0
        Vector.__init__(self, self.endPoint, self.startPoint, color)

    def GetOrigineVector(self, axe: Axe):

        #DO NOT RENDER THE VECTOR
        if axe == Axe.Z:

            a = self.RotaX
            b = self.RotaY
            x = math.sin(b)
            y = math.cos(b) * math.sin(a)
            z = math.cos(b) * math.cos(a)
            vector = Vector((x, y, z))

        elif axe == Axe.Y:

            a = self.RotaX
            b = self.RotaY
            x = 0
            y = math.sin(a + math.pi/2)
            z = math.cos(a + math.pi/2)
            vector = Vector((x, y, z))

        elif axe == Axe.X:
            
            a = self.RotaX
            b = self.RotaY
            x = math.sin(b + math.pi/2)
            y = math.cos(b + math.pi/2) * math.sin(a)
            z = math.cos(b + math.pi/2) * math.cos(a)
            vector = Vector((x, y, z))
            
        return vector
        