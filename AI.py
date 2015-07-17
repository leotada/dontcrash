
# Constants
DEG_TO_RAD = pi / 180  # translates degrees to radians for sin and cos


class AI(object):
    """Classe responsavel por realizar os calculos e tomada de decisoes para
    os veiculos."""

    def area_prediction(self):
        # gira 90 graus, o obj esta colocado assim
        direction = DEG_TO_RAD * (self.vehicle2.node.getHpr().getX()+90)
        distancia = 50

        # Car position, +3 para comecar da frente do carro
        pFrom = self.vehicle2.node.getPos()
        pFrom.setX(pFrom.getX()+(cos(direction)*3))
        pFrom.setY(pFrom.getY()+(sin(direction)*3))

        # Pos: LVector3(X<>, Y^, Z/Altura)
        pTo = LVector3(pFrom.getX() + (cos(direction)*distancia),
                       pFrom.getY() + (sin(direction)*distancia),
                       0.5)

        self.generator.begin(base.cam, render)
        self.generator.segment(pFrom, pTo, 1, 1, LVector4(0.5, 0.2, 0.8, 0.6))
        self.generator.end()
