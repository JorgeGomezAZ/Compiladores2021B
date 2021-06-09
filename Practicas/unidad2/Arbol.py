class Nodo:
    def __init__(self,simbolo):
        self.simbolo = simbolo
        self.hijos = []
        self.posicion = None
        self.anulable = None
        self.primeros = []
        self.ultimos = []

    def recorre(self,arr):
        for hijo in self.hijos:
            hijo.recorre(arr)
        arr.append(self)
        return