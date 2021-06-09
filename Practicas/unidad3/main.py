#from LL1 import gramLL1, construirTabla, imprimeTabla,pruebaCadenaLL1
# from LR0 import extiendeGram, subconjuntosLR0,imprimeTabla, pruebaCadenaLR0
# from gramatica import Inicial, Producciones,Terminales,NoTerminales,epsilon
# from PS import primero, siguiente
from LR1 import subconjuntosLR1, pruebaCadenaLR1
# print(Producciones)
# print(Terminales)
# print(NoTerminales)
# print(Inicial)

# for p in NoTerminales:
#     print(siguiente(p))
#-------------------------------------------
# construirTabla()
# imprimeTabla()
# if gramLL1():
#     pruebaCadenaLL1('i*n/n+(i*n)')
# else:
#     print("No se puede probar la cadena ya que la gramática no es LL(1)")
#-----------------------------------------
# extiendeGram()
subconjuntosLR1()
pruebaCadenaLR1('cdcd')
# imprimeTabla()
# pruebaCadenaLR0("baa")