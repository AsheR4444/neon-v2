from tasks.base import Base
from tasks.mora import Mora
from eth_async.client import Client

class Controller(Base):
    def __init__(self, client: Client):
        super().__init__(client)

        self.base = Base(client=client)
        self.neon = Mora(client=client)
        #self.neonPass = NeonPass()