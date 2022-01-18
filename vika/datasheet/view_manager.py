from typing import List

from vika.types import MetaView


class ViewManager:

    def __init__(self, dst: 'Datasheet'):
        self.dst = dst

    def all(self) -> List[MetaView]:
        """
        查询当前维格表所有视图
        @return: List[MetaView]
        """
        return self.dst.get_views()
