class Automata:
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

class AFD(Automata):
    pass
class AFN(Automata):
    def __init__(self,simbolo, n):
        self.nodos = [n,n+1]

        self.alfabeto = [simbolo]
        self.transiciones ={
            self.nodos[0]:{simbolo: [self.nodos[1]]}
        }
        self.eInicial = self.nodos[0]
        self.eFinal = self.nodos[1]
    
    def thompson_or(self,segundo,n):
        self.nodos += segundo.nodos
        self.nodos.append(n)
        self.nodos.append(n+1)
        self.alfabeto += segundo.alfabeto
        self.transiciones.update(segundo.transiciones)
        self.transiciones.update({
            self.nodos[-2]:{'E': [self.eInicial,segundo.eInicial]},
            self.eFinal:{'E': [self.nodos[-1]]},
            segundo.eFinal:{'E': [self.nodos[-1]]}
        })
        self.eInicial = self.nodos[-2]
        self.eFinal = self.nodos[-1]
        return self

    def thompson_concat(self,segundo,n):
        self.nodos += segundo.nodos
        self.alfabeto += segundo.alfabeto
        self.transiciones.update(segundo.transiciones)
        self.transiciones[self.eFinal] = self.transiciones.pop(segundo.eInicial)
        self.eFinal = segundo.eFinal
        self.nodos.remove(segundo.eInicial)
        return self
    
    def thompson_cerradura(self,n):
        self.nodos.append(n)
        self.nodos.append(n+1)
        self.transiciones.update({
            self.nodos[-2]:{'E': [self.eInicial,self.nodos[-1]]},
            self.eFinal:{'E': [self.eInicial,self.nodos[-1]]}
        })
        self.eInicial = self.nodos[-2]
        self.eFinal = self.nodos[-1]
        return self