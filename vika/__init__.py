from apitable import Apitable


class Vika(Apitable):
    def __init__(self, token: str, **kwargs):
        super(Vika, self).__init__(token, **kwargs)
        self._api_base = kwargs.get("api_base", "https://vika.cn")


__all__ = (Vika,)
