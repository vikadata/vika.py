import time
import requests


class ApitableSession(requests.Session):
    def __init__(self):
        super(ApitableSession, self).__init__()
        self.qps = 1 / 5
        # self.qps_map = dict()

    def get(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(ApitableSession, self).get(*args)

    def post(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(ApitableSession, self).post(*args)

    def patch(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(ApitableSession, self).patch(*args)

    def delete(self, *args):
        if self.qps > 0:
            time.sleep(self.qps)
        return super(ApitableSession, self).delete(*args)
