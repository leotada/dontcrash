import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import MeshDrawer
from world import World
from car import Car


class Simulador(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.setBackgroundColor(0.1, 0.1, 0.8, 1)
        base.setFrameRateMeter(True)

        base.cam.setPos(3, -30, 4)
        base.cam.lookAt(3, 0, 0)

        # Light
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
        alightNP = render.attachNewNode(alight)

        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(1, 1, -1))
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dlightNP = render.attachNewNode(dlight)

        render.clearLight()
        render.setLight(alightNP)
        render.setLight(dlightNP)

        # Input
        base.accept('escape', self.doExit)
        base.accept('r', self.doReset)
        base.accept('f1', self.toggleWireframe)
        base.accept('f2', self.toggleTexture)
        base.accept('f3', self.toggleDebug)
        base.accept('f5', self.doScreenshot)
        base.accept('i', self.toggleVerify)

        # World, Physics
        self.world = None
        self.setup()

        # Task
        taskMgr.add(self.update, 'updateWorld')
        taskMgr.add(self.verify, 'verifyColision')

        self.maxv = 0.0
        self.maxd = 0.0
        self.smartStop = True

    # _____HANDLER_____
    def toggleVerify(self):
        self.smartStop = False if self.smartStop else True

    def doExit(self):
        self.cleanup()
        sys.exit(1)

    def doReset(self):
        self.cleanup()
        self.setup()

    def toggleWireframe(self):
        base.toggleWireframe()

    def toggleTexture(self):
        base.toggleTexture()

    def toggleDebug(self):
        if self.world.debug.isHidden():
            self.world.debug.show()
        else:
            self.world.debug.hide()

    def doScreenshot(self):
        base.screenshot('Bullet')

    # ____TASK___

    def update(self, task):
        dt = globalClock.getDt()
        self.world.bulletW.doPhysics(dt, 10, 0.008)
        return task.cont

    def cleanup(self):
        worldNP = self.world.node
        worldNP.removeNode()

    def setup(self):
        self.world = World()
        # Car
        self.vehicle = Car(self.world, (1.5, 0, 1), (180, 0, 0))
        self.vehicle2 = Car(self.world, (50, 0, 1), (90, 0, 0))
        cars = [self.vehicle, self.vehicle2]
        for car in cars:
            print(dir(car))
            taskMgr.add(car.AI.area_prediction, "draw task")

    def verify(self, task):
        dist = self.vehicle2.node.getDistance(self.vehicle.node)
        vel = self.vehicle2.bulletVehicle.getCurrentSpeedKmHour()
        distf = ((vel**2) / (250*0.66)) + 6  # medida de seguranca
        # Medidor
        # print('MAX V: {} disf: {}'.format(self.maxv, self.maxd))
        # print('INST V: {} disf: {} dist: {}'.format(vel, distf, dist))
        if vel > self.maxv:
            self.maxv = vel
        if distf > self.maxd:
            self.maxd = distf
        # Aciona freio
        if self.smartStop and (vel > 40.0 or self.vehicle2.stopping):
            self.vehicle2.stopping = True  # diz que ja acionou o sistema
            if vel <= 0.1:
                self.vehicle2.stopping = False  # o sistema ja freiou
            if dist <= distf:
                #task.time
                self.vehicle2.brake()
        return task.cont

sim = Simulador()
base.run()
