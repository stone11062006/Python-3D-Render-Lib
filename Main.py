from typing import Any
import pygame
import keyboard

from Renderer.Render import Renderer
from Renderer.FourDRenderer import FourDRenderer
from Models.BasicObjects import *
from Models.FourDObjects import *
from Models.CustomModels import CustomModel
from Renderer.OrigineVector import Axe, OrigineVector
import random


clock = pygame.time.Clock()

angle = 0
rotSpeed = 0.03
origine = (0, 0, 0)
rotationAngle = (0, 0, 0)

origineVector = OrigineVector() 
renderer = Renderer((800, 450), 500)

renderer4 = FourDRenderer((800, 450), 500)

tesseract = FourDCube((0, 0, 100, 100), 50, (255, 255, 255))

tetrahedron = Tetrahedron((-500, 200, 2000), 300 , (0, 255, 255))
pyramide = Pyramide((0, 0, 400), (200, 300, 200), (255, 255, 0))
pyramide2 = Pyramide((800, 400, 700), 100, (0, 255, 0))
cube = Cube((200, 200, 250), 50, (255, 0, 100))
cube2 = Cube((0, 0, 0), 150, (0, 150, 255))
#rock = CustomModel("towers.obj", (700, 0, 700), 100, "", (255, 255, 255), True)
light = Light((0, 1000, -1000), 1, (255, 255, 255))
light2 = Light((0, 1000, 1000), 1, (255, 255, 255))
light3 = Light((1000, -1000, 0), 1, (255, 255, 255))
light4 = Light((-1000, -1000, 0), 1, (255, 255, 255))
cubes = [n for n in range(10)]
for cube in cubes:
    cube = Cube((random.random() * 10000, random.random() * 10000, random.random() * 10000), random.random() * 500, (random.random() * 255, random.random() * 255, random.random() * 255))

while True:

    try:
        if keyboard.is_pressed("q"):
            renderer.rotationAngle = (0, rotSpeed, 0)
            renderer.OV.RotaY += rotSpeed
        if keyboard.is_pressed("d"):
            renderer.rotationAngle = (0, -rotSpeed, 0)
            renderer.OV.RotaY += -rotSpeed
        if keyboard.is_pressed("r"):
            renderer.rotationAngle = (rotSpeed, 0, 0)
            renderer.OV.RotaX += -rotSpeed
        if keyboard.is_pressed("f"):
            renderer.rotationAngle = (-rotSpeed, 0, 0)
            renderer.OV.RotaX += rotSpeed
        if keyboard.is_pressed("z"):
            renderer.origine = (0, 0, 5)
        if keyboard.is_pressed("s"):
            renderer.origine = (0, 0, -5)
        if keyboard.is_pressed("x"):
            renderer.origine = (0, 5, 0)
        if keyboard.is_pressed("c"):
            renderer.origine = (0, -5, 0)
    except:
        pass
    
    renderer4.Render(tesseract)
    renderer.CleanScreen()
    renderer.TranslateAndRotateAll()
    #renderer.RenderAll()
    angle = 0.02
    renderer.Rotate(cube, Axe.Y, angle * 2)
    renderer.Rotate(pyramide, Axe.Y, angle)
    renderer.Rotate(pyramide2, Axe.Y, angle, cube2)
    renderer.Rotate(tetrahedron, Axe.X, angle)
    renderer.Rotate(tetrahedron, Axe.Z, angle)
    clock.tick(60)
    print(clock.get_fps())
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
    pygame.display.update()
