import re
from gramatica import Producciones,Terminales,NoTerminales,epsilon, Inicial

global pilaSiguienete
pilaSiguienete = []

def revisaAdelante(produccion,indice,A):
    sig = []
    try: ## A = aBb regla 2
        beta = produccion[indice+1]
        sig += primero(beta)
        if epsilon in sig: # A = aBépsi regla 2.1
            sig.remove(epsilon)
            sig += siguiente(A) if A != produccion[indice] else []

        return sig
    except: # A = aB regla 3
        return siguiente(A) if A != produccion[indice] else []

def primero(x):
    #regla 1
    if x in Terminales:
        return [x]

    #regla 2
    if x in NoTerminales:
        prim = []
        for prod in Producciones:
            
            if prod[0] == x:
                for y in prod[1]:
                    prim += primero(y)
                    if epsilon not in prim:
                        break
        return prim

    #regla 3
    if x == epsilon:
        return [epsilon]

def siguiente(x):
    if x not in pilaSiguienete:
        pilaSiguienete.append(x)
        sig = []
        #regla 1
        if x == Inicial:
            sig.append('$')
        for prod in Producciones:
            if x in prod[1]:
                for inx,p in enumerate(prod[1]):
                    if p == x:
                        #regla 2, 3 & 3.1
                        sig += revisaAdelante(prod[1],inx,prod[0])
        sig = list(dict.fromkeys(sig))
        pilaSiguienete.pop()
        return sig
    else:
        return []