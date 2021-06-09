from gramatica import Producciones,Terminales,NoTerminales,epsilon, Inicial #elementos de la gramática
from PS import primero, siguiente #funciones auxiliares


tabla = {} #tabla LL(1) M
columnas = []

columnas = Terminales.copy() #columnas de la tabla 
columnas += ['$']

entradasMultiples= False

"""
construirTabla():
    
Construye la tabla LL(1) de la gramática con las reglas del algoritmo:
    Para cada producción A->a de la gramática de hace:
1.- Cada terminal t en Primero(a), se agrega A->a en M[A,t]
2.- Si épsilon esta en Primero(a), para cada elemento s en Siguente(A), se agrega A->a en M[A,s]
"""
def construirTabla():
    primeros =[]
    global entradasMultiples
    #recorre cada producción de la gramática
    for idx,prod in enumerate(Producciones):
        #recorre el lado derecho de la produccón
        for a in prod[1]:
            if prod[0] not in tabla.keys():
                tabla[prod[0]] = {}
            #obtiene Primero del lado derecho y si contiene a épsilon calcula siguiente del lado izquierdo
            primeros += primero(a)
            if epsilon in primeros:
                primeros.remove(epsilon)
                primeros += siguiente(prod[0])
            else:
                break

        #Agrega a tabla el número de producción en la pocición tabla[lado izq.][ele. de primero]
        #si ya existe un elemento ahí, se añaden juntos y existen entradas múltiples en la tabla
        for i in primeros:
            if i in tabla[prod[0]].keys():
                entradasMultiples = True
                tabla[prod[0]][i] = [tabla[prod[0]][i],idx]
            else:
                tabla[prod[0]][i] = idx
        primeros =[]
        
    return

"""
imprimeTabla():
    
Imprime la tabla LL(1) de forma ordenada con filas y columnas 
y con la variable tabla, imprime el ínicie de la producción en la "celda" indicada
"""
def imprimeTabla():
    for c in columnas:
        print("\t",c,end="")
    print("")

    for f in NoTerminales:
        print(f,end="\t")
        for t in columnas:
            if t in tabla[f].keys():
                print(tabla[f][t],end="\t")
            else:
                print("",end="\t")
        print("")
    print(entradasMultiples)
    return

"""
gramLL1():
Revisa si en la tabla construida existen entradas múltiples
devueve: True si no existen entradas múltiples,
         False si existen entradas múltiples y por lo tanto la gramática no es LL(1)
"""
def gramLL1():
    return not entradasMultiples

"""
pruebaCadenaLL1(cadena):
recibe: una cadena

Con la tabla contruida se analiza si la cadena de entrada pertenece o no a la gramática
Se agrega '$' al final de la cadena y se recorre de izquierda a derecha 
y se tiene una pila que inicia con '$' y el símbolo inicial que sirve para saber regla se nececita aplicar
"""
def pruebaCadenaLL1(cadena):
    og = cadena
    cadena+='$'
    cadena = [c for c in cadena]
    cadena.reverse()
    pila = ['$',Inicial] 
    try:
        while True:
            #si el tope t de la pila es un no terminal se consulta M[t,elemento de la cadena]
            #y se agrega de manera invertida el lado derecho de la producción encontrada
            if pila[-1] in NoTerminales:
                a = tabla[pila.pop()][cadena[-1]]
                for e in reversed(Producciones[a][1]):
                    pila.append(e)
            elif pila[-1] == cadena[-1] and cadena[-1] == '$': #tope  de pila y cadena son '$', fin del algoritmo.
                print("cadena",og,"aceptada")
                return
            #si el tope t de la pila es un terminal y es igual al elemento en revisión de la cadena
            elif pila[-1] == cadena[-1] and pila[-1] in Terminales:
                pila.pop()
                cadena.pop()
            #cuando el tope de la pila es épsilon
            elif pila[-1] == epsilon:
                pila.pop()
            else:   #error
                print("cadena no aceptada")
                return
    except KeyError:
        print("cadena no aceptada")
        return

