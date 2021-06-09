from Automata import *
"""
subconjuntos(automata): recibe un AFN que calculará su equivaente AFD por el algoritmo de subconjuntos4
regresa: AFD
"""
def subconjuntos(automata):
    #lista que contendrá la cerradura de el estado inicial
    c = []

    #todos los nucleos que se han encontrado
    nucleos = []

    #las cerraduras é de cada nucleo
    epsilons = []

    nucleos.append([automata.eInicial])
    
    cerraduraE(automata.transiciones,automata.eInicial, c)

    epsilons.append(list(dict.fromkeys(c)))

    pociEp = 0
    afd = AFD()
    calcNucs(automata,epsilons,nucleos,pociEp,afd)
    afd.alfabeto = automata.alfabeto.copy()
    for i in list(afd.transiciones):
        afd.nodos.append(i)
        for n in epsilons[i]:
            if n == automata.eInicial:
                afd.eInicial = i
            if n == automata.eFinal:
                afd.eFinal.append(i)
    
    return afd


"""
calcNucs(automata,epsilons,nucleos,pociEp,afd):
    Recibe:
    El automata que va a convertir a afd,
    lista de cerraduras é de cada nucleo encontrado,
    lista de todos los nucleos encontrados,
    pociEp- un indicador para saber de que C-é se calculan los nucleos,
    el nuevo afd que se esta construyendo
    
Pregunta si los entados en epsilons[pociEp] se pueden mover con cada simbolo del alfabeto,
si sí pregunta si se encontró un nuevo nucleo para calcular su C-é y posteriormente calcNucs de la nueva C-é.
Crea las nuevas trancisiones de AFD.
"""

def calcNucs(automata,epsilons,nucleos,pociEp,afd):
    t = {}
    #*Conjunto de estados del AFN para los cuales hay una transición con 'simbolo', a partir de cierto estado epsilons[pociEp]
    #*crea los núcleos para cada símbolo del alfabeto
    
    for simbolo in automata.alfabeto:
        m = mover(automata.transiciones,epsilons[pociEp],simbolo)

        if m not in nucleos:
            nucleos.append(m)
            cerraduraParcial = []
            for i in m:
                cerraduraE(automata.transiciones,i, cerraduraParcial)
            
            epsilons.append(list(dict.fromkeys(cerraduraParcial)))
            calcNucs(automata,epsilons,nucleos,len(epsilons)-1,afd)

        t[simbolo] = nucleos.index(m)

    afd.transiciones[pociEp] = t
    return

    
"""
cerraduraE(transiciones,estado,c): recibe un diccionario de trancisiones, el estado del cual se sacará la cerradura, una lista para guadar la cerradura
Pregunta si el estado tiene trancisiones con E, si sí llama recursivamente a cerraduraE con el estado el cual
se llega con epsilon desde el 'estado original'
"""
def cerraduraE(transiciones,estado,c):
    c.append(estado)
    try:
        for i in transiciones[estado]['E']:
            if i not in c:
                cerraduraE(transiciones,i,c)
    except:
        pass
    return

"""
mover(transiciones,estados,simbolo): recibe un diccionario de trancisiones, una lista de estados, un simbolo que pertenece al alfabeto del automata
Pregunta si cada estado tiene trancisiones con simbolo, si sí agrega el estado al que se llega con la trancisión a una lista

"""
def mover(transiciones,estados,simbolo):
    posibles = []
    for i in estados:
        try:
            a =transiciones[i][simbolo][0]
            posibles.append(a)
        except:
            pass
    posibles.sort()
    return posibles