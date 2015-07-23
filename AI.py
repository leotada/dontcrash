from panda3d.core import LVector3, LVector4
from panda3d.core import MeshDrawer
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode, BulletBoxShape
from panda3d.core import BitMask32
from panda3d.core import Vec3
from math import sin, cos, pi
# Constants
DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos


class AI(object):
    """Classe responsavel por realizar os calculos e tomada de decisoes para
    os veiculos."""

    def __init__(self, node, worldNP, world):
        self.node = node
        self.worldNP = worldNP  # world node
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

        # Box (dynamic)
        shape = BulletBoxShape(Vec3(1, 20, 1))
        self.area = self.worldNP.attachNewNode(BulletGhostNode('Area'))
        self.area.node().addShape(shape)
        self.area.setPos(self.node.getPos())
        self.area.setCollideMask(BitMask32.bit(1))

        self.world.attach(self.area.node())
        self.area.node().notifyCollisions(True)

    def area_prediction(self, task):
        """ Draw the area """
        # turn 90 degrees to adjustment
        direction = DEG_TO_RAD * (self.node.getHpr().getX()+90)
        distance = 38

        # Car position +3, position ahead the car
        self.pFrom = self.node.getPos()
        self.pFrom.setX(self.pFrom.getX()+(cos(direction)*3))
        self.pFrom.setY(self.pFrom.getY()+(sin(direction)*3))

        # Pos: LVector3(X<>, Y^, Z/height)
        self.pTo = LVector3(self.pFrom.getX() + (cos(direction)*distance),
                            self.pFrom.getY() + (sin(direction)*distance),
                            0.5)

        # Draw line
        self.generator.begin(base.cam, render)
        self.generator.segment(self.pFrom, self.pTo, 1, 1, LVector4(0.5, 0.2, 0.8, 0.6))
        self.generator.end()

        # Area Bullet
        self.area.setX(self.node.getX()+(cos(direction)*22))
        self.area.setY(self.node.getY()+(sin(direction)*22))
        self.area.setHpr(self.node.getHpr())

        # Test collisions and filter by bitmask
        result = self.world.contactTest(self.area.node(), use_filter=True)

        print(result.getNumContacts())

        for contact in result.getContacts():
            # print('Node0:', contact.getNode0().getName())
            # print('Node1:',contact.getNode1())
            mpoint = contact.getManifoldPoint()
            print('Dist:', mpoint.getDistance())
            print('Imp', mpoint.getAppliedImpulse())
            print('PosA:', mpoint.getPositionWorldOnA())
            print('PosB:', mpoint.getPositionWorldOnB())
            print('LocA:', mpoint.getLocalPointA())
            print('LocB:', mpoint.getLocalPointB())

        return task.cont
