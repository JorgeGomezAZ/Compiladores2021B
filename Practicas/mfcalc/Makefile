mfcalc: mfcalc.y symbol.c init_table.c calc.h
	bison -d mfcalc.y
	gcc -c mfcalc.tab.c
	gcc -c init_table.c 
	gcc -c symbol.c 
	gcc init_table.o mfcalc.tab.o symbol.o -lm -o mfcalc