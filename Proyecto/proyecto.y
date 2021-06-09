%{
#  include <stdio.h>
%}
%token IDENTIFIER CONSTANT STRING_LITERAL
%token TYPE_NAME

%token CHAR INT CONST VOID EQ_OP

%token IF WHILE RETURN

%start translation_unit
%%

primary_expression
	: IDENTIFIER 				
	| CONSTANT					
	| STRING_LITERAL			
	| '(' expression ')'
	;

postfix_expression
	: primary_expression
	| postfix_expression '(' argument_expression_list ')'
	;

argument_expression_list
	: assignment_expression
	| argument_expression_list ',' assignment_expression
	;

unary_expression
	: postfix_expression
	| unary_operator unary_expression
	;

unary_operator
	: '&'
	| '-'
	;


multiplicative_expression
	: unary_expression
	| multiplicative_expression '*' unary_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Multiplicar ambos valores y guardar el resultado \n" );
									printf("4. Regresar el resultado\n" );
									}
	| multiplicative_expression '/' unary_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Dividir ambos valores y guardar el resultado \n" );
									printf("4. Regresar el resultado\n" );
									}
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' multiplicative_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Sumar ambos valores y guardar el resultado \n" );
									printf("4. Regresar el resultado\n" );
									}
	| additive_expression '-' multiplicative_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Restar ambos valores y guardar el resultado \n" );
									printf("4. Regresar el resultado\n" );
									}
	;

relational_expression
	: additive_expression
	| relational_expression '<' relational_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Comparar el valor de la izquierda es menor al de la derecha \n" );
									printf("4. Regresar el resultado, 1 si cumple, 0 si no\n" );
									}
	| relational_expression '>' relational_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Comparar el valor de la izquierda es mayor al de la derecha \n" );
									printf("4. Regresar el resultado, 1 si cumple, 0 si no\n" );
									}
	;

equality_expression
	: relational_expression
	| equality_expression EQ_OP relational_expression		{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la primer expresión\n");
									printf("2. Calcular/obtener el valor de la segunda expresión\n");
									printf("3. Comparar los valores para ver si son iguales\n" );
									printf("4. Regresar el resultado, 1 si cumple, 0 si no\n" );
									}
	;

assignment_expression
	: equality_expression  				
	| unary_expression assignment_operator assignment_expression 	{
									// prototipo de regla semántica:
									printf("1. Calcular/obtener el valor de la expresión\n");
									printf("2. Obtener la dirección de VARIABLE.\n");
									printf("3. Copiar el valor de la expresioń a la dirección de la VARIABLE\n" );
									}
	;

assignment_operator
	: '='
	;

expression
	: assignment_expression
	| expression ',' assignment_expression
	;

constant_expression
	: equality_expression
	;

declaration
	: declaration_specifiers ';'
	| declaration_specifiers init_declarator_list ';'
	;

declaration_specifiers
	: type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
	;

init_declarator_list
	: init_declarator
	| init_declarator_list ',' init_declarator
	;

init_declarator
	: declarator
	| declarator '=' initializer
	;

type_specifier
	: VOID
	| CHAR
	| INT
	;


type_qualifier
	: CONST
	;

declarator
	: direct_declarator
	;

direct_declarator
	: IDENTIFIER
	| '(' declarator ')'
	| direct_declarator '[' constant_expression ']'
	| direct_declarator '[' ']'
	| direct_declarator '(' parameter_type_list ')'
	| direct_declarator '(' identifier_list ')'
	| direct_declarator '(' ')'
	;

parameter_type_list
	: parameter_list
	;

parameter_list
	: parameter_declaration
	| parameter_list ',' parameter_declaration
	;

parameter_declaration
	: declaration_specifiers declarator
	| declaration_specifiers
	;

identifier_list
	: IDENTIFIER
	| identifier_list ',' IDENTIFIER
	;


initializer
	: assignment_expression
	| '{' initializer_list '}'
	| '{' initializer_list ',' '}'
	;

initializer_list
	: initializer
	| initializer_list ',' initializer
	;

statement
	: compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	;


compound_statement
	: '{' '}'
	| '{' statement_list '}'
	| '{' declaration_list '}'
	| '{' declaration_list statement_list '}'
	;

declaration_list
	: declaration
	| declaration_list declaration
	;

statement_list
	: statement
	| statement_list statement
	;

expression_statement
	: ';'
	| expression ';'
	;

selection_statement
	: IF '(' expression ')' statement
	;

iteration_statement
	: WHILE '(' expression ')' statement
	;
	
	jump_statement
	: RETURN ';'
	| RETURN expression ';'
	;

translation_unit
	: external_declaration
	| translation_unit external_declaration
	;

external_declaration
	: function_definition
	| declaration
	;

function_definition
	: declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement
	| declarator declaration_list compound_statement
	| declarator compound_statement
	;

%%

extern char yytext[];
extern int column;

main()
{
  yyparse();
}

yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}
