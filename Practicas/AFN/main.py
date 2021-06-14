# AUTOR: Jorge Arturo Gomez Ojeda

# DESCRIPCIÓN: Implementación del algoritmo de McNaughton-Yamada-Thompson para convertir una expresión regular en un AFN,
#              algoritmo de subconjuntos para convertir un AFN a un AFD,
#              algoritmo de minimización de un AFD. 

# OBSERVACIONES:
# Los caracteres aceptados para la expresion regular son las letras minusculas a-z,
# se debe de usar el caracter E para representar épsilon
# los operadores de la expresion regular deben ser:
#                                             |  (pleca o barra vertica) para la unión
#                                             *  (asterisco) para la cerradura de kleene
#                                             () (parentesis) para agrupaciones 

#! Se emplea las funciones ER_AFD.py, subconjuntos.py y minimizacion.py

# EJECUCIÓN: python main.py

from re_afn import construyeAutomata
from subconjuntos import subconjuntos
import re

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


regex = input("\n\nIngrese una expresión regular, use letras minusculas a-z para caracteres y E para épsilon: ")
if not re.search(r'^[a-z*|()E]+$', regex):
    print("La expresión regular solo debe de contener los caracteres [a-z], *, | , (, ), E")
    exit(0)
if not parentesis(regex):
    print("La expresion esta esta incorrecta ")
print("----------------AFN-------------------")
afn = construyeAutomata(convertPost(regex))
afn.imprimeA()
if '1' == input("\nIngrese 1 para convertir el AFN a un AFD: "):
    print("\n")
    print("\n----------------AFD-------------------")
    afd = subconjuntos(afn)
    afd.imprimeA()
