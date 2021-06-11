# AUTOR: Jorge Arturo Gomez Ojeda

# DESCRIPCIÓN: Implementación del algoritmo de McNaughton-Yamada-Thompson para convertir una expresión regular en un AFN,
#              algoritmo de subconjuntos para convertir un AFN a un AFD,
#              construir un AFD a partir de una expresion regular por el método del árbol,
#              algoritmo de minimización de un AFD. 

# OBSERVACIONES:
# Los caracteres aceptados para la expresion regular son las letras minusculas a-z,
# se debe de usar el caracter E para representar épsilon
# los operadores de la expresion regular deben ser:
#                                             |  (pleca o barra vertica) para la unión
#                                             *  (asterisco) para la cerradura de kleene
#                                             () (parentesis) para agrupaciones 

# Se emplea las funciones ER_AFD.py, subconjuntos.py y minimizacion.py

# EJECUCIÓN: python automatas.py

import re
from ER_AFD import ex2afd
from subconjuntos import subconjuntos
from minimizacion import minimizar
from Automata import AFN


"""
parentesis(expresion): Recibe: una expresión regular en forma de cadena 
Revisa si la expresión tiene sus parentesis en orden
Regresa: la expresión regular con los marcadores agregados
"""
def parentesis(expresion):
    pilaParentesis = []
    for i in expresion:
        if i == '(':
            pilaParentesis.append(i)
        if i == ')':
            if len(pilaParentesis) == 0:
                return False
            else:
                pilaParentesis.pop()
    if len(pilaParentesis) == 0:
        return True
    return False 

"""
agregaMarcadores(er): Recibe: una expresión regular en forma de cadena 
Agrega a la exr el caracter '.' para simbolizar la operación de concatenación
Regresa: la expresión regular con los marcadores agregados
"""
def agregaMarcadores(er):
    i = 0
    nueva = ''
    while i < len(er)-1:
        nueva += er[i]
        if re.search(r'[^(|E]', er[i]) and re.search(r'[^)*|E]', er[i+1]):
            nueva += '.'
        i += 1
    nueva += er[-1]
    return nueva

"""
precedencia(operador): Recibe: un operador o parentesis de expresiones regulares  
Regresa: Un nivel de precedencia predeterminado
"""  
def precedencia(operador):
    precedencia = 0

    if operador == '*':
        precedencia=3
    elif operador == '.':
        precedencia=2
    elif operador == '|':
        precedencia=1
    elif operador == '(':
        precedencia=0
    elif operador == ')':
        precedencia=4
    return precedencia
            

"""
convertPost(er): recibe una expresión regular en forma de cadena 
Efecto: Convierte la expresion regular a una forma postfija
"""
def convertPost(er):
    er = agregaMarcadores(er)
    pilaOperadores=[]
    postfija= []
    for i in er:
        if re.search(r'[*.|(]', i):
            if len(pilaOperadores) == 0 or i =='(':
                pass
            else:
                while precedencia(i) <= precedencia(pilaOperadores[-1]):
                    postfija.append(pilaOperadores.pop())
                    if len(pilaOperadores) == 0:
                        break
            pilaOperadores.append(i)
        elif i == ')':
            while True:
                tope = pilaOperadores.pop()
                if tope == '(':
                    break
                postfija.append(tope)
                if len(pilaOperadores) == 0:
                    break
        else:
            postfija.append(i)

    while len(pilaOperadores) != 0:
        postfija.append(pilaOperadores.pop())

    return postfija



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




menu = {}
menu['1']="Expresion Regular a AFN." 
menu['2']="Expresion Regular a AFD."
menu['3']="Salir."
opciones=menu.keys()
for n in opciones: 
    print(n, menu[n])

selection=input("\nSelecciona una opción:")

if selection =='1': 
    regex = input("\n\nIngrese una expresión regular, use letras minusculas a-z para caracteres y E para épsilon: ")
    if not re.search(r'^[a-z*|()E]+$', regex):
        print("La expresión regular solo debe de contener los caracteres [a-z], *, | , (, ), E")
        exit(0)
    print("----------------AFN-------------------")
    afn = construyeAutomata(convertPost(regex))
    afn.imprimeA()
    if '1' == input("\nIngrese 1 para convertir el AFN a un AFD: "):
        print("\n")
        print("\n----------------AFD-------------------")
        afd = subconjuntos(afn)
        afd.imprimeA()
        if '1' == input("\nIngrese 1 para minimizar el AFD: "):
            print("\n----------------AFN MÍNIMO----------------")
            minimizar(afd).imprimeA()
            input("Presione ENTER para continuar...")

elif selection == '2':
    regex = input("\n\nIngrese una expresión regular, use letras minusculas a-z para caracteres y E para épsilon: ")
    if not re.search(r'^[a-z*|()E]+$', regex):
        print("La expresión regular solo debe de contener los caracteres [a-z], *, | , (, ), E")
        exit(0)
    afd = ex2afd(convertPost(regex))
    afd.imprimeA()
    if '1' == input("\nIngrese 1 para minimizar el AFD: "):
        print("\n\n----------------AFN MÍNIMO----------------")
        minimizar(afd).imprimeA()
        input("Presione ENTER para continuar...")

elif selection == '5': 
    pass
else: 
    print("\nIngrese una opcion válida\n") 