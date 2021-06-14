import re
from Arbol import Nodo, AFD

"""
ex2afd(postfija): recibe una expresión regular en forma postfija
Pregunta si cada estado tiene trancisiones con simbolo, si sí,
agrega el estado al que se llega con la trancisión a una lista

"""
def ex2afd(postfija):
    alfabeto = []
    tabla = []
    #determina el alfabeto del AFD
    for i in postfija:
        if re.search(r'[^*.|E]', i) and i not in alfabeto:
            alfabeto.append(i)

    a = construyeArbol(postfija)
    t = tablaSig(a)
    estado = [a.primeros]
    estado[0].sort()
    eActual = 0
    nodos = []
    a.recorre(nodos)
    nodos = remueveNodos(nodos)
    afd = AFD()
    afd.alfabeto = alfabeto

    for i in nodos:
        tabla.append( (*i, t[i[1]]) )

    #mientras no haya nuevo estado
    while eActual != len(estado):
        if len(nodos)+1 in estado[eActual]:
            afd.eFinal.append(estado[eActual])
        transicion = {}
        for simbolo in alfabeto:
            posibles = []
            for i in tabla: #recorre la tabla de siguientes
                if i[0] == simbolo and i[1] in estado[eActual]: #si el nodo n esta dentro de los estados actuales que se estan revisando
                    posibles += i[2] #sigiente(n) se agega a la lista de posibles
            posibles = list(dict.fromkeys(posibles))
            posibles.sort()
            transicion[simbolo] = posibles
            if posibles not in estado and len(posibles)>0:
                estado.append(posibles)
                
            afd.transiciones[repr(estado[eActual])] = transicion
        eActual += 1
    
    afd.nodos = estado
    afd.eInicial = estado[0]
    renombraNodos(afd)
    return afd


            
"""
remueveNodos(l): recibe una lista de Nodos
Remueve los nodos que tienen como simbolo un operador o épsilon 
Regresa: tupla de 2 elementos donde el primer elemento es el caracter y el segundo es la posición 
"""
def remueveNodos(l):
    return [(x.simbolo,x.posicion) for x in l if re.search(r'[^*.|E#]', x.simbolo)]


"""
construyeArbol(postfija): recibe una expresión regular en forma postfija
Usa el algoritmo de resolver una expresión postfija, pero en vez de hacer operaciones,
va creando un árbol con objetos de la clase Nodo
Regresa: un objeto Nodo (árbol de análisis sintáctico)
"""
def construyeArbol(postfija):
    #* Marca el final de la expresión regular con una concatenación con #
    postfija.append('#')
    postfija.append('.')

    #* Posicion para cada símbolo
    pos=1
    pilaRes = []

    for i in postfija:
        if i == '*':
            n = Nodo(i)
            n.hijos.append(pilaRes.pop())
            n.anulable = True
            
            n.primeros = n.hijos[0].primeros.copy()
            n.ultimos = n.hijos[0].ultimos.copy()
                
            pilaRes.append(n)

        elif i == '|':
            n = Nodo(i)
            n.hijos.append(pilaRes.pop())
            n.hijos.insert(0,pilaRes.pop())
            
            n.anulable = n.hijos[0].anulable or n.hijos[1].anulable
            
            for p in n.hijos[0].primeros:
                n.primeros.append(p)
            for p in n.hijos[1].primeros:
                n.primeros.append(p)

            for p in n.hijos[0].ultimos:
                n.ultimos.append(p)
            for p in n.hijos[1].ultimos:
                n.ultimos.append(p)
            
            n.primeros.sort()
            n.ultimos.sort()

            pilaRes.append(n)

        elif i == '.':
            n = Nodo(i)
            n.hijos.append(pilaRes.pop())
            n.hijos.insert(0,pilaRes.pop())
            
            n.anulable = n.hijos[0].anulable and n.hijos[1].anulable

            for p in n.hijos[0].primeros:
                n.primeros.append(p)
            if n.hijos[0].anulable:
                for p in n.hijos[1].primeros:
                    n.primeros.append(p)
            
            for p in n.hijos[1].ultimos:
                n.ultimos.append(p)
            if n.hijos[1].anulable:
                for p in n.hijos[0].ultimos:
                    n.ultimos.append(p)
            
            n.primeros.sort()
            n.ultimos.sort()
            pilaRes.append(n)

        elif i == 'E':
            n = Nodo(i)
            n.anulable = True
            pilaRes.append(n)

        else:
            n = Nodo(i)
            n.anulable = False
            n.primeros.append(pos)
            n.ultimos.append(pos)
            n.posicion = pos
            pos += 1
            pilaRes.append(n)

    return pilaRes.pop()


"""
tablaSig(arbol): recibe un objeto Nodo (árbol de análisis sintáctico)
Regresa: un diccionario (tabla de siguientes)
"""
def tablaSig(arbol):
    #número de nodos con símbolos del alfabeto
    tam = arbol.ultimos[0]
    tabla = {}
    for i in range(tam):
        tabla[i+1] = []
    
    arr = []
    arbol.recorre(arr)
    for n in arr:
        if n.simbolo == '*':
            for i in n.ultimos:
                tabla[i] = tabla[i] + n.primeros
                tabla[i] = list(dict.fromkeys(tabla[i]))
                
        if n.simbolo == '.':
            for i in n.hijos[0].ultimos:
                tabla[i] = tabla[i] + n.hijos[1].primeros
                tabla[i] = list(dict.fromkeys(tabla[i]))

    return tabla

"""
renombraNodos(afd): recibe un objeto afd
toma el arbol que se constuye anteriormente y cambia sus etiquetas de los nodos a enteros 
para que pueda ser minimizado y agrega un estado pozo si existen nodos que no tienen transiciones definidas para cualquier simbolo del alfabeto

"""
def renombraNodos(afd):
    nuevosNodos = []
    for i in range(len(afd.nodos)):
        nuevosNodos.append(i)

    afd.eInicial = afd.nodos.index(afd.eInicial)
    f = []
    for i in afd.eFinal:
        f.append(afd.nodos.index(i))
    afd.eFinal = f
    
    estadoPozo = len(afd.nodos)
    activarPozo = 0
    i = 0
    for n in afd.nodos:
        for t in list(afd.transiciones):
            e = afd.transiciones[t]
            if t == repr(n):
                afd.transiciones[i] = e
                del afd.transiciones[repr(n)]
            for s in list(e):
                edo = e[s]
                if type(edo) == list:
                    if len(edo) < 1:
                        activarPozo = 1
                        e[s] = estadoPozo
                if edo == n:
                    e[s] = i
        i = i+1
    afd.nodos = nuevosNodos

    #crea estado pozo si es necesario
    if activarPozo == 1:
        afd.transiciones[estadoPozo] = {}
        afd.nodos.append(estadoPozo)
        for s in afd.alfabeto:
            afd.transiciones[estadoPozo][s] = estadoPozo
    
    
    return



