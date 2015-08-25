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
                    # Calculate distance between car and collision point
                    d = client.position - mpoint.getPositionWorldOnA()
                    distance = sqrt(d[0]**2 + d[1]**2 + d[2]**2) - 3  # 3 offset
                    # time to reach the point (instant velocity)
                    time = distance / client.speed
                    print(time)

        return task.cont
