import re
epsilon = 'E'
Producciones = []
NoTerminales = []
Terminales = []
Inicial = None

with open('./gramatica.txt', encoding="utf8") as f:
    for linea in f.readlines():
        if linea[-1] == '\n':
            linea = linea[:-1]
        Producciones.append([linea[0],linea[3:]])
for p in Producciones:
    if p[0] not in NoTerminales:
        if p[0] == epsilon:
            print("'E' no se puede usar como no terminal ya que se usa para representar a épsilon")
            exit(1)
        NoTerminales.append(p[0]) 
    for t in p[1]:
        if re.search(r'[a-zE.+*/;,()-]', t):
            if t not in Terminales:
                Terminales.append(t)
    if epsilon in Terminales:
        Terminales.remove(epsilon)
Inicial = Producciones[0][0]