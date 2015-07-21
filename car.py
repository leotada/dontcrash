from panda3d.bullet import BulletVehicle
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import ZUp
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.core import TransformState
from AI import AI


class Car(object):
    def __init__(self, world, pos, rot=None):
        self.worldNP = world.node
        self.world = world.bulletW

        self.keyMap = {
            'w': False,
            's': False,
            'a': False,
            'd': False,
            'space': False}

        base.accept("w", self.setKey, ["w", True])
        base.accept("s", self.setKey, ["s", True])
        base.accept("a", self.setKey, ["a", True])
        base.accept("d", self.setKey, ["d", True])
        base.accept("space", self.setKey, ["space", True])
        base.accept("w-up", self.setKey, ["w", False])
        base.accept("s-up", self.setKey, ["s", False])
        base.accept("a-up", self.setKey, ["a", False])
        base.accept("d-up", self.setKey, ["d", False])
        base.accept("space-up", self.setKey, ["space", False])

        taskMgr.add(self.update, "Car Control")

        self.stopping = False
        self.dt = None
        self.engineForce = 0.0
        self.brakeForce = 0.0
        self.pos = pos

        # Chassis
        self.shape = BulletBoxShape(Vec3(0.6, 1.4, 0.5))
        ts = TransformState.makePos(Point3(0, 0, 0.5))

        self.np = self.worldNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.np.node().addShape(self.shape, ts)
        self.np.setPos(*self.pos)
        if rot: self.np.setHpr(*rot)
        self.np.node().setMass(800.0)
        self.np.node().setDeactivationEnabled(False)

        self.world.attachRigidBody(self.np.node())

        # Bullet Continuous Collision Detection
        self.np.node().setCcdSweptSphereRadius(1.0)
        self.np.node().setCcdMotionThreshold(1e-7)

        # Vehicle
        self.vehicle = BulletVehicle(self.world, self.np.node())
        self.vehicle.setCoordinateSystem(ZUp)
        self.world.attachVehicle(self.vehicle)

        self.yugoNP = loader.loadModel('models/yugo/yugo.egg')
        self.yugoNP.reparentTo(self.np)

        # Right front wheel
        self.np1 = loader.loadModel('models/yugo/yugotireR.egg')
        self.np1.reparentTo(self.worldNP)
        self._addWheel(Point3(0.70,  1.05, 0.3), True, self.np1)

        # Left front wheel
        self.np2 = loader.loadModel('models/yugo/yugotireL.egg')
        self.np2.reparentTo(self.worldNP)
        self._addWheel(Point3(-0.70,  1.05, 0.3), True, self.np2)

        # Right rear wheel
        self.np3 = loader.loadModel('models/yugo/yugotireR.egg')
        self.np3.reparentTo(self.worldNP)
        self._addWheel(Point3(0.70, -1.05, 0.3), False, self.np3)

        # Left rear wheel
        self.np4 = loader.loadModel('models/yugo/yugotireL.egg')
        self.np4.reparentTo(self.worldNP)
        self._addWheel(Point3(-0.70, -1.05, 0.3), False, self.np4)

        # Steering info
        self.steering = 0.0             # degree
        self.steeringClamp = 45.0       # degree
        self.steeringIncrement = 120.0  # degree per second

        # setup AI
        self.setupAI()

    @property
    def node(self):
        return self.np

    @property
    def bulletVehicle(self):
        return self.vehicle

    def _addWheel(self, pos, front, np):
        wheel = self.vehicle.createWheel()

        wheel.setNode(np.node())
        wheel.setChassisConnectionPointCs(pos)
        wheel.setFrontWheel(front)

        wheel.setWheelDirectionCs(Vec3(0, 0, -1))
        wheel.setWheelAxleCs(Vec3(1, 0, 0))
        wheel.setWheelRadius(0.25)
        wheel.setMaxSuspensionTravelCm(40.0)

        wheel.setSuspensionStiffness(40.0)
        wheel.setWheelsDampingRelaxation(2.3)
        wheel.setWheelsDampingCompression(4.4)
        wheel.setFrictionSlip(100.0)
        wheel.setRollInfluence(0.1)

    def forward(self):
        self.engineForce = 1000.0
        self.brakeForce = 0.0

    def reverse(self):
        self.engineForce = -1000.0
        self.brakeForce = 0.0

    def brake(self):
        self.engineForce = 0.0
        self.brakeForce = 50.0

    def neutral(self):
        self.engineForce = 0.0
        self.brakeForce = 0.0

    def turnLeft(self):
        self.steering += self.dt * self.steeringIncrement
        self.steering = min(self.steering, self.steeringClamp)

    def turnRight(self):
        self.steering -= self.dt * self.steeringIncrement
        self.steering = max(self.steering, -self.steeringClamp)

    def turnNeutral(self):
        if self.steering > 0.0:
            self.steering -= self.dt * self.steeringIncrement
            self.steering = max(self.steering, 0.0)
        else:
            self.steering += self.dt * self.steeringIncrement
            self.steering = min(self.steering, 0.0)

    def setKey(self, key, value):
        self.keyMap[key] = value

    def setupAI(self):
        self.AI = AI(self.node, self.worldNP, self.world)

    def update(self, task):
        # Apply steering to front wheels
        self.vehicle.setSteeringValue(self.steering, 0)
        self.vehicle.setSteeringValue(self.steering, 1)

        # Apply engine and brake to rear wheels
        self.vehicle.applyEngineForce(self.engineForce, 2)  # rear
        self.vehicle.applyEngineForce(self.engineForce, 3)  # rear
        # self.vehicle.applyEngineForce(self.engineForce, 0);
        # self.vehicle.applyEngineForce(self.engineForce, 1);
        self.vehicle.setBrake(self.brakeForce, 2)
        self.vehicle.setBrake(self.brakeForce, 3)

        self.dt = globalClock.getDt()
        if self.dt > .20:  # prevent high framerates
            return task.cont
        if not self.keyMap["w"] and not self.keyMap["s"]:
            self.neutral()
        elif self.keyMap["w"]:
            self.forward()
        elif self.keyMap["s"]:
            self.reverse()
        if not self.keyMap["a"] and not self.keyMap["d"]:
            self.turnNeutral()
        elif self.keyMap["a"]:
            self.turnLeft()
        elif self.keyMap["d"]:
            self.turnRight()
        if self.keyMap["space"]:
            self.brake()

        return task.cont
