%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>
    #include "calc.h"
    int yylex(void);
    void yyerror (char const *);
%}

%define api.value.type union 
%token <double>  NUM     
%token <symrec*> VAR FUN /* Symbol table pointer: variable/function. */
%nterm <double>  exp

%precedence '='
%left '-' '+'
%left '*' '/'
%precedence NEG /* menos unario */
%right '^'      /* exponente */



%% 

input: %empty
| input line
;


line: '\n'
| exp '\n'   { printf ("%.10g\n", $1); }
| error '\n' { yyerrok;                }
;


exp: NUM
| VAR                { $$ = $1->value.var;              }
| VAR '=' exp        { $$ = $3; $1->value.var = $3;     }
| FUN '(' exp ')'    { $$ = $1->value.fun ($3);         }
| exp '+' exp        { $$ = $1 + $3;                    }
| exp '-' exp        { $$ = $1 - $3;                    }
| exp '*' exp        { $$ = $1 * $3;                    }
| exp '/' exp        { $$ = $1 / $3;                    }
| '-' exp  %prec NEG { $$ = -$2;                        }
| exp '^' exp        { $$ = pow ($1, $3);               }
| '(' exp ')'        { $$ = $2;                         }
;

%%
#include <ctype.h>
#include <stddef.h>

int main(){
    init_table();
    return yyparse();
}
int yylex (void)
{
  int c = getchar ();

  /* consume espacios blancos. */
  while (c == ' ' || c == '\t')
    c = getchar ();
  
  //fin
  if (c == EOF)
    return YYEOF;


  /* lee un número que regresa en NUM */
  if (c == '.' || isdigit (c))
    {
      ungetc (c, stdin);
      if (scanf ("%lf", &yylval.NUM) != 1)
        abort ();
      return NUM;
    }


  /* lee el nombre de una variable o función */
  if (isalpha (c))
    {
      static ptrdiff_t bufsize = 0;
      static char *symbuf = 0;

      ptrdiff_t i = 0;
      do {
          /* incrementa el buffer si se llena */
          if (bufsize <= i)
            {
              bufsize = 2 * bufsize + 40;
              symbuf = realloc (symbuf, (size_t) bufsize);
            }
          /* agrega caracter al buffer. */
          symbuf[i++] = (char) c;
          /* sigue leyendo */
          c = getchar ();
        }

      while (isalnum (c));

      ungetc (c, stdin);
      symbuf[i] = '\0';


      symrec *s = getsym (symbuf);
      if (!s) //si la variable no existe, agregar a la tabla de símbolos
          s = putsym (symbuf, VAR);
      yylval.VAR = s;
      return s->type;
    }

  /* otro tipo de caracter */
  return c;
}

/* Error. */
void yyerror (char const *s)
{
  fprintf (stderr, "%s\n", s);
}


