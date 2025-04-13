
from itertools import starmap


class Node:
    """Represents a node
    """
    def __init__(self, priority, add):
        self.priority = priority
        self.add = add
        self.ws = None

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def to_pair(self):
        return self.priority, self.add

    def send(self, data):
        if self.ws:
            return self.ws.send(data)
        return -1

class BinTreeTopologyManager:
    def __init__(self, pairs) -> None:
        self.heap = []
        self.peer2idx = {}

        self.update(pairs)

    def update(self, pairs=None) -> None:
        if pairs is None:
            pairs = self.heap
        else:
            pairs = starmap(Node, pairs)

        self.heap = sorted(pairs, reverse=True)
        self.peer2idx = {}

        for idx, n in enumerate(self.heap):
            self.peer2idx[n.add] = idx

    def update_with(self, pairs):
        for pair in pairs:
            if pair[1] in self.peer2idx:
                self.get(pair[1]).priority = pair[0]
            else:
                self.heap.append(Node(*pair))

        self.update()

    def serialize(self):
        return list(map(Node.to_pair, self.heap))

    def parent_of(self, peer) -> Node:
        return self.heap[(self.peer2idx[peer] - 1) // 2]

    def remove(self, peer):
        self.heap.pop(self.peer2idx[peer])
        self.update()

    def add(self, pair):
        if pair[1] in self.peer2idx:
            self.get(pair[1]).priority = pair[0]
        else:
            self.heap.append(Node(*pair))

        self.update()

    def get(self, peer):
        return self.heap[self.peer2idx[peer]]