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

from typing import Any
import arcade
import keyboard

from Renderer.Render import Renderer
from Models.BasicObjects import *
from Models.CustomModels import CustomModel
from Renderer.OrigineVector import Axe, OrigineVector
import random

angle = 0
rotSpeed = 0.03
origine = (0, 0, 0)
rotationAngle = (0, 0, 0)

origineVector = OrigineVector() 

renderer = Renderer((800, 450), 500)
angle = 0.02

def main():
    renderer.TranslateAndRotateAll()
    renderer.Rotate(cube, Axe.Y, angle * 2)
    renderer.Rotate(pyramide, Axe.Y, angle)
    renderer.Rotate(pyramide2, Axe.Y, angle, cube2)
    renderer.Rotate(tetrahedron, Axe.X, angle)
    renderer.Rotate(tetrahedron, Axe.Z, angle)
    renderer.RenderAll()
    arcade.run()
    
def run():
    renderer.TranslateAndRotateAll()
    angle = angle + 0.02
    renderer.Rotate(cube, Axe.Y, angle * 2)
    renderer.Rotate(pyramide, Axe.Y, angle)
    renderer.Rotate(pyramide2, Axe.Y, angle, cube2)
    renderer.Rotate(tetrahedron, Axe.X, angle)
    renderer.Rotate(tetrahedron, Axe.Z, angle)
    renderer.RenderAll()


tetrahedron = Tetrahedron((-500, 200, 2000), 300 , (0, 255, 255))
pyramide = Pyramide((0, 0, 400), (200, 300, 200), (255, 255, 0))
pyramide2 = Pyramide((400, 400, 700), 100, (0, 255, 0))
cube = Cube((200, 200, 250), 50, (255, 0, 100))
cube2 = Cube((0, 0, 0), 150, (0, 150, 255))
#rock = CustomModel("cat.obj", (700, 0, 700), 5, "", (255, 100, 100), True)
light = Light((0, 1000, -1000), 1, (255, 255, 255))
light2 = Light((0, 1000, 1000), 1, (255, 255, 255))
light3 = Light((1000, -1000, 0), 1, (255, 255, 255))
light4 = Light((-1000, -1000, 0), 1, (255, 255, 255))


if __name__ == "__main__":
    main()


while True:
    run()

#while True:
#
#    try:
#        if keyboard.is_pressed("q"):
#            renderer.rotationAngle = (0, rotSpeed, 0)
#            renderer.OV.RotaY += rotSpeed
#        if keyboard.is_pressed("d"):
#            renderer.rotationAngle = (0, -rotSpeed, 0)
#            renderer.OV.RotaY += -rotSpeed
#        if keyboard.is_pressed("r"):
#            renderer.rotationAngle = (rotSpeed, 0, 0)
#            renderer.OV.RotaX += -rotSpeed
#        if keyboard.is_pressed("f"):
#            renderer.rotationAngle = (-rotSpeed, 0, 0)
#            renderer.OV.RotaX += rotSpeed
#        if keyboard.is_pressed("z"):
#            renderer.origine = (0, 0, 5)
#        if keyboard.is_pressed("s"):
#            renderer.origine = (0, 0, -5)
#        if keyboard.is_pressed("x"):
#            renderer.origine = (0, 5, 0)
#        if keyboard.is_pressed("c"):
#            renderer.origine = (0, -5, 0)
#    except:
#        pass
    

    #renderer.CleanScreen()
