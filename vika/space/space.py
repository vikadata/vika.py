from vika.node import NodeManager


class Space:
    def __init__(self, vika: "Vika", space_id: str):
        self.vika = vika
        self.id = space_id

    @property
    def nodes(self):
        return NodeManager(self.vika, space_id=self.id)
