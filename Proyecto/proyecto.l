%option noyywrap
%{
	#include <stdio.h>
	#include <stdlib.h>
	#include "proyecto.tab.h"
	//#include "proy.h"
%}
%%
"char"			{ yylval.tipo = CHAR;return(CHAR); }
"if"			{ return(IF); }
"int"			{ yylval.tipo = INT;return(INT); }
"return"		{ return(RETURN); }
"void"			{ yylval.tipo = VOID;return(VOID); }
"while"			{ return(WHILE); }
"=="			{ return(EQ_OP); }

[a-zA-Z_]([a-zA-Z_]|[0-9])*		{ yylval.cad=strdup(yytext);return(IDENTIFIER); }

[0-9]+"."[0-9]* |
"."?[0-9]+		    { yylval.d = atoi(yytext); return (NUMBER); }

L?\"(\\.|[^\\"])*\"	{ return(STRING_LITERAL); }

";"			{ return(';'); }
("{")		{ return('{'); }
("}")		{ return('}'); }
","			{ return(','); }
"="			{ return('='); }
"("			{ return('('); }
")"			{ return(')'); }
("[")		{ return('['); }
("]")		{ return(']'); }
"."			{ return('.'); }
"&"			{ return('&'); }
"-"			{ return('-'); }
"+"			{ return('+'); }
"*"			{ return('*'); }
"/"			{ return('/'); }
"<"			{ return('<'); }
">"			{ return('>'); }

[ \t\v\n\f]		{ }
.			{ }

%%
//yyerror("Mystery character %c\n", *yytext);  }
//yylval->d = atof(yytext);
//printf("%s\n",yytext);