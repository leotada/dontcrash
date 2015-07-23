from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import BitMask32
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape, BulletTriangleMeshShape, BulletConvexHullShape
from panda3d.bullet import BulletRigidBodyNode, BulletTriangleMesh
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import ZUp


class World(object):
    def __init__(self):
        self.worldNP = render.attachNewNode('World')

        # World
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()

        self.worldB = BulletWorld()
        self.worldB.setGravity(Vec3(0, 0, -9.81))
        self.worldB.setDebugNode(self.debugNP.node())

        # Ground
        # geom = loader.loadModel('models/rua.egg')\
        #         .findAllMatches('**/+GeomNode')\
        #         .getPath(0)\
        #         .node()\
        #         .getGeom(0)
        #
        # mesh = BulletTriangleMesh()
        # mesh.addGeom(geom)
        # shape = BulletTriangleMeshShape(mesh, dynamic=False)

        shape = BulletPlaneShape(Vec3(0, 0, 1), 0)

        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(shape)
        np.setPos(0, 0, 0)
        np.setScale(78)
        np.setCollideMask(BitMask32.allOff())

        # Ground Model
        self.pista = loader.loadModel('models/rua.egg')
        self.pista.setZ(0)
        self.pista.setScale(0.05)

        self.pista.reparentTo(np)

        self.worldB.attach(np.node())

    @property
    def bulletW(self):
        return self.worldB

    @property
    def node(self):
        return self.worldNP

    @property
    def debug(self):
        return self.debugNP
