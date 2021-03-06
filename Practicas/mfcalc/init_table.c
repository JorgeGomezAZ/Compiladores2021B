#include "calc.h"
#include <math.h>
#include "mfcalc.tab.h"

struct init
{
  char const *name;
  func_t *fun;
};


struct init const funs[] =
{
  { "atan", atan },
  { "cos",  cos  },
  { "exp",  exp  },
  { "ln",   log  },
  { "sin",  sin  },
  { "sqrt", sqrt },
  { 0, 0 },
};


/* The symbol table: a chain of 'struct symrec'. */
symrec *sym_table;


/* Agrega funciones de funs[] a la tabla*/
void init_table(void)
{
  for (int i = 0; funs[i].name; i++)
    {
      symrec *ptr = putsym (funs[i].name, FUN);
      ptr->value.fun = funs[i].fun;
    }
}
