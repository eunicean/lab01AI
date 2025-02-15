class Nodo:
    def __init__(self, estado, action=None, parent=None, costo_acumulado=0, heuristica=0):
        self.estado = estado
        self.action = action
        self.parent = parent
        self.costo_acumulado = costo_acumulado
        self.heuristica = heuristica

    def __lt__(self, otro):
        return self.heuristica < otro.heuristica 