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

from Models.FourDObjects import FourDObject
from Renderer.Render import *

class FourDRenderer(Renderer):
    def __init__(self, screenDimension: tuple, focalDistance: float, lightingSystem=True):
        Renderer.__init__(self, screenDimension, focalDistance, lightingSystem)
    
    def Render(self, object: FourDObject, renderFace: bool = False):
        
        displayCoord = [n for n in range(len(object.vertices))]  
        n = 0  
        notValidVertexs = [n for n in range(0)]
        i = 0
        for vertex in object.vertices:
            threeDCoord = ((vertex[0]/(self.FOV + vertex[3])) * self.FOV, (vertex[1]/(self.FOV + vertex[3])) * self.FOV, (vertex[2]/(self.FOV + vertex[3])) * self.FOV)
            if threeDCoord[2] > -self.FOV :
                X = (threeDCoord[0]/(self.FOV + threeDCoord[2])) * self.FOV + self.display.get_width()/2
                Y = (threeDCoord[1]/(self.FOV + threeDCoord[2])) * self.FOV + self.display.get_height()/2
                displayCoord[n] = (X, Y)
            else:
                notValidVertexs.append(vertex)
                displayCoord[n] = ("", "")
            n += 1
            
        for edge in object.edges:
            if displayCoord[edge[0]] != ("", "") and displayCoord[edge[1]] != ("", "") and displayCoord[edge[0]] > (0, 0) and displayCoord[edge[0]] < (self.display.get_width(), self.display.get_height()) and displayCoord[edge[1]] > (0, 0) and displayCoord[edge[1]] < (self.display.get_width(), self.display.get_height()):
                pygame.draw.line(self.display, object.color, displayCoord[edge[0]], displayCoord[edge[1]])
    