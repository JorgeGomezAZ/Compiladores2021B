from PS import primero
from LR0 import extiendeGram, posiblesMovimientos
from gramatica import Producciones,Terminales,NoTerminales,epsilon, Inicial

tabla = {}
subconjuntos = []
kernels = []

columnas = Terminales.copy()
columnas += ['$']
columnas += NoTerminales

class ElementoLR1:
    def __init__(self, produccion,pociPunto,simboloAnticipacion):
        self.produccion = produccion
        self.pociPunto = pociPunto
        self.simboloAnticipacion = simboloAnticipacion

    def __eq__(self, o):
        if not isinstance(o, ElementoLR1):
            return NotImplemented
        return self.produccion == o.produccion and self.pociPunto == o.pociPunto and o.simboloAnticipacion == self.simboloAnticipacion



def imprimeListaElementos(l):
    for n in l:
        print(n.produccion,n.pociPunto,n.simboloAnticipacion)

def subconjuntosLR1():
    extiendeGram()
    #todos los kernels que se han encontrado
    global kernels
    global subconjuntos

    elementoInicial = ElementoLR1(Producciones[0],0,'$')
    kernels.append([elementoInicial])
    
    i = 0
    while i < len(kernels):
        subconjuntos.append(cerraduraLR1(kernels[i]))
        #imprimeListaElementos(subconjuntos[i])
        movimientos = posiblesMovimientos(subconjuntos[i])
        #print(movimientos)
        for s in movimientos:
            mover(subconjuntos[i],s)
        i +=1

    for s in subconjuntos:
        imprimeListaElementos(s)
        print("")
    print(tabla)
    imprimeTabla()
    return

def obtenerProducciones(no_terminal,anticipa):
    elementosNuevos= []
    for produccion in Producciones:
        if produccion[0] == no_terminal:
            elementosNuevos.append(ElementoLR1(produccion,0,anticipa))
    return elementosNuevos

def mover(subconjunto,simbolo):
    nuevoSubconjunto =[]
    for n in subconjunto:
        try:
            if n.produccion[1][n.pociPunto] == simbolo:
                nuevoSubconjunto.append(ElementoLR1(n.produccion,n.pociPunto+1,n.simboloAnticipacion))
        except IndexError:
            pass
    if nuevoSubconjunto not in kernels:
        kernels.append(nuevoSubconjunto)


    if subconjuntos.index(subconjunto) not in tabla.keys():
        tabla[subconjuntos.index(subconjunto)] = {}

    if simbolo in NoTerminales:
        tabla[subconjuntos.index(subconjunto)][simbolo] = kernels.index(nuevoSubconjunto)
    elif simbolo in Terminales:
        tabla[subconjuntos.index(subconjunto)][simbolo] = 'd'+str(kernels.index(nuevoSubconjunto))

    for k in nuevoSubconjunto:
        if k.pociPunto == len(k.produccion[1]):
            prod = Producciones.index(k.produccion)
            if kernels.index(nuevoSubconjunto) not in tabla.keys():
                tabla[kernels.index(nuevoSubconjunto)] = {}
            tabla[kernels.index(nuevoSubconjunto)][k.simboloAnticipacion] = 'r'+str(prod)
            if tabla[kernels.index(nuevoSubconjunto)][k.simboloAnticipacion] == 'r0':
                tabla[kernels.index(nuevoSubconjunto)][k.simboloAnticipacion] = 'acc'

def cerraduraLR1(nucleo):
    cerradura= nucleo.copy()
    produccionesAgregadas ={}
    for n in cerradura:
        try:
            if n.produccion[1][n.pociPunto] in NoTerminales:
                if n.simboloAnticipacion in produccionesAgregadas.keys():
                    if produccionesAgregadas[n.simboloAnticipacion] == n.produccion[1][n.pociPunto]:
                        continue
                produccionesAgregadas[n.simboloAnticipacion] = n.produccion[1][n.pociPunto]
                beta =  n.produccion[1][n.pociPunto+1:] + n.simboloAnticipacion
                primeros=[]
                for b in beta:
                    if b == '$':
                        primeros.append('$')
                    else:
                        primeros+=primero(b)
                    if epsilon not in primeros:
                        break
                    primeros.remove(epsilon)
                for p in primeros:
                    cerradura += obtenerProducciones(n.produccion[1][n.pociPunto],p)
        except:
            pass
    return cerradura

def imprimeTabla():
    for c in columnas:
        print("\t",c,end="")
    print("")

    for i,f in enumerate(kernels):
        print(i,end="\t")
        for t in columnas:
            if t in tabla[i].keys():
                print(tabla[i][t],end="\t")
            else:
                print("",end="\t")
        print("")
    return

def pruebaCadenaLR1(cadena):
    og = cadena
    cadena+='$'
    cadena = [c for c in cadena]
    cadena.reverse()
    pila = [0]

    try:
        while True:
            print(cadena)
            print(pila)
            if tabla[pila[-1]][cadena[-1]][0] == 'd':
                desplaza = int(tabla[pila[-1]][cadena.pop()][1:])
                pila.append(desplaza)
            elif tabla[pila[-1]][cadena[-1]][0] == 'r':
                anuncio = Producciones[int(tabla[pila[-1]][cadena[-1]][1:])]
                for i in anuncio[1]:
                    pila.pop()
                pila.append(tabla[pila[-1]][anuncio[0]])
            elif tabla[pila[-1]][cadena[-1]] == 'acc':
                print(og,"cadena aceptada")
                return
    except:
        print("cadena no aceptada")
    return