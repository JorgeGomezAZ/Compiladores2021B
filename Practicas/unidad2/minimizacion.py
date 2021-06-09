from Automata import *
"""
minimizar(afd): recibe un afd
regresa un afd equivalente con los estados mínimos por el algoritmo de minimización
"""
def minimizar(afd):
    particiones= {}
    noFinal =[]

    #Separa los estados finales y no finales en 2 paticiones 
    for i in afd.nodos:
        if i not in afd.eFinal:
            noFinal.append(i)
    particiones[0] = afd.eFinal.copy()
    if len(noFinal) >= 1:
        particiones[1] = noFinal
    
    #Intenta separar las particiones 
    t, p =divideP(afd, particiones)

    #Constuye el nuevo automata con las particiones finales y sus tranciciones
    afdMinimo = AFD()
    for part, edo in p.items():
        afdMinimo.nodos.append(part)
        for e in edo:
            if e in afd.eFinal:
                afdMinimo.eFinal.append(part)
            if e == afd.eInicial:
                afdMinimo.eInicial = part
    afdMinimo.alfabeto = afd.alfabeto
    for i, e in p.items():
        p[i] = t[e[0]]
    afdMinimo.transiciones = p
    afdMinimo.eFinal = list(dict.fromkeys(afdMinimo.eFinal))
    return afdMinimo

"""
divideP(afd,particiones): recibe un afd, y un diccionario que representa las particiones 
regresa las particiones que ya no son separables y sus tranciciones 
"""
def divideP(afd,particiones):
    partActual = 0
        
    while partActual != len(particiones):
        
        huboSep = 0 #marcador para saber si hubo un separacion el un ciclo anterior

        if len(particiones[partActual]) > 1:
            transicionAParticion = {}
            #de las particiones actuales encuentra a que particion va cada estado con cada simbolo del alfabeto
            for edo, t in afd.transiciones.items():
                aux = {}
                for s, e in t.items():
                    aux[s] = particionDelEstado(e,particiones)
                transicionAParticion[edo] = aux
            
            Nuevas_particiones =[]
            
            #si la particion tiene más de un estado, itenta separalos
            if len(particiones[partActual]) > 1:
                p = juntaNuevasParticiones(particiones[partActual],transicionAParticion)
                if len(p) > 1:
                    huboSep = 1

            particiones[partActual] = p[0]
            #agregas nuevas particiones
            for i in p[1:]:
                particiones[len(particiones)] = i
        
        if(huboSep == 1):
            partActual = 0
        else:
            partActual += 1
        
    transicionAParticion = {}
    for edo, t in afd.transiciones.items():
        aux = {}
        for s, e in t.items():
            aux[s] = particionDelEstado(e,particiones)
        transicionAParticion[edo] = aux
    

    return transicionAParticion,particiones


"""
comparaEstados(e1,e2,transiciones): dos estados y las tranciciones a particiones de un AFD
Revisa si los estados comparten las mismas transiciones con los mismos simbolos del alfabeto
si todo es igual, regresa Falso (que no se pueden separar), si no son exactamente igual regresa verdadero
"""
def comparaEstados(e1,e2,transiciones):
    elementosCompartidos = {k: transiciones[e2][k] for k in transiciones[e2] if k in transiciones[e1] and transiciones[e2][k] == transiciones[e1][k] }
    if len(transiciones[e1]) == len(transiciones[e2]) and len(transiciones[e2]) == len(elementosCompartidos) :
        return False
    else:
        return True

"""
particionDelEstado(estado,particiones): recibe un estado, y una lista de particiones 
regresa el índice la particion donde esta el estado
"""
def particionDelEstado(estado,particiones):
    for p,edos in particiones.items():
        for e in edos:
            if e == estado:
                return p



"""
juntaNuevasParticiones(particiones,transiciones): una lista de particiones y las tranciones a particiones 
Regresa una lista de listas donde cada lista interna contiene estados que van a las mismas particiones 

"""
def juntaNuevasParticiones(particion,transiciones):
    p = [] #list de listas para estados que van a las mismas particiones  
    i = 0

    #agrega listas a 'p' comparando estados por parejas una sola vez
    while i != len(particion):
        p.append([particion[i]])
        j=i+1
        while j != len(particion):
            if comparaEstados(particion[i],particion[j],transiciones):
                j += 1
            else:
                p[i].append(particion.pop(j))
        i = i+1
    return p
