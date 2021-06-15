/* tipo función: apuntador a una función que tiene como parámetro (double), y valor de regreso double */
typedef double (func_t) (double);


/* tipo de dato de la lista ligada (tabla de símbolos). */
struct symrec{
    char *name;  /* nombre del símbolo */
    int type;    /* tipo de símbolo: VAR o FUN */
    union{
        double var;    /* valor de un VAR */
        func_t *fun;   /* valor de un FUN */
    } value;
  struct symrec *next;  /* apuntador a sigiente elemento de la lista */
};


typedef struct symrec symrec;

/* Tabla de símbolos: lista ligada de  'struct symrec'. */
extern symrec *sym_table;

symrec *putsym (char const *name, int sym_type);
symrec *getsym (char const *name);
void init_table(void);
