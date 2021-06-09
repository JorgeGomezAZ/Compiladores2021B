D			[0-9]
L			[a-zA-Z_]
E			[Ee][+-]?{D}+

%{
#include <stdio.h>
#include "proyecto.tab.h"

void count();
%}

%%

"char"			{ count(); return(CHAR); }
"const"			{ count(); return(CONST); }
"if"			{ count(); return(IF); }
"int"			{ count(); return(INT); }
"return"		{ count(); return(RETURN); }
"void"			{ count(); return(VOID); }
"while"			{ count(); return(WHILE); }
"=="			{ count(); return(EQ_OP); }

{L}({L}|{D})*		{ count(); return(IDENTIFIER); }

L?'(\\.|[^\\'])+'	{ count(); return(CONSTANT); }

{D}+{E}?		{ count(); return(CONSTANT); }

L?\"(\\.|[^\\"])*\"	{ count(); return(STRING_LITERAL); }

";"			{ count(); return(';'); }
("{")		{ count(); return('{'); }
("}")		{ count(); return('}'); }
","			{ count(); return(','); }
"="			{ count(); return('='); }
"("			{ count(); return('('); }
")"			{ count(); return(')'); }
("[")		{ count(); return('['); }
("]")		{ count(); return(']'); }
"."			{ count(); return('.'); }
"&"			{ count(); return('&'); }
"-"			{ count(); return('-'); }
"+"			{ count(); return('+'); }
"*"			{ count(); return('*'); }
"/"			{ count(); return('/'); }
"<"			{ count(); return('<'); }
">"			{ count(); return('>'); }

[ \t\v\n\f]		{ count(); }
.			{ yyerror("Mystery character %c\n", *yytext);  }

%%

int column = 0;

void count()
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n')
			column = 0;
		else if (yytext[i] == '\t')
			column += 8 - (column % 8);
		else
			column++;

	//printf("valid token");
}


