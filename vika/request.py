import time
import requests


class VikaSession(requests.Session):
    def __init__(self):
        super(VikaSession, self).__init__()
        self.qps = 1 / 5
        # self.qps_map = dict()

    def get(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(VikaSession, self).get(*args)

    def post(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(VikaSession, self).post(*args)

    def patch(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(VikaSession, self).patch(*args)

    def delete(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(VikaSession, self).delete(*args)
