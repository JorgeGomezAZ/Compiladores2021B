import re
from Automata import AFN


"""
construyeAutomata(postfija): recibe una expresión regular en forma postfija
Usa el algoritmo de resolver una expresión postfija, pero en vez de hacer operaciones,
va creando un automata con metodos de la clase Automata (AFN por construcciones de Thompson)

"""
def construyeAutomata(postfija):
    #indica cuantos nodos se han creado
    totalNodos=0 

    pilaRes = []

    for i in postfija:
        if i == '*':
            pilaRes.append((pilaRes.pop()).thompson_cerradura(totalNodos))
            totalNodos+=2

        elif i == '|':
            segundo = pilaRes.pop()
            pilaRes.append((pilaRes.pop()).thompson_or(segundo,totalNodos))
            totalNodos+=2
        elif i == '.':
            segundo = pilaRes.pop()
            pilaRes.append((pilaRes.pop()).thompson_concat(segundo,totalNodos))

        else:
            pilaRes.append(AFN(i,totalNodos))
            totalNodos+=2

    pilaRes[0].alfabeto = list(dict.fromkeys(pilaRes[0].alfabeto))
    if 'E' in pilaRes[0].alfabeto:
        pilaRes[0].alfabeto.remove('E')

    return pilaRes.pop()


