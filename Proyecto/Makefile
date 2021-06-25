proyecto: proyecto.l proyecto.y
	bison -d proyecto.y
	flex proyecto.l
	gcc -c proyecto.tab.c
	gcc -c lex.yy.c
	gcc -o proyecto lex.yy.o proyecto.tab.o -lfl
	./proyecto prueba.c