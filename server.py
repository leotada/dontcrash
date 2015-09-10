from math import sqrt


class Server(object):
    """Artificial server to listen, decide, and response information to clients."""
    def __init__(self):
        self.clients = []
        self.collisions = []

    @property
    def quantity(self):
        """Return the quantity of clients connected on the server."""
        return len(self.clients)

    def distance(self, point, point2):
        """Calculate the distance between two points."""
        d = point - point2
        return sqrt(d[0]**2 + d[1]**2 + d[2]**2)

    def add_client(self, client):
        """Connect the client(AI) on the server."""
        self.clients.append(client)

    def remove_client(self, client):
        """Remove the client(AI) on the server."""
        self.clients.remove(client)

    def verify(self, task):
        for client in self.clients:
            if client.area_collisions is not None:
                for contact in client.area_collisions:
                    mpoint = contact.getManifoldPoint()
                    point = mpoint.getPositionWorldOnA()
                    # add point collision to list if not any near
                    if len(self.collisions) > 0:
                        for p in self.collisions:
                            if self.distance(point, p[0]) > 5.0:
                                # if not any near
                                self.collisions.append([point, [client.id]])
                            else:
                                # add client in the same point
                                if client.id not in p[1]:
                                    p[1].append(client.id)
                    else:
                        self.collisions.append([point, [client.id]])
                    # Calculate distance between car and collision point
                    # d = client.position - mpoint.getPositionWorldOnA()
                    # distance = sqrt(d[0]**2 + d[1]**2 + d[2]**2) - 3  # 3 offset
                    # # time to reach the point (instant velocity)
                    # time = distance / client.speed
                    # print(distance)
                    print(self.collisions)

        return task.cont
