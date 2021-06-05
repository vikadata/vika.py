class ViewManager:
    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

    def _check_meta(self):
        if not self._is_fetched:
            views = self.dst.get_views()
            self.dst.client_set_meta_views(views)
            self._is_fetched = True

    def __getitem__(self, index):
        return self.dst.meta_views[index]
