from gramatica import Producciones,Terminales,NoTerminales, Inicial
from PS import siguiente

entradasMultiples= False

tabla = {} #Tabla LR(0)
subconjuntos = []
kernels = []

columnas = Terminales.copy()
columnas += ['$']
columnas += NoTerminales
"""
clase: ElementoLR0
atributos:
    produccion: lista
    pociPunto: entero
"""
class ElementoLR0:
    def __init__(self, produccion,pociPunto):
        self.produccion = produccion
        self.pociPunto = pociPunto

    def __eq__(self, o):
        if not isinstance(o, ElementoLR0):
            return NotImplemented
        return self.produccion == o.produccion and self.pociPunto == o.pociPunto


#para debuggear
def imprimeListaElementos(l):
    for n in l:
        print(n.produccion,n.pociPunto)

"""
extiendeGram():
    Agrega un producción a la gramática donde Inicial' -> Inicial
"""
def extiendeGram():
    Producciones.insert(0,[str(Inicial+"'"),Inicial])
    return

"""
posiblesMovimientos(subconjunto):
recibe: una lista de ElementosLR0
recorre la lista para consultar qué elementos existen después del punto . para cada producción
devuelve: una lista de caracteres (elementos terminales o no terminales) sin repeticiones
"""
def posiblesMovimientos(subconjunto):
    elementos = []
    for e in subconjunto:
        try:
            elementos.append(e.produccion[1][e.pociPunto])
        except IndexError:
            pass
    return list(dict.fromkeys(elementos))

"""
obtenerProducciones(no_terminal):
recibe: un caracter (elemento de NoTerminal)
recorre las producciones para ver cuando aparece no_terminal del lado izq.
devuelve: una lista de ElementoLR0's donde no_terminal -> a y pociPunto = 0
"""
def obtenerProducciones(no_terminal):
    elementosNuevos= []
    for produccion in Producciones:
        if produccion[0] == no_terminal:
            elementosNuevos.append(ElementoLR0(produccion,0))
    return elementosNuevos

"""
mover(subconjunto,simbolo):
recibe: subconjunto, una lista de ElementosLR0
        simbolo, un caracter (elemento de Terminal o NoTerminal)

recorre subconjunto para ver en qué producciones el punto esta antes de simbolo
para agregarlos a un nuevo kernerl con el punto avanzado por una pocición
Si es un kernerl repetido, no hace nada, si no, agrega el nuevo kernel a kernels.
Llama a accion() para llenar los elementos de la tabla LR(0)
"""
def mover(subconjunto,simbolo):
    nuevoKernel =[]
    for n in subconjunto:
        try:
            if n.produccion[1][n.pociPunto] == simbolo:
                nuevoKernel.append(ElementoLR0(n.produccion,n.pociPunto+1))
        except IndexError:
            pass
    if nuevoKernel not in kernels:
        kernels.append(nuevoKernel)

    if subconjuntos.index(subconjunto) not in tabla.keys():
        tabla[subconjuntos.index(subconjunto)] = {}
    accion(simbolo,subconjunto,nuevoKernel)
    return

"""
accion(simbolo,subconjunto,nuevoKernel):
recibe: subconjunto, una lista de ElementosLR0
        simbolo, un caracter (elemento de Terminal o NoTerminal)
        nuevoKernel, una lista de ElementosLR0

Si el subconjunto de mueve a con un terminal, se agrega 'desplaza con nuevo Kernel'
Si el subconjunto de mueve a con un no terminal, se agrega 'mueve/ir a nuevo Kernel'
Si el nuevo Kernel contiene el punto al final de la producción, se agrega 'reduce al ínice de prod.'
    excepto cuando es la producción extendida, ahí se agrega 'acc'
"""
def accion(simbolo,subconjunto,nuevoKernel):
    global entradasMultiples
    if simbolo in NoTerminales:
        if simbolo not in tabla[subconjuntos.index(subconjunto)].keys():
            tabla[subconjuntos.index(subconjunto)][simbolo] = kernels.index(nuevoKernel)
        else:
            entradasMultiples = True
            tabla[subconjuntos.index(subconjunto)][simbolo] = str(tabla[subconjuntos.index(subconjunto)][simbolo])+'/'+str(kernels.index(nuevoKernel))
    elif simbolo in Terminales:
        if simbolo not in tabla[subconjuntos.index(subconjunto)].keys():
            tabla[subconjuntos.index(subconjunto)][simbolo] = 'd'+str(kernels.index(nuevoKernel))
        else:
            tabla[subconjuntos.index(subconjunto)][simbolo] += '/d'+str(kernels.index(nuevoKernel))
            entradasMultiples = True

    for k in nuevoKernel:
        if k.pociPunto == len(k.produccion[1]):
            prod = Producciones.index(k.produccion)
            if k.produccion[1] == Inicial:
                if kernels.index(nuevoKernel) not in tabla.keys():
                    tabla[kernels.index(nuevoKernel)] = {}
                    tabla[kernels.index(nuevoKernel)]['$'] = 'acc'
                else:
                    tabla[kernels.index(nuevoKernel)]['$'] += '/acc'
                    entradasMultiples = True
            for s in siguiente(k.produccion[0]):
                if kernels.index(nuevoKernel) not in tabla.keys():
                    tabla[kernels.index(nuevoKernel)] = {}
                if s not in tabla[kernels.index(nuevoKernel)].keys():
                    tabla[kernels.index(nuevoKernel)][s] = 'r'+str(prod)
                else:
                    if tabla[kernels.index(nuevoKernel)][s] != 'r'+str(prod):
                        tabla[kernels.index(nuevoKernel)][s] += '/r'+str(prod)
                        entradasMultiples = True
                

    return

"""
subconjuntosLR0():
recorre la  lista de kernels para aplicales la cerradura para crear nuvos subconjuntos
y después aplica la función mover a para crear nuevos kernels
"""
def subconjuntosLR0():
    #todos los kernels que se han encontrado
    global kernels
    global subconjuntos

    #agrega la producción extendida como primer kernel  
    elementoInicial = ElementoLR0(Producciones[0],0)
    kernels.append([elementoInicial])
    
    
    i = 0
    while i < len(kernels):
        subconjuntos.append(cerraduraLR0(kernels[i]))
        movimientos = posiblesMovimientos(subconjuntos[i])
        for s in movimientos:
            mover(subconjuntos[i],s)
        i +=1
    return

"""
cerraduraLR0(nucleo):
recibe: nucleo, una lista de ElementosLR0
aplica el algoritmo de la cerradura:
    para cada producción en el subconjunto nuevo donde el punto esté antes de un no terminal,
    se agregas las producciones del no terminal con el punto al inicio
"""
def cerraduraLR0(nucleo):
    cerradura= nucleo.copy()
    produccionesAgregadas =[]
    for n in cerradura:
        try:
            if n.produccion[1][n.pociPunto] in NoTerminales and n.produccion[1][n.pociPunto] not in produccionesAgregadas:
                produccionesAgregadas.append(n.produccion[1][n.pociPunto])
                cerradura += obtenerProducciones(n.produccion[1][n.pociPunto])
        except:
            pass
    return cerradura


"""
gramLR0():
Revisa si en la tabla construida existen entradas múltiples
devueve: True si no existen entradas múltiples,
         False si existen entradas múltiples y por lo tanto la gramática no es LR(0)
"""
def gramLR0():
    return not entradasMultiples

"""
imprimeTabla():
    
Imprime la tabla LR(0) de forma ordenada con filas y columnas 
y con la variable tabla, imprime el ínicie de la producción en la "celda" indicada
"""
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

"""
pruebaCadenaLR0(cadena):
recibe: una cadena

Con la tabla contruida se analiza si la cadena de entrada pertenece o no a la gramática
Se agrega '$' al final de la cadena y se recorre de izquierda a derecha,
se crea una pila que tiene el subconjunto 0 
se consulta la pocisión de la tabla que intesecta el elemento más izquierdo de la cadena con el tope de la pila
si se encuentra un d(desplazamiento), se recorre al siguiente elemento de la cadena y 
a la pila de agrega el subconjunto que indica el desplazamiento
si se encuentra un r(reducción), se remueven el numero de elementos de que estan del lado derecho de la producción indicada
y el siguente paso es consultar M[tope de la pila, lado izq. de la prod]
cuando se llegue M[,] = acc. ;la cadena es aceptada. 
"""
def pruebaCadenaLR0(cadena):
    og = cadena
    cadena+='$'#(i)$
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

    