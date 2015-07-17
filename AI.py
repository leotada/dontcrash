from panda3d.core import LVector3, LVector4
from panda3d.core import MeshDrawer
from math import sin, cos, pi
# Constants
DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos


class AI(object):
    """Classe responsavel por realizar os calculos e tomada de decisoes para
    os veiculos."""

    def __init__(self, node, world):
        self.node = node
        self.world = world  # bullet world
        self.setup()

    def setup(self):
        # band
        self.generator = MeshDrawer()
        self.generator.setBudget(100)
        generatorNode = self.generator.getRoot()
        generatorNode.reparentTo(render)
        generatorNode.setDepthWrite(False)
        generatorNode.setTransparency(True)
        generatorNode.setTwoSided(True)
        generatorNode.setBin("fixed", 0)
        generatorNode.setLightOff(True)

    def area_prediction(self, task):
        """ Draw the area """
        # turn 90 degrees to adjustment
        direction = DEG_TO_RAD * (self.node.getHpr().getX()+90)
        distance = 50

        # Car position, +3 position ahead the car
        self.pFrom = self.node.getPos()
        self.pFrom.setX(self.pFrom.getX()+(cos(direction)*3))
        self.pFrom.setY(self.pFrom.getY()+(sin(direction)*3))

        # Pos: LVector3(X<>, Y^, Z/height)
        self.pTo = LVector3(self.pFrom.getX() + (cos(direction)*distance),
                            self.pFrom.getY() + (sin(direction)*distance),
                            0.5)

        self.generator.begin(base.cam, render)
        self.generator.segment(self.pFrom, self.pTo, 1, 1, LVector4(0.5, 0.2, 0.8, 0.6))
        self.generator.end()
        self.raycast()
        return task.cont

    def raycast(self):
        # Raycast for closest hit
        result = self.world.rayTestClosest(self.pFrom, self.pTo)
        # colision
        print result.hasHit(), \
              result.getHitFraction(), \
              result.getNode(), \
              result.getHitPos(), \
              result.getHitNormal()
