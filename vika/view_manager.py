from typing import Optional, List

from vika.types import MetaView


class ViewManager:
    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

    def _check_meta(self):
        if not self._is_fetched:
            views = self.dst.get_views()
            self._is_fetched = True

    def all(self) -> List[Optional[MetaView]]:
        self._check_meta()
        return self.dst.meta_views

    def __getitem__(self, index):
        return self.dst.meta_views[index]
