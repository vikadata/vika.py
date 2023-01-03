from typing import List

from vika.types import MetaView


class ViewManager:

    def __init__(self, dst: 'Datasheet'):
        self.dst = dst

    def all(self) -> List[MetaView]:
        """
        Query all views of the current datasheet
        @return: List[MetaView]
        """
        return self.dst.get_views()
