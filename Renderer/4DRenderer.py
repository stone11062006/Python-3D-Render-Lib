from Renderer.Render import *

class FourDRenderer(Renderer):
    def __init__(self, screenDimension: tuple, focalDistance: float, lightingSystem=True):
        Renderer.__init__(self, screenDimension, focalDistance, lightingSystem)
    