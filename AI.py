from panda3d.core import LVector3, LVector4
from panda3d.core import MeshDrawer
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode, BulletBoxShape
from panda3d.core import BitMask32
from panda3d.core import Vec3
from math import sin, cos, pi, sqrt
import random

# Constants
DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos


class AI(object):
    """Classe responsavel por realizar os calculos e tomada de decisoes para
    os veiculos."""

    def __init__(self, vehicle, worldNP, world):
        self.vehicle = vehicle
        self.worldNP = worldNP  # world node
        self.world = world  # bullet world
        self.smartStop = True
        self.stopping = False
        self.area_collisions = None
        self.prediction = False  # Server response about collision
        self.id = random.randint(100, 999)
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
        self.area.setPos(self.vehicle.node.getPos())
        self.area.setCollideMask(BitMask32.bit(1))

        self.world.attach(self.area.node())
        self.area.node().notifyCollisions(True)

    @property
    def position(self):
        """Position of vehicle."""
        return self.vehicle.node.getPos()

    @property
    def speed(self):
        """Speed in Km/Hour."""
        return self.vehicle.speedKmHour

    def area_prediction(self, task):
        """ Draw the area and predict the collision inside."""
        # turn 90 degrees to adjustment
        direction = DEG_TO_RAD * (self.vehicle.node.getHpr().getX()+90)
        distance = 38

        # Car position +3, position ahead the car
        self.pFrom = self.vehicle.node.getPos()
        self.pFrom.setX(self.pFrom.getX()+(cos(direction)*3))
        self.pFrom.setY(self.pFrom.getY()+(sin(direction)*3))

        # Pos: LVector3(X<>, Y^, Z/height)
        self.pTo = LVector3(self.pFrom.getX() + (cos(direction)*distance),
                            self.pFrom.getY() + (sin(direction)*distance),
                            0.5)

        # Draw line
        self.generator.begin(base.cam, render)
        if self.vehicle.brakeForce > 0.0:  # red line while braking
            self.generator.segment(self.pFrom, self.pTo, 1, 1, LVector4(1.0, 0.0, 0.0, 0.6))
        else:
            self.generator.segment(self.pFrom, self.pTo, 1, 1, LVector4(0.5, 0.2, 0.8, 0.6))
        self.generator.end()

        # Area (Box) Bullet
        self.area.setX(self.vehicle.node.getX()+(cos(direction)*22))
        self.area.setY(self.vehicle.node.getY()+(sin(direction)*22))
        self.area.setHpr(self.vehicle.node.getHpr())

        # Test collisions and filter by bitmask
        result = self.world.contactTest(self.area.node(), use_filter=True)
        self.area_collisions = result.getContacts()
        # print(result.getNumContacts())

        return task.cont
