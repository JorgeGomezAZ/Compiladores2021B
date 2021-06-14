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

class AFD:
    def __init__(self):
        self.nodos = []
        self.alfabeto = []
        self.transiciones = {}
        self.eInicial = None
        self.eFinal = []

    def imprimeA(self):
        print("Alfabeto: ",self.alfabeto)
        print("Nodos: ",self.nodos)
        print("Transiciones: ")
        for i,v in self.transiciones.items():
            print("\t",i,':',v)
        print("Estado inicial: ",self.eInicial)
        print("Estados finales: ",self.eFinal)