import json

from .topologymgr import BinTreeTopologyManager
from .leaderboard import Leaderboard

class NotificationBus:
    def __init__(self, topology: BinTreeTopologyManager, lb: Leaderboard, pusher):
        self.lb = lb
        self.tm = topology
        self.pusher = pusher

    def lb_update(self, data):
        self.lb.update(data["name"], data["score"])
        self.push({"op": "lb_update", "d": data})

    def tm_update(self, data):
        self.tm.update(data)
        self.push({"op": "tm_update", "d": self.tm.serialize()})

    def tm_sync(self, data):
        self.tm.update_with(data)
        # self.push({"op": "tm_sync", "d": self.tm.serialize()})

    def lb_sync(self, data):
        self.lb.players.update({d["name"]: d["score"] for d in data})
        # self.push({"op": "lb_sync", "d": self.lb.get_leaderboard()})

    def handle(self, payload):
        getattr(self, payload["op"])(payload["d"])
        print(payload, flush=True)

    def push(self, msg):
        print("sending ", msg, flush=True)
        self.pusher(json.dumps(msg))