import heapq

class ColaPRIORITY:
    def __init__(self):
        self.cola = []

    def empty(self):
        return len(self.cola) == 0

    def pop(self):
        return heapq.heappop(self.cola) if not self.empty() else None

    def add(self, elemento):
        if elemento.estado not in [nodo.estado for nodo in self.cola]:
            heapq.heappush(self.cola, elemento)