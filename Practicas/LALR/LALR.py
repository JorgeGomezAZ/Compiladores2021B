from auxiliar import Producciones,Terminales,NoTerminales,epsilon, primero, Inicial

tabla = {}
subconjuntos = []
kernels = []
entradasMultiples= False

columnas = Terminales.copy()
columnas += ['$']
columnas += NoTerminales

"""
clase: ElementoLR1
atributos:
    produccion: lista
    pociPunto: entero
    simboloAnticiparion: char
"""
class ElementoLR1:
    def __init__(self, produccion,pociPunto,simboloAnticipacion):
        self.produccion = produccion
        self.pociPunto = pociPunto
        self.simboloAnticipacion = simboloAnticipacion

    def __eq__(self, o):
        if not isinstance(o, ElementoLR1):
            return NotImplemented
        return self.produccion == o.produccion and self.pociPunto == o.pociPunto and o.simboloAnticipacion == self.simboloAnticipacion

"""
clase: ElementoLR1
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

"""
extiendeGram():
    Agrega un producción a la gramática donde Inicial' -> Inicial
    y elimina el simbolo de epsion si existe
"""
def extiendeGram():
    Producciones.insert(0,[str(Inicial+"'"),Inicial])
    for p in Producciones:
        if epsilon in p[1]:
            p[1].remove(epsilon)
    return
"""
fucionaKernels(kernels):
modifica la tabla LALR al combinar los subconjuntos que tengan kernels similares
"""
def fucionaKernels(kernels):
    global entradasMultiples
    krnlsLR0 = []

    #Obtiene los elementos LR0 de la lista de kernels
    for k in kernels:
        l = []
        for i in k:
            e = ElementoLR0(i.produccion,i.pociPunto)
            if e not in l:
                l.append(e)
        krnlsLR0.append(l)
        
    #obtiene lista de kernels que comparten los mismos Elementos LR0
    similares = []
    for k in krnlsLR0:
        s = [i for i, x in enumerate(krnlsLR0) if x == k]
        if s not in similares and len(s)>1:
            similares.append(s)

    #toma los subconjuntos de los kernels similares y cambia los valores para que 
    #cada subconjunto tenga un mismo índice
    for key, value in tabla.items():
        for k, v in value.items():
            for sim in similares:
                for s in sim[1:]:
                    if str(s) == str(v):
                        tabla[key][k] = sim[0]
                    if 'd'+str(s) == v:
                        tabla[key][k] = 'd'+str(sim[0])

    
    #fusiona subconjuntos similares donde no existen conflictos y elimina 
    # los que subconjuntos que se usan para fucionar, excepto el primero 
    for sim in similares:
        for s in sim[1:]:
            for key, value in tabla[s].items():
                if key in tabla[sim[0]].keys():
                    if tabla[sim[0]][key] != value:
                        tabla[sim[0]][key] += "/"+value
                        entradasMultiples = True
                tabla[sim[0]][key] = value
            del tabla[s]
            
    return

"""
subconjuntosLR1():
recorre la  lista de kernels para aplicales la cerradura para crear nuvos subconjuntos
y después aplica la función mover a para crear nuevos kernels
"""
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
    #fucionaKernels(kernels)
    
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
devuelve: una lista de ElementoLR0's donde no_terminal -> a, pociPunto = 0 y simboloAnticipacion = Primero(beta+simbolo)
"""
def obtenerProducciones(no_terminal,anticipa):
    elementosNuevos= []
    for produccion in Producciones:
        if produccion[0] == no_terminal:
            elementosNuevos.append(ElementoLR1(produccion,0,anticipa))
    return elementosNuevos

"""
mover(subconjunto,simbolo):
recibe: subconjunto, una lista de ElementosLR1
        simbolo, un caracter (elemento de Terminal o NoTerminal)

recorre subconjunto para ver en qué producciones el punto esta antes de simbolo
para agregarlos a un nuevo kernerl con el punto avanzado por una pocición, y el simbolo de anticipacion se mantiene
Si es un kernerl repetido, no hace nada, si no, agrega el nuevo kernel a kernels.
Llama a accion() para llenar los elementos de la tabla LR(1)
"""
def mover(subconjunto,simbolo):
    nuevoKernel =[]
    for n in subconjunto:
        try:
            if n.produccion[1][n.pociPunto] == simbolo:
                nuevoKernel.append(ElementoLR1(n.produccion,n.pociPunto+1,n.simboloAnticipacion))
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
recibe: subconjunto, una lista de ElementosLR1
        simbolo, un caracter (elemento de Terminal o NoTerminal)
        nuevoKernel, una lista de ElementosLR1

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
            if kernels.index(nuevoKernel) not in tabla.keys():
                tabla[kernels.index(nuevoKernel)] = {}
            if k.simboloAnticipacion not in tabla[kernels.index(nuevoKernel)].keys():
                tabla[kernels.index(nuevoKernel)][k.simboloAnticipacion] = 'r'+str(prod)
            else:
                if tabla[kernels.index(nuevoKernel)][k.simboloAnticipacion] != 'r'+str(prod):
                    tabla[kernels.index(nuevoKernel)][k.simboloAnticipacion] += '/r'+str(prod)
                    entradasMultiples = True
            tabla[kernels.index(nuevoKernel)][k.simboloAnticipacion]=tabla[kernels.index(nuevoKernel)][k.simboloAnticipacion].replace("r0","acc")
    return

"""
cerraduraLR1(nucleo):
recibe: nucleo, una lista de ElementosLR1
aplica el algoritmo de la cerradura:
    para cada producción en el subconjunto nuevo donde el punto esté antes de un no terminal,
    se agregas las producciones del no terminal con el punto al inicio con simbolo de anticipación b
    donde b es primero lo que sigue de la producción que se va a agregar concatenado con el simbolo de
    anticipación de la elemento LR1 que se esta revisando 
regresa: una lista de ElementosLR1 (subconjunto nuevo)
"""
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

"""
imprimeTabla():
    
Imprime la tabla LALR de forma ordenada con filas y columnas 
y con la variable tabla, imprime el ínicie de la producción en la "celda" indicada
"""
def imprimeTabla():
    for c in columnas:
        print("\t",c,end="")
    print("")

    for i,f in sorted(tabla.items()):
        print(i,end="\t")
        for t in columnas:
            if t in tabla[i].keys():
                print(tabla[i][t],end="\t")
            else:
                print("",end="\t")
        print("")
    return

"""
pruebaCadenaLALR(cadena):
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
def pruebaCadenaLALR(cadena):
    og = cadena
    cadena+='$'
    cadena = [c for c in cadena]
    cadena.reverse()
    pila = [0]

    try:
        while True:
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

i = 1
print("\n\tGramática encontrada:")
print("No terminales: ",NoTerminales)
print("Terminales: ",Terminales)
print("Producciones:")
for p in Producciones:
    print("\t",i,p[0],"->",p[1])
    i+=1
print("Simbolo inicial: ",Inicial,"\n\n")


subconjuntosLR1()
imprimeTabla()
if not entradasMultiples:
    prueba = input("\n\nIngrese una cadena para probar si pertenece al lenguaje formado por la gramática:\n")
    pruebaCadenaLALR(prueba)
else:
    print("\nLa gramática no es LALR, no se pueden probar cadenas")