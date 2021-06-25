%{
	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>

	extern FILE *yyin;;
	FILE * f1;

	//#include "proy.h"
	//int main(){int a;int b;char c;a=5;b = a*2;}
	struct simbolo{
        char *nombre;
        int val;
        short tipo;
		unsigned char fn;
		unsigned short registro;
    };
    
	struct simbolo tabla_de_simbolos[256];
    int indice;
	unsigned short regActual;
	void yyerror (char const *s);

	void AgregaVar(short tipo, struct simbolo *var);
	int VarExistente(char *var);
	int buscaPorNom(char *nombre);
	void AgregaValI(char *nombre,int val);
	int AgregaConstI(int val);
	int modificaReg(int r1, int r2, char op);
	int buscaPorReg(int r);
	int yylex();
%}
%union {
  int d;
  char *cad;
  struct simbolo *s;
  short tipo;
}
%token <d>NUMBER
%token <cad> IDENTIFIER STRING_LITERAL

%token<tipo> CHAR INT VOID CONSTANT
%token EQ_OP
%token IF WHILE RETURN

%type <tipo> type_specifier declaration_specifiers
%type <cad> direct_declarator  declarator 
%type <s> init_declarator_list init_declarator
%type <d> primary_expression postfix_expression unary_expression multiplicative_expression additive_expression
%type <d> relational_expression equality_expression assignment_expression
%start translation_unit

%%
translation_unit
	: external_declaration	{printf("termina el programa\n");}
	| translation_unit external_declaration
	;

external_declaration
	: function_definition		{//printf("agrega funcion %s a la tala de simbolos\n",$1);
								}
	| declaration
	;

function_definition
	: declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement {}
    ;

declaration_specifiers
	: type_specifier	{$$ = $1;}
	;

type_specifier
	: VOID	{ $$ = $1;}
	| CHAR	{ $$ = $1;}
	| INT 	{ $$ = $1;}
	;
                                                        
declarator
	: direct_declarator {$$ = $1;}
	;

direct_declarator
	: IDENTIFIER 		{$$=$1;}
	| direct_declarator '(' ')'	{$$ = $1;}
	;

compound_statement
	: '{' declaration_list '}' {}
	| '{' declaration_list statement_list '}'
	;

statement_list
	: statement
	| statement_list statement
	;

statement
	: compound_statement
	| expression_statement
	;
expression_statement
	: ';'
	| expression ';'
	;

expression
	: assignment_expression {}
	;

declaration_list
	: declaration
	| declaration_list declaration
	;

declaration
	: declaration_specifiers ';'
	| declaration_specifiers init_declarator_list ';'{AgregaVar($1,$2);
											fprintf(f1,"const v%d, 0x%x\n",$2->registro,$2->val);
													
	}
	;

init_declarator_list
	: init_declarator	{$$ = $1;
		//printf("%s\n",$1->nombre);
	}
    ;

init_declarator
	: IDENTIFIER					{$$->nombre = strdup($1);}
	| IDENTIFIER '=' assignment_expression	{$$->nombre = strdup($1);
											$$->val = tabla_de_simbolos[buscaPorReg($3)].val;
											}
	;



primary_expression
	: IDENTIFIER	{
					$$ = buscaPorNom($1);
	}
	| NUMBER		{//usa constante entera
		$$ = AgregaConstI($1);
					
	//| STRING_LITERAL			
	}			

	;

postfix_expression
	: primary_expression	{$$ = $1;}
	;
unary_expression
	: postfix_expression	{$$ = $1;}
	| '-' unary_expression	{$$ = modificaReg($2, $2, '!');}
	;

multiplicative_expression
	: unary_expression		{$$ = $1;}
	| multiplicative_expression '*' unary_expression	{$$ = modificaReg($1, $3, '*');}	
	| multiplicative_expression '/' unary_expression	{$$ = modificaReg($1, $3, '/');}	
	;

additive_expression
	: multiplicative_expression	{$$ = $1;}
	| additive_expression '+' multiplicative_expression		{$$ = modificaReg($1, $3, '+');}	
	| additive_expression '-' multiplicative_expression		{$$ = modificaReg($1, $3, '-');}	
	;

relational_expression
	: additive_expression	{$$ = $1;}
	| relational_expression '<' relational_expression		{}
	| relational_expression '>' relational_expression		{}
	;

equality_expression
	: relational_expression	{$$ = $1;}
	| equality_expression EQ_OP relational_expression		{}
	;

assignment_expression
	: equality_expression	{$$ = $1;}	
	| IDENTIFIER '=' assignment_expression 	{ AgregaValI($1,tabla_de_simbolos[buscaPorReg($3)].val);
											

	}
	;
%%
int main(int argc, char *argv[])
{
  	yyin = fopen(argv[1], "r");
	f1=fopen("codigoIntermedio.txt","w");
	
    indice = 0;
	regActual = 0;
   	yyparse();
	for (int i = 0;i!= indice;i++){
	  	printf("Nombre: %s\tTipo: %d\tValor: %d\t Reg:%d\n",tabla_de_simbolos[i].nombre,tabla_de_simbolos[i].tipo,tabla_de_simbolos[i].val,tabla_de_simbolos[i].registro);
	}
	fclose(yyin);
	fclose(f1);
    return 0;
}
void yyerror (char const *s) {
   	fprintf (stderr, "%s\n", s);
	exit(1);
}

void AgregaVar(short tipo, struct simbolo *var){
	if (VarExistente(var->nombre)!=-1){
		yyerror("variable previamente declarada");
	}
	var->tipo = tipo;
	var->registro = regActual;
	tabla_de_simbolos[indice] = *var;
	
	fprintf(f1,"const-wide/32 v%x, 0x0\n",var->registro);

	regActual += 2;
	indice++;
}

int VarExistente(char *var){
	for (int i = 0;i!= indice;i++){
		if(strcmp(var,tabla_de_simbolos[i].nombre)==0){
			return i;
		}
	}
	return -1;
}
int buscaPorNom(char *nombre){
	int inx = VarExistente(nombre);
	if(inx == -1)
		yyerror("variable no declarada");
	else
		return tabla_de_simbolos[inx].registro;
}

void AgregaValI(char *nombre,int val){
	int inx = VarExistente(nombre);
	if(inx ==-1)
		yyerror("variable no declarada");
	else{
		tabla_de_simbolos[inx].val = val;
		fprintf(f1,"move v%x, v%x\n",tabla_de_simbolos[inx].registro,val);
	}
}

int AgregaConstI(int val){
	struct simbolo *var;
	var->tipo = CONSTANT;
	var->registro = regActual;

	var->val = val;
	var->nombre = "const";
	fprintf(f1,"const-wide/32 v%x, 0x%x\n",var->registro,val);
	tabla_de_simbolos[indice] = *var;
	int i = indice;

	indice++;
	regActual += 2;
	
	return var->registro;
}
int buscaPorReg(int r){
	int inx;
	for (int i = 0;i!= indice;i++){
		if(r == tabla_de_simbolos[i].registro){
			return i;
		}
	}
	return -1;
}

int modificaReg(int r1, int r2, char op){
	int i1 = buscaPorReg(r1);
	int i2 = buscaPorReg(r2);
	int res;
	switch (op) {
    case '+':
        res = tabla_de_simbolos[i1].val + tabla_de_simbolos[i2].val;
        break;
    case '-':
        res = tabla_de_simbolos[i1].val - tabla_de_simbolos[i2].val;
        break;
    case '*':
        res = tabla_de_simbolos[i1].val * tabla_de_simbolos[i2].val;
        break;
    case '/':
        res = tabla_de_simbolos[i1].val / tabla_de_simbolos[i2].val;
        break;
	case '!':
        res = tabla_de_simbolos[i1].val * -1;
        break;
    default:
        yyerror("error\n");
	
    }
	struct simbolo *var;
	var->tipo = CONSTANT;
	var->registro = regActual;
	var->val = res;
	var->nombre = "const";
	fprintf(f1,"const-wide/32 v%x, 0x%x\n",var->registro,res);
	tabla_de_simbolos[indice] = *var;
	int i = indice;

	indice++;
	regActual += 2;
	return regActual-2;
}