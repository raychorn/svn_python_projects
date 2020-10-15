/* luxsys.c - generated from mluxsys.c by onesrc
 * paths: lua-4.0/src/ lua-4.0/src/lib/ lua-4.0/include/ .
 * Wed Feb 21 21:31:06 PST 2001
 */

/* Include all of Lua and extension libs here, used for "onesrc" */

/* include: lua.h */
/*
** $Id: lua.h,v 1.79 2000/10/31 12:44:07 roberto Exp $
** Lua - An Extensible Extension Language
** TeCGraf: Grupo de Tecnologia em Computacao Grafica, PUC-Rio, Brazil
** e-mail: lua@tecgraf.puc-rio.br
** www: http://www.tecgraf.puc-rio.br/lua/
** See Copyright Notice at the end of this file
*/


#ifndef lua_h
#define lua_h


/* definition of `size_t' */
#include <stddef.h>


/* mark for all API functions */
#ifndef LUA_API
#define LUA_API		extern
#endif


#define LUA_VERSION	"Lua 4.0"
#define LUA_COPYRIGHT	"Copyright (C) 1994-2000 TeCGraf, PUC-Rio"
#define LUA_AUTHORS 	"W. Celes, R. Ierusalimschy & L. H. de Figueiredo"


/* name of global variable with error handler */
#define LUA_ERRORMESSAGE	"_ERRORMESSAGE"


/* pre-defined references */
#define LUA_NOREF	(-2)
#define LUA_REFNIL	(-1)
#define LUA_REFREGISTRY	0

/* pre-defined tags */
#define LUA_ANYTAG	(-1)
#define LUA_NOTAG	(-2)


/* option for multiple returns in lua_call */
#define LUA_MULTRET	(-1)


/* minimum stack available for a C function */
#define LUA_MINSTACK	20


/* error codes for lua_do* */
#define LUA_ERRRUN	1
#define LUA_ERRFILE	2
#define LUA_ERRSYNTAX	3
#define LUA_ERRMEM	4
#define LUA_ERRERR	5


typedef struct lua_State lua_State;

typedef int (*lua_CFunction) (lua_State *L);

/*
** types returned by `lua_type'
*/
#define LUA_TNONE	(-1)

#define LUA_TUSERDATA	0
#define LUA_TNIL	1
#define LUA_TNUMBER	2
#define LUA_TSTRING	3
#define LUA_TTABLE	4
#define LUA_TFUNCTION	5



/*
** state manipulation
*/
LUA_API lua_State *lua_open (int stacksize);
LUA_API void       lua_close (lua_State *L);


/*
** basic stack manipulation
*/
LUA_API int   lua_gettop (lua_State *L);
LUA_API void  lua_settop (lua_State *L, int index);
LUA_API void  lua_pushvalue (lua_State *L, int index);
LUA_API void  lua_remove (lua_State *L, int index);
LUA_API void  lua_insert (lua_State *L, int index);
LUA_API int   lua_stackspace (lua_State *L);


/*
** access functions (stack -> C)
*/

LUA_API int            lua_type (lua_State *L, int index);
LUA_API const char    *lua_typename (lua_State *L, int t);
LUA_API int            lua_isnumber (lua_State *L, int index);
LUA_API int            lua_isstring (lua_State *L, int index);
LUA_API int            lua_iscfunction (lua_State *L, int index);
LUA_API int            lua_tag (lua_State *L, int index);

LUA_API int            lua_equal (lua_State *L, int index1, int index2);
LUA_API int            lua_lessthan (lua_State *L, int index1, int index2);

LUA_API double         lua_tonumber (lua_State *L, int index);
LUA_API const char    *lua_tostring (lua_State *L, int index);
LUA_API size_t         lua_strlen (lua_State *L, int index);
LUA_API lua_CFunction  lua_tocfunction (lua_State *L, int index);
LUA_API void	      *lua_touserdata (lua_State *L, int index);
LUA_API const void    *lua_topointer (lua_State *L, int index);


/*
** push functions (C -> stack)
*/
LUA_API void  lua_pushnil (lua_State *L);
LUA_API void  lua_pushnumber (lua_State *L, double n);
LUA_API void  lua_pushlstring (lua_State *L, const char *s, size_t len);
LUA_API void  lua_pushstring (lua_State *L, const char *s);
LUA_API void  lua_pushcclosure (lua_State *L, lua_CFunction fn, int n);
LUA_API void  lua_pushusertag (lua_State *L, void *u, int tag);


/*
** get functions (Lua -> stack)
*/
LUA_API void  lua_getglobal (lua_State *L, const char *name);
LUA_API void  lua_gettable (lua_State *L, int index);
LUA_API void  lua_rawget (lua_State *L, int index);
LUA_API void  lua_rawgeti (lua_State *L, int index, int n);
LUA_API void  lua_getglobals (lua_State *L);
LUA_API void  lua_gettagmethod (lua_State *L, int tag, const char *event);
LUA_API int   lua_getref (lua_State *L, int ref);
LUA_API void  lua_newtable (lua_State *L);


/*
** set functions (stack -> Lua)
*/
LUA_API void  lua_setglobal (lua_State *L, const char *name);
LUA_API void  lua_settable (lua_State *L, int index);
LUA_API void  lua_rawset (lua_State *L, int index);
LUA_API void  lua_rawseti (lua_State *L, int index, int n);
LUA_API void  lua_setglobals (lua_State *L);
LUA_API void  lua_settagmethod (lua_State *L, int tag, const char *event);
LUA_API int   lua_ref (lua_State *L, int lock);


/*
** "do" functions (run Lua code)
*/
LUA_API int   lua_call (lua_State *L, int nargs, int nresults);
LUA_API void  lua_rawcall (lua_State *L, int nargs, int nresults);
LUA_API int   lua_dofile (lua_State *L, const char *filename);
LUA_API int   lua_dostring (lua_State *L, const char *str);
LUA_API int   lua_dobuffer (lua_State *L, const char *buff, size_t size, const char *name);

/*
** Garbage-collection functions
*/
LUA_API int   lua_getgcthreshold (lua_State *L);
LUA_API int   lua_getgccount (lua_State *L);
LUA_API void  lua_setgcthreshold (lua_State *L, int newthreshold);

/*
** miscellaneous functions
*/
LUA_API int   lua_newtag (lua_State *L);
LUA_API int   lua_copytagmethods (lua_State *L, int tagto, int tagfrom);
LUA_API void  lua_settag (lua_State *L, int tag);

LUA_API void  lua_error (lua_State *L, const char *s);

LUA_API void  lua_unref (lua_State *L, int ref);

LUA_API int   lua_next (lua_State *L, int index);
LUA_API int   lua_getn (lua_State *L, int index);

LUA_API void  lua_concat (lua_State *L, int n);

LUA_API void *lua_newuserdata (lua_State *L, size_t size);


/* 
** ===============================================================
** some useful macros
** ===============================================================
*/

#define lua_pop(L,n)		lua_settop(L, -(n)-1)

#define lua_register(L,n,f)	(lua_pushcfunction(L, f), lua_setglobal(L, n))
#define lua_pushuserdata(L,u)	lua_pushusertag(L, u, 0)
#define lua_pushcfunction(L,f)	lua_pushcclosure(L, f, 0)
#define lua_clonetag(L,t)	lua_copytagmethods(L, lua_newtag(L), (t))

#define lua_isfunction(L,n)	(lua_type(L,n) == LUA_TFUNCTION)
#define lua_istable(L,n)	(lua_type(L,n) == LUA_TTABLE)
#define lua_isuserdata(L,n)	(lua_type(L,n) == LUA_TUSERDATA)
#define lua_isnil(L,n)		(lua_type(L,n) == LUA_TNIL)
#define lua_isnull(L,n)		(lua_type(L,n) == LUA_TNONE)

#define lua_getregistry(L)	lua_getref(L, LUA_REFREGISTRY)

#endif



/******************************************************************************
* Copyright (C) 1994-2000 TeCGraf, PUC-Rio.  All rights reserved.
* 
* Permission is hereby granted, without written agreement and without license
* or royalty fees, to use, copy, modify, and distribute this software and its
* documentation for any purpose, including commercial applications, subject to
* the following conditions:
* 
*  - The above copyright notice and this permission notice shall appear in all
*    copies or substantial portions of this software.
* 
*  - The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software in a
*    product, an acknowledgment in the product documentation would be greatly
*    appreciated (but it is not required).
* 
*  - Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
*    
* The authors specifically disclaim any warranties, including, but not limited
* to, the implied warranties of merchantability and fitness for a particular
* purpose.  The software provided hereunder is on an "as is" basis, and the
* authors have no obligation to provide maintenance, support, updates,
* enhancements, or modifications.  In no event shall TeCGraf, PUC-Rio, or the
* authors be held liable to any party for direct, indirect, special,
* incidental, or consequential damages arising out of the use of this software
* and its documentation.
* 
* The Lua language and this implementation have been entirely designed and
* written by Waldemar Celes Filho, Roberto Ierusalimschy and
* Luiz Henrique de Figueiredo at TeCGraf, PUC-Rio.
*
* This implementation contains no third-party code.
******************************************************************************/

/* resumed: mluxsys.c */
/* include: luadebug.h */
/*
** $Id: luadebug.h,v 1.17 2000/10/30 12:38:50 roberto Exp $
** Debugging API
** See Copyright Notice in lua.h
*/


#ifndef luadebug_h
#define luadebug_h


/* skipped: lua.h - see mluxsys.c */

typedef struct lua_Debug lua_Debug;  /* activation record */
typedef struct lua_Localvar lua_Localvar;

typedef void (*lua_Hook) (lua_State *L, lua_Debug *ar);


LUA_API int lua_getstack (lua_State *L, int level, lua_Debug *ar);
LUA_API int lua_getinfo (lua_State *L, const char *what, lua_Debug *ar);
LUA_API const char *lua_getlocal (lua_State *L, const lua_Debug *ar, int n);
LUA_API const char *lua_setlocal (lua_State *L, const lua_Debug *ar, int n);

LUA_API lua_Hook lua_setcallhook (lua_State *L, lua_Hook func);
LUA_API lua_Hook lua_setlinehook (lua_State *L, lua_Hook func);


#define LUA_IDSIZE	60

struct lua_Debug {
  const char *event;     /* `call', `return' */
  int currentline;       /* (l) */
  const char *name;      /* (n) */
  const char *namewhat;  /* (n) `global', `tag method', `local', `field' */
  int nups;              /* (u) number of upvalues */
  int linedefined;       /* (S) */
  const char *what;      /* (S) `Lua' function, `C' function, Lua `main' */
  const char *source;    /* (S) */
  char short_src[LUA_IDSIZE]; /* (S) */
  /* private part */
  struct lua_TObject *_func;  /* active function */
};


#endif
/* resumed: mluxsys.c */
/* include: lualib.h */
/*
** $Id: lualib.h,v 1.14 2000/10/27 16:15:53 roberto Exp $
** Lua standard libraries
** See Copyright Notice in lua.h
*/


#ifndef lualib_h
#define lualib_h

/* skipped: lua.h - see mluxsys.c */


#ifndef LUALIB_API
#define LUALIB_API	extern
#endif


#define LUA_ALERT               "_ALERT"

LUALIB_API void lua_baselibopen (lua_State *L);
LUALIB_API void lua_iolibopen (lua_State *L);
LUALIB_API void lua_strlibopen (lua_State *L);
LUALIB_API void lua_mathlibopen (lua_State *L);
LUALIB_API void lua_dblibopen (lua_State *L);



/* Auxiliary functions (private) */

const char *luaI_classend (lua_State *L, const char *p);
int luaI_singlematch (int c, const char *p, const char *ep);

#endif
/* resumed: mluxsys.c */
/* include: lauxlib.h */
/*
** $Id: lauxlib.h,v 1.30 2000/10/30 12:38:50 roberto Exp $
** Auxiliary functions for building Lua libraries
** See Copyright Notice in lua.h
*/


#ifndef lauxlib_h
#define lauxlib_h


#include <stddef.h>
#include <stdio.h>

/* skipped: lua.h - see mluxsys.c */


#ifndef LUALIB_API
#define LUALIB_API	extern
#endif


struct luaL_reg {
  const char *name;
  lua_CFunction func;
};


LUALIB_API void luaL_openlib (lua_State *L, const struct luaL_reg *l, int n);
LUALIB_API void luaL_argerror (lua_State *L, int numarg, const char *extramsg);
LUALIB_API const char *luaL_check_lstr (lua_State *L, int numArg, size_t *len);
LUALIB_API const char *luaL_opt_lstr (lua_State *L, int numArg, const char *def, size_t *len);
LUALIB_API double luaL_check_number (lua_State *L, int numArg);
LUALIB_API double luaL_opt_number (lua_State *L, int numArg, double def);

LUALIB_API void luaL_checkstack (lua_State *L, int space, const char *msg);
LUALIB_API void luaL_checktype (lua_State *L, int narg, int t);
LUALIB_API void luaL_checkany (lua_State *L, int narg);

LUALIB_API void luaL_verror (lua_State *L, const char *fmt, ...);
LUALIB_API int luaL_findstring (const char *name, const char *const list[]);



/*
** ===============================================================
** some useful macros
** ===============================================================
*/

#define luaL_arg_check(L, cond,numarg,extramsg) if (!(cond)) \
                                               luaL_argerror(L, numarg,extramsg)
#define luaL_check_string(L,n)	(luaL_check_lstr(L, (n), NULL))
#define luaL_opt_string(L,n,d)	(luaL_opt_lstr(L, (n), (d), NULL))
#define luaL_check_int(L,n)	((int)luaL_check_number(L, n))
#define luaL_check_long(L,n)	((long)luaL_check_number(L, n))
#define luaL_opt_int(L,n,d)	((int)luaL_opt_number(L, n,d))
#define luaL_opt_long(L,n,d)	((long)luaL_opt_number(L, n,d))
#define luaL_openl(L,a)		luaL_openlib(L, a, (sizeof(a)/sizeof(a[0])))


/*
** {======================================================
** Generic Buffer manipulation
** =======================================================
*/


#ifndef LUAL_BUFFERSIZE
#define LUAL_BUFFERSIZE	  BUFSIZ
#endif


typedef struct luaL_Buffer {
  char *p;			/* current position in buffer */
  int level;
  lua_State *L;
  char buffer[LUAL_BUFFERSIZE];
} luaL_Buffer;

#define luaL_putchar(B,c) \
  ((void)((B)->p < &(B)->buffer[LUAL_BUFFERSIZE] || luaL_prepbuffer(B)), \
   (*(B)->p++ = (char)(c)))

#define luaL_addsize(B,n)	((B)->p += (n))

LUALIB_API void luaL_buffinit (lua_State *L, luaL_Buffer *B);
LUALIB_API char *luaL_prepbuffer (luaL_Buffer *B);
LUALIB_API void luaL_addlstring (luaL_Buffer *B, const char *s, size_t l);
LUALIB_API void luaL_addstring (luaL_Buffer *B, const char *s);
LUALIB_API void luaL_addvalue (luaL_Buffer *B);
LUALIB_API void luaL_pushresult (luaL_Buffer *B);


/* }====================================================== */


#endif


/* resumed: mluxsys.c */

/* include: lapi.c */
/*
** $Id: lapi.c,v 1.110 2000/10/30 12:50:09 roberto Exp $
** Lua API
** See Copyright Notice in lua.h
*/


#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* include: lapi.h */
/*
** $Id: lapi.h,v 1.20 2000/08/31 14:08:27 roberto Exp $
** Auxiliary functions from Lua API
** See Copyright Notice in lua.h
*/

#ifndef lapi_h
#define lapi_h


/* include: lobject.h */
/*
** $Id: lobject.h,v 1.82 2000/10/30 17:49:19 roberto Exp $
** Type definitions for Lua objects
** See Copyright Notice in lua.h
*/

#ifndef lobject_h
#define lobject_h


/* include: llimits.h */
/*
** $Id: llimits.h,v 1.19 2000/10/26 12:47:05 roberto Exp $
** Limits, basic types, and some other "installation-dependent" definitions
** See Copyright Notice in lua.h
*/

#ifndef llimits_h
#define llimits_h


#include <limits.h>
#include <stddef.h>



/*
** try to find number of bits in an integer
*/
#ifndef BITS_INT
/* avoid overflows in comparison */
#if INT_MAX-20 < 32760
#define	BITS_INT	16
#else
#if INT_MAX > 2147483640L
/* machine has at least 32 bits */
#define BITS_INT	32
#else
#error "you must define BITS_INT with number of bits in an integer"
#endif
#endif
#endif


/*
** Define the type `number' of Lua
** GREP LUA_NUMBER to change that
*/
#ifndef LUA_NUM_TYPE
#define LUA_NUM_TYPE double
#endif

typedef LUA_NUM_TYPE Number;

/* function to convert a Number to a string */
#define NUMBER_FMT	"%.16g"		/* LUA_NUMBER */
#define lua_number2str(s,n)	sprintf((s), NUMBER_FMT, (n))

/* function to convert a string to a Number */
#define lua_str2number(s,p)	strtod((s), (p))



typedef unsigned long lint32;  /* unsigned int with at least 32 bits */


#define MAX_SIZET	((size_t)(~(size_t)0)-2)


#define MAX_INT (INT_MAX-2)  /* maximum value of an int (-2 for safety) */

/*
** conversion of pointer to int (for hashing only)
** (the shift removes bits that are usually 0 because of alignment)
*/
#define IntPoint(p)  (((unsigned long)(p)) >> 3)



#define MINPOWER2       4       /* minimum size for "growing" vectors */



#ifndef DEFAULT_STACK_SIZE
#define DEFAULT_STACK_SIZE      1024
#endif



/* type to ensure maximum alignment */
union L_Umaxalign { double d; char *s; long l; };



/*
** type for virtual-machine instructions
** must be an unsigned with (at least) 4 bytes (see details in lopcodes.h)
** For a very small machine, you may change that to 2 bytes (and adjust
** the following limits accordingly)
*/
typedef unsigned long Instruction;


/*
** size and position of opcode arguments.
** For an instruction with 2 bytes, size is 16, and size_b can be 5
** (accordingly, size_u will be 10, and size_a will be 5)
*/
#define SIZE_INSTRUCTION        32
#define SIZE_B          9

#define SIZE_OP         6
#define SIZE_U          (SIZE_INSTRUCTION-SIZE_OP)
#define POS_U           SIZE_OP
#define POS_B           SIZE_OP
#define SIZE_A          (SIZE_INSTRUCTION-(SIZE_OP+SIZE_B))
#define POS_A           (SIZE_OP+SIZE_B)


/*
** limits for opcode arguments.
** we use (signed) int to manipulate most arguments,
** so they must fit in BITS_INT-1 bits (-1 for sign)
*/
#if SIZE_U < BITS_INT-1
#define MAXARG_U        ((1<<SIZE_U)-1)
#define MAXARG_S        (MAXARG_U>>1)		/* `S' is signed */
#else
#define MAXARG_U        MAX_INT
#define MAXARG_S        MAX_INT
#endif

#if SIZE_A < BITS_INT-1
#define MAXARG_A        ((1<<SIZE_A)-1)
#else
#define MAXARG_A        MAX_INT
#endif

#if SIZE_B < BITS_INT-1
#define MAXARG_B        ((1<<SIZE_B)-1)
#else
#define MAXARG_B        MAX_INT
#endif


/* maximum stack size in a function */
#ifndef MAXSTACK
#define MAXSTACK	250
#endif

#if MAXSTACK > MAXARG_B
#undef MAXSTACK
#define MAXSTACK	MAXARG_B
#endif


/* maximum number of local variables */
#ifndef MAXLOCALS
#define MAXLOCALS 200           /* arbitrary limit (<MAXSTACK) */
#endif
#if MAXLOCALS>=MAXSTACK
#undef MAXLOCALS
#define MAXLOCALS	(MAXSTACK-1)
#endif


/* maximum number of upvalues */
#ifndef MAXUPVALUES
#define MAXUPVALUES 32          /* arbitrary limit (<=MAXARG_B) */
#endif
#if MAXUPVALUES>MAXARG_B
#undef MAXUPVALUES
#define MAXUPVALUES	MAXARG_B
#endif


/* maximum number of variables in the left side of an assignment */
#ifndef MAXVARSLH
#define MAXVARSLH 100           /* arbitrary limit (<MULT_RET) */
#endif
#if MAXVARSLH>=MULT_RET
#undef MAXVARSLH
#define MAXVARSLH	(MULT_RET-1)
#endif


/* maximum number of parameters in a function */
#ifndef MAXPARAMS
#define MAXPARAMS 100           /* arbitrary limit (<MAXLOCALS) */
#endif
#if MAXPARAMS>=MAXLOCALS
#undef MAXPARAMS
#define MAXPARAMS	(MAXLOCALS-1)
#endif


/* number of list items to accumulate before a SETLIST instruction */
#define LFIELDS_PER_FLUSH	64
#if LFIELDS_PER_FLUSH>(MAXSTACK/4)
#undef LFIELDS_PER_FLUSH
#define LFIELDS_PER_FLUSH	(MAXSTACK/4)
#endif

/* number of record items to accumulate before a SETMAP instruction */
/* (each item counts 2 elements on the stack: an index and a value) */
#define RFIELDS_PER_FLUSH	(LFIELDS_PER_FLUSH/2)


/* maximum lookback to find a real constant (for code generation) */
#ifndef LOOKBACKNUMS
#define LOOKBACKNUMS    20      /* arbitrary constant */
#endif


#endif
/* resumed: lua-4.0/src/lobject.h */
/* skipped: lua.h - see mluxsys.c */


#ifdef LUA_DEBUG
#undef NDEBUG
#include <assert.h>
#define LUA_INTERNALERROR(s)	assert(((void)s,0))
#define LUA_ASSERT(c,s)		assert(((void)s,(c)))
#else
#define LUA_INTERNALERROR(s)	/* empty */
#define LUA_ASSERT(c,s)		/* empty */
#endif


#ifdef LUA_DEBUG
/* to avoid warnings, and make sure value is really unused */
#define UNUSED(x)	(x=0, (void)(x))
#else
#define UNUSED(x)	((void)(x))	/* to avoid warnings */
#endif


/* mark for closures active in the stack */
#define LUA_TMARK	6


/* tags for values visible from Lua == first user-created tag */
#define NUM_TAGS	6


/* check whether `t' is a mark */
#define is_T_MARK(t)	((t) == LUA_TMARK)


typedef union {
  struct TString *ts;	/* LUA_TSTRING, LUA_TUSERDATA */
  struct Closure *cl;	/* LUA_TFUNCTION */
  struct Hash *a;	/* LUA_TTABLE */
  struct CallInfo *i;	/* LUA_TLMARK */
  Number n;		/* LUA_TNUMBER */
} Value;


/* Macros to access values */
#define ttype(o)        ((o)->ttype)
#define nvalue(o)       ((o)->value.n)
#define tsvalue(o)      ((o)->value.ts)
#define clvalue(o)      ((o)->value.cl)
#define hvalue(o)       ((o)->value.a)
#define infovalue(o)	((o)->value.i)
#define svalue(o)       (tsvalue(o)->str)


typedef struct lua_TObject {
  int ttype;
  Value value;
} TObject;


/*
** String headers for string table
*/

/*
** most `malloc' libraries allocate memory in blocks of 8 bytes. TSPACK
** tries to make sizeof(TString) a multiple of this granularity, to reduce
** waste of space.
*/
#define TSPACK	((int)sizeof(int))

typedef struct TString {
  union {
    struct {  /* for strings */
      unsigned long hash;
      int constindex;  /* hint to reuse constants */
    } s;
    struct {  /* for userdata */
      int tag;
      void *value;
    } d;
  } u;
  size_t len;
  struct TString *nexthash;  /* chain for hash table */
  int marked;
  char str[TSPACK];   /* variable length string!! must be the last field! */
} TString;


/*
** Function Prototypes
*/
typedef struct Proto {
  Number *knum;  /* Number numbers used by the function */
  int nknum;  /* size of `knum' */
  struct TString **kstr;  /* strings used by the function */
  int nkstr;  /* size of `kstr' */
  struct Proto **kproto;  /* functions defined inside the function */
  int nkproto;  /* size of `kproto' */
  Instruction *code;
  int ncode;  /* size of `code'; when 0 means an incomplete `Proto' */
  short numparams;
  short is_vararg;
  short maxstacksize;
  short marked;
  struct Proto *next;
  /* debug information */
  int *lineinfo;  /* map from opcodes to source lines */
  int nlineinfo;  /* size of `lineinfo' */
  int nlocvars;
  struct LocVar *locvars;  /* information about local variables */
  int lineDefined;
  TString  *source;
} Proto;


typedef struct LocVar {
  TString *varname;
  int startpc;  /* first point where variable is active */
  int endpc;    /* first point where variable is dead */
} LocVar;


/*
** Closures
*/
typedef struct Closure {
  union {
    lua_CFunction c;  /* C functions */
    struct Proto *l;  /* Lua functions */
  } f;
  struct Closure *next;
  struct Closure *mark;  /* marked closures (point to itself when not marked) */
  short isC;  /* 0 for Lua functions, 1 for C functions */
  short nupvalues;
  TObject upvalue[1];
} Closure;


#define iscfunction(o)	(ttype(o) == LUA_TFUNCTION && clvalue(o)->isC)


typedef struct Node {
  TObject key;
  TObject val;
  struct Node *next;  /* for chaining */
} Node;

typedef struct Hash {
  Node *node;
  int htag;
  int size;
  Node *firstfree;  /* this position is free; all positions after it are full */
  struct Hash *next;
  struct Hash *mark;  /* marked tables (point to itself when not marked) */
} Hash;


/* unmarked tables and closures are represented by pointing `mark' to
** themselves
*/
#define ismarked(x)	((x)->mark != (x))


/*
** informations about a call (for debugging)
*/
typedef struct CallInfo {
  struct Closure *func;  /* function being called */
  const Instruction **pc;  /* current pc of called function */
  int lastpc;  /* last pc traced */
  int line;  /* current line */
  int refi;  /* current index in `lineinfo' */
} CallInfo;


extern const TObject luaO_nilobject;
extern const char *const luaO_typenames[];


#define luaO_typename(o)	(luaO_typenames[ttype(o)])


lint32 luaO_power2 (lint32 n);
char *luaO_openspace (lua_State *L, size_t n);

int luaO_equalObj (const TObject *t1, const TObject *t2);
int luaO_str2d (const char *s, Number *result);

void luaO_verror (lua_State *L, const char *fmt, ...);
void luaO_chunkid (char *out, const char *source, int len);


#endif
/* resumed: lua-4.0/src/lapi.h */


TObject *luaA_index (lua_State *L, int index);
void luaA_pushobject (lua_State *L, const TObject *o);

#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: ldo.h */
/*
** $Id: ldo.h,v 1.28 2000/10/06 12:45:25 roberto Exp $
** Stack and Call structure of Lua
** See Copyright Notice in lua.h
*/

#ifndef ldo_h
#define ldo_h


/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* include: lstate.h */
/*
** $Id: lstate.h,v 1.41 2000/10/05 13:00:17 roberto Exp $
** Global State
** See Copyright Notice in lua.h
*/

#ifndef lstate_h
#define lstate_h

/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lua.h - see mluxsys.c */
/* skipped: luadebug.h - see mluxsys.c */



typedef TObject *StkId;  /* index to stack elements */


/*
** marks for Reference array
*/
#define NONEXT          -1      /* to end the free list */
#define HOLD            -2
#define COLLECTED       -3
#define LOCK            -4


struct Ref {
  TObject o;
  int st;  /* can be LOCK, HOLD, COLLECTED, or next (for free list) */
};


struct lua_longjmp;  /* defined in ldo.c */
struct TM;  /* defined in ltm.h */


typedef struct stringtable {
  int size;
  lint32 nuse;  /* number of elements */
  TString **hash;
} stringtable;



struct lua_State {
  /* thread-specific state */
  StkId top;  /* first free slot in the stack */
  StkId stack;  /* stack base */
  StkId stack_last;  /* last free slot in the stack */
  int stacksize;
  StkId Cbase;  /* base for current C function */
  struct lua_longjmp *errorJmp;  /* current error recover point */
  char *Mbuffer;  /* global buffer */
  size_t Mbuffsize;  /* size of Mbuffer */
  /* global state */
  Proto *rootproto;  /* list of all prototypes */
  Closure *rootcl;  /* list of all closures */
  Hash *roottable;  /* list of all tables */
  stringtable strt;  /* hash table for strings */
  stringtable udt;   /* hash table for udata */
  Hash *gt;  /* table for globals */
  struct TM *TMtable;  /* table for tag methods */
  int last_tag;  /* last used tag in TMtable */
  struct Ref *refArray;  /* locked objects */
  int refSize;  /* size of refArray */
  int refFree;  /* list of free positions in refArray */
  unsigned long GCthreshold;
  unsigned long nblocks;  /* number of `bytes' currently allocated */
  lua_Hook callhook;
  lua_Hook linehook;
  int allowhooks;
};


#endif

/* resumed: lua-4.0/src/ldo.h */


/*
** macro to increment stack top.
** There must be always an empty slot at the L->stack.top
*/
#define incr_top {if (L->top == L->stack_last) luaD_checkstack(L, 1); L->top++;}


void luaD_init (lua_State *L, int stacksize);
void luaD_adjusttop (lua_State *L, StkId base, int extra);
void luaD_lineHook (lua_State *L, StkId func, int line, lua_Hook linehook);
void luaD_call (lua_State *L, StkId func, int nResults);
void luaD_callTM (lua_State *L, Closure *f, int nParams, int nResults);
void luaD_checkstack (lua_State *L, int n);

void luaD_breakrun (lua_State *L, int errcode);
int luaD_runprotected (lua_State *L, void (*f)(lua_State *, void *), void *ud);


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: lfunc.h */
/*
** $Id: lfunc.h,v 1.13 2000/09/29 12:42:13 roberto Exp $
** Auxiliary functions to manipulate prototypes and closures
** See Copyright Notice in lua.h
*/

#ifndef lfunc_h
#define lfunc_h


/* skipped: lobject.h - see lua-4.0/src/lapi.h */



Proto *luaF_newproto (lua_State *L);
void luaF_protook (lua_State *L, Proto *f, int pc);
Closure *luaF_newclosure (lua_State *L, int nelems);
void luaF_freeproto (lua_State *L, Proto *f);
void luaF_freeclosure (lua_State *L, Closure *c);

const char *luaF_getlocalname (const Proto *func, int local_number, int pc);


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: lgc.h */
/*
** $Id: lgc.h,v 1.8 2000/10/02 14:47:43 roberto Exp $
** Garbage Collector
** See Copyright Notice in lua.h
*/

#ifndef lgc_h
#define lgc_h


/* skipped: lobject.h - see lua-4.0/src/lapi.h */


void luaC_collect (lua_State *L, int all);
void luaC_checkGC (lua_State *L);


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: lmem.h */
/*
** $Id: lmem.h,v 1.16 2000/10/30 16:29:59 roberto Exp $
** Interface to Memory Manager
** See Copyright Notice in lua.h
*/

#ifndef lmem_h
#define lmem_h


#include <stddef.h>

/* skipped: llimits.h - see lua-4.0/src/lobject.h */
/* skipped: lua.h - see mluxsys.c */

void *luaM_realloc (lua_State *L, void *oldblock, lint32 size);
void *luaM_growaux (lua_State *L, void *block, size_t nelems,
                    int inc, size_t size, const char *errormsg,
                    size_t limit);

#define luaM_free(L, b)		luaM_realloc(L, (b), 0)
#define luaM_malloc(L, t)	luaM_realloc(L, NULL, (t))
#define luaM_new(L, t)          ((t *)luaM_malloc(L, sizeof(t)))
#define luaM_newvector(L, n,t)  ((t *)luaM_malloc(L, (n)*(lint32)sizeof(t)))

#define luaM_growvector(L, v,nelems,inc,t,e,l) \
          ((v)=(t *)luaM_growaux(L, v,nelems,inc,sizeof(t),e,l))

#define luaM_reallocvector(L, v,n,t) \
	((v)=(t *)luaM_realloc(L, v,(n)*(lint32)sizeof(t)))


#ifdef LUA_DEBUG
extern unsigned long memdebug_numblocks;
extern unsigned long memdebug_total;
extern unsigned long memdebug_maxmem;
extern unsigned long memdebug_memlimit;
#endif


#endif

/* resumed: lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* include: lstring.h */
/*
** $Id: lstring.h,v 1.24 2000/10/30 17:49:19 roberto Exp $
** String table (keep all strings handled by Lua)
** See Copyright Notice in lua.h
*/

#ifndef lstring_h
#define lstring_h


/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */


/*
** any TString with mark>=FIXMARK is never collected.
** Marks>=RESERVEDMARK are used to identify reserved words.
*/
#define FIXMARK		2
#define RESERVEDMARK	3


#define sizestring(l)	((long)sizeof(TString) + \
                         ((long)(l+1)-TSPACK)*(long)sizeof(char))


void luaS_init (lua_State *L);
void luaS_resize (lua_State *L, stringtable *tb, int newsize);
TString *luaS_newudata (lua_State *L, size_t s, void *udata);
TString *luaS_createudata (lua_State *L, void *udata, int tag);
void luaS_freeall (lua_State *L);
TString *luaS_newlstr (lua_State *L, const char *str, size_t l);
TString *luaS_new (lua_State *L, const char *str);
TString *luaS_newfixed (lua_State *L, const char *str);


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: ltable.h */
/*
** $Id: ltable.h,v 1.24 2000/08/31 14:08:27 roberto Exp $
** Lua tables (hash)
** See Copyright Notice in lua.h
*/

#ifndef ltable_h
#define ltable_h

/* skipped: lobject.h - see lua-4.0/src/lapi.h */


#define node(t,i)	(&(t)->node[i])
#define key(n)		(&(n)->key)
#define val(n)		(&(n)->val)

Hash *luaH_new (lua_State *L, int nhash);
void luaH_free (lua_State *L, Hash *t);
const TObject *luaH_get (lua_State *L, const Hash *t, const TObject *key);
const TObject *luaH_getnum (const Hash *t, Number key);
const TObject *luaH_getstr (const Hash *t, TString *key);
void luaH_remove (Hash *t, TObject *key);
TObject *luaH_set (lua_State *L, Hash *t, const TObject *key);
Node * luaH_next (lua_State *L, const Hash *t, const TObject *r);
TObject *luaH_setint (lua_State *L, Hash *t, int key);
void luaH_setstrnum (lua_State *L, Hash *t, TString *key, Number val);
unsigned long luaH_hash (lua_State *L, const TObject *key);
const TObject *luaH_getglobal (lua_State *L, const char *name);

/* exported only for debugging */
Node *luaH_mainposition (const Hash *t, const TObject *key);


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: ltm.h */
/*
** $Id: ltm.h,v 1.18 2000/10/05 13:00:17 roberto Exp $
** Tag methods
** See Copyright Notice in lua.h
*/

#ifndef ltm_h
#define ltm_h


/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */

/*
* WARNING: if you change the order of this enumeration,
* grep "ORDER TM"
*/
typedef enum {
  TM_GETTABLE = 0,
  TM_SETTABLE,
  TM_INDEX,
  TM_GETGLOBAL,
  TM_SETGLOBAL,
  TM_ADD,
  TM_SUB,
  TM_MUL,
  TM_DIV,
  TM_POW,
  TM_UNM,
  TM_LT,
  TM_CONCAT,
  TM_GC,
  TM_FUNCTION,
  TM_N		/* number of elements in the enum */
} TMS;


struct TM {
  Closure *method[TM_N];
  TString *collected;  /* list of garbage-collected udata with this tag */
};


#define luaT_gettm(L,tag,event) (L->TMtable[tag].method[event])
#define luaT_gettmbyObj(L,o,e)  (luaT_gettm((L),luaT_tag(o),(e)))


#define validtag(t) (NUM_TAGS <= (t) && (t) <= L->last_tag)

extern const char *const luaT_eventname[];


void luaT_init (lua_State *L);
void luaT_realtag (lua_State *L, int tag);
int luaT_tag (const TObject *o);
int luaT_validevent (int t, int e);  /* used by compatibility module */


#endif
/* resumed: lua-4.0/src/lapi.c */
/* include: lvm.h */
/*
** $Id: lvm.h,v 1.27 2000/10/05 12:14:08 roberto Exp $
** Lua virtual machine
** See Copyright Notice in lua.h
*/

#ifndef lvm_h
#define lvm_h


/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */


#define tonumber(o)   ((ttype(o) != LUA_TNUMBER) && (luaV_tonumber(o) != 0))
#define tostring(L,o) ((ttype(o) != LUA_TSTRING) && (luaV_tostring(L, o) != 0))


int luaV_tonumber (TObject *obj);
int luaV_tostring (lua_State *L, TObject *obj);
const TObject *luaV_gettable (lua_State *L, StkId t);
void luaV_settable (lua_State *L, StkId t, StkId key);
const TObject *luaV_getglobal (lua_State *L, TString *s);
void luaV_setglobal (lua_State *L, TString *s);
StkId luaV_execute (lua_State *L, const Closure *cl, StkId base);
void luaV_Cclosure (lua_State *L, lua_CFunction c, int nelems);
void luaV_Lclosure (lua_State *L, Proto *l, int nelems);
int luaV_lessthan (lua_State *L, const TObject *l, const TObject *r, StkId top);
void luaV_strconc (lua_State *L, int total, StkId top);

#endif
/* resumed: lua-4.0/src/lapi.c */


const char lua_ident[] = "$Lua: " LUA_VERSION " " LUA_COPYRIGHT " $\n"
                               "$Authors: " LUA_AUTHORS " $";



#define Index(L,i)	((i) >= 0 ? (L->Cbase+((i)-1)) : (L->top+(i)))

#define api_incr_top(L)	incr_top




TObject *luaA_index (lua_State *L, int index) {
  return Index(L, index);
}


static TObject *luaA_indexAcceptable (lua_State *L, int index) {
  if (index >= 0) {
    TObject *o = L->Cbase+(index-1);
    if (o >= L->top) return NULL;
    else return o;
  }
  else return L->top+index;
}


void luaA_pushobject (lua_State *L, const TObject *o) {
  *L->top = *o;
  incr_top;
}

LUA_API int lua_stackspace (lua_State *L) {
  return (L->stack_last - L->top);
}



/*
** basic stack manipulation
*/


LUA_API int lua_gettop (lua_State *L) {
  return (L->top - L->Cbase);
}


LUA_API void lua_settop (lua_State *L, int index) {
  if (index >= 0)
    luaD_adjusttop(L, L->Cbase, index);
  else
    L->top = L->top+index+1;  /* index is negative */
}


LUA_API void lua_remove (lua_State *L, int index) {
  StkId p = luaA_index(L, index);
  while (++p < L->top) *(p-1) = *p;
  L->top--;
}


LUA_API void lua_insert (lua_State *L, int index) {
  StkId p = luaA_index(L, index);
  StkId q;
  for (q = L->top; q>p; q--)
    *q = *(q-1);
  *p = *L->top;
}


LUA_API void lua_pushvalue (lua_State *L, int index) {
  *L->top = *luaA_index(L, index);
  api_incr_top(L);
}



/*
** access functions (stack -> C)
*/


LUA_API int lua_type (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL) ? LUA_TNONE : ttype(o);
}

LUA_API const char *lua_typename (lua_State *L, int t) {
  UNUSED(L);
  return (t == LUA_TNONE) ? "no value" : luaO_typenames[t];
}


LUA_API int lua_iscfunction (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL) ? 0 : iscfunction(o);
}

LUA_API int lua_isnumber (lua_State *L, int index) {
  TObject *o = luaA_indexAcceptable(L, index);
  return (o == NULL) ? 0 : (tonumber(o) == 0);
}

LUA_API int lua_isstring (lua_State *L, int index) {
  int t = lua_type(L, index);
  return (t == LUA_TSTRING || t == LUA_TNUMBER);
}


LUA_API int lua_tag (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL) ? LUA_NOTAG : luaT_tag(o);
}

LUA_API int lua_equal (lua_State *L, int index1, int index2) {
  StkId o1 = luaA_indexAcceptable(L, index1);
  StkId o2 = luaA_indexAcceptable(L, index2);
  if (o1 == NULL || o2 == NULL) return 0;  /* index out-of-range */
  else return luaO_equalObj(o1, o2);
}

LUA_API int lua_lessthan (lua_State *L, int index1, int index2) {
  StkId o1 = luaA_indexAcceptable(L, index1);
  StkId o2 = luaA_indexAcceptable(L, index2);
  if (o1 == NULL || o2 == NULL) return 0;  /* index out-of-range */
  else return luaV_lessthan(L, o1, o2, L->top);
}



LUA_API double lua_tonumber (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL || tonumber(o)) ? 0 : nvalue(o);
}

LUA_API const char *lua_tostring (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL || tostring(L, o)) ? NULL : svalue(o);
}

LUA_API size_t lua_strlen (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL || tostring(L, o)) ? 0 : tsvalue(o)->len;
}

LUA_API lua_CFunction lua_tocfunction (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL || !iscfunction(o)) ? NULL : clvalue(o)->f.c;
}

LUA_API void *lua_touserdata (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  return (o == NULL || ttype(o) != LUA_TUSERDATA) ? NULL :
                                                    tsvalue(o)->u.d.value;
}

LUA_API const void *lua_topointer (lua_State *L, int index) {
  StkId o = luaA_indexAcceptable(L, index);
  if (o == NULL) return NULL;
  switch (ttype(o)) {
    case LUA_TTABLE: 
      return hvalue(o);
    case LUA_TFUNCTION:
      return clvalue(o);
    default: return NULL;
  }
}



/*
** push functions (C -> stack)
*/


LUA_API void lua_pushnil (lua_State *L) {
  ttype(L->top) = LUA_TNIL;
  api_incr_top(L);
}


LUA_API void lua_pushnumber (lua_State *L, double n) {
  nvalue(L->top) = n;
  ttype(L->top) = LUA_TNUMBER;
  api_incr_top(L);
}


LUA_API void lua_pushlstring (lua_State *L, const char *s, size_t len) {
  tsvalue(L->top) = luaS_newlstr(L, s, len);
  ttype(L->top) = LUA_TSTRING;
  api_incr_top(L);
}


LUA_API void lua_pushstring (lua_State *L, const char *s) {
  if (s == NULL)
    lua_pushnil(L);
  else
    lua_pushlstring(L, s, strlen(s));
}


LUA_API void lua_pushcclosure (lua_State *L, lua_CFunction fn, int n) {
  luaV_Cclosure(L, fn, n);
}


LUA_API void lua_pushusertag (lua_State *L, void *u, int tag) {
  /* ORDER LUA_T */
  if (!(tag == LUA_ANYTAG || tag == LUA_TUSERDATA || validtag(tag)))
    luaO_verror(L, "invalid tag for a userdata (%d)", tag);
  tsvalue(L->top) = luaS_createudata(L, u, tag);
  ttype(L->top) = LUA_TUSERDATA;
  api_incr_top(L);
}



/*
** get functions (Lua -> stack)
*/


LUA_API void lua_getglobal (lua_State *L, const char *name) {
  StkId top = L->top;
  *top = *luaV_getglobal(L, luaS_new(L, name));
  L->top = top;
  api_incr_top(L);
}


LUA_API void lua_gettable (lua_State *L, int index) {
  StkId t = Index(L, index);
  StkId top = L->top;
  *(top-1) = *luaV_gettable(L, t);
  L->top = top;  /* tag method may change top */
}


LUA_API void lua_rawget (lua_State *L, int index) {
  StkId t = Index(L, index);
  LUA_ASSERT(ttype(t) == LUA_TTABLE, "table expected");
  *(L->top - 1) = *luaH_get(L, hvalue(t), L->top - 1);
}


LUA_API void lua_rawgeti (lua_State *L, int index, int n) {
  StkId o = Index(L, index);
  LUA_ASSERT(ttype(o) == LUA_TTABLE, "table expected");
  *L->top = *luaH_getnum(hvalue(o), n);
  api_incr_top(L);
}


LUA_API void lua_getglobals (lua_State *L) {
  hvalue(L->top) = L->gt;
  ttype(L->top) = LUA_TTABLE;
  api_incr_top(L);
}


LUA_API int lua_getref (lua_State *L, int ref) {
  if (ref == LUA_REFNIL)
    ttype(L->top) = LUA_TNIL;
  else if (0 <= ref && ref < L->refSize &&
          (L->refArray[ref].st == LOCK || L->refArray[ref].st == HOLD))
    *L->top = L->refArray[ref].o;
  else
    return 0;
  api_incr_top(L);
  return 1;
}


LUA_API void lua_newtable (lua_State *L) {
  hvalue(L->top) = luaH_new(L, 0);
  ttype(L->top) = LUA_TTABLE;
  api_incr_top(L);
}



/*
** set functions (stack -> Lua)
*/


LUA_API void lua_setglobal (lua_State *L, const char *name) {
  StkId top = L->top;
  luaV_setglobal(L, luaS_new(L, name));
  L->top = top-1;  /* remove element from the top */
}


LUA_API void lua_settable (lua_State *L, int index) {
  StkId t = Index(L, index);
  StkId top = L->top;
  luaV_settable(L, t, top-2);
  L->top = top-2;  /* pop index and value */
}


LUA_API void lua_rawset (lua_State *L, int index) {
  StkId t = Index(L, index);
  LUA_ASSERT(ttype(t) == LUA_TTABLE, "table expected");
  *luaH_set(L, hvalue(t), L->top-2) = *(L->top-1);
  L->top -= 2;
}


LUA_API void lua_rawseti (lua_State *L, int index, int n) {
  StkId o = Index(L, index);
  LUA_ASSERT(ttype(o) == LUA_TTABLE, "table expected");
  *luaH_setint(L, hvalue(o), n) = *(L->top-1);
  L->top--;
}


LUA_API void lua_setglobals (lua_State *L) {
  StkId newtable = --L->top;
  LUA_ASSERT(ttype(newtable) == LUA_TTABLE, "table expected");
  L->gt = hvalue(newtable);
}


LUA_API int lua_ref (lua_State *L,  int lock) {
  int ref;
  if (ttype(L->top-1) == LUA_TNIL)
    ref = LUA_REFNIL;
  else {
    if (L->refFree != NONEXT) {  /* is there a free place? */
      ref = L->refFree;
      L->refFree = L->refArray[ref].st;
    }
    else {  /* no more free places */
      luaM_growvector(L, L->refArray, L->refSize, 1, struct Ref,
                      "reference table overflow", MAX_INT);
      L->nblocks += sizeof(struct Ref);
      ref = L->refSize++;
    }
    L->refArray[ref].o = *(L->top-1);
    L->refArray[ref].st = lock ? LOCK : HOLD;
  }
  L->top--;
  return ref;
}


/*
** "do" functions (run Lua code)
** (most of them are in ldo.c)
*/

LUA_API void lua_rawcall (lua_State *L, int nargs, int nresults) {
  luaD_call(L, L->top-(nargs+1), nresults);
}


/*
** Garbage-collection functions
*/

/* GC values are expressed in Kbytes: #bytes/2^10 */
#define GCscale(x)		((int)((x)>>10))
#define GCunscale(x)		((unsigned long)(x)<<10)

LUA_API int lua_getgcthreshold (lua_State *L) {
  return GCscale(L->GCthreshold);
}

LUA_API int lua_getgccount (lua_State *L) {
  return GCscale(L->nblocks);
}

LUA_API void lua_setgcthreshold (lua_State *L, int newthreshold) {
  if (newthreshold > GCscale(ULONG_MAX))
    L->GCthreshold = ULONG_MAX;
  else
    L->GCthreshold = GCunscale(newthreshold);
  luaC_checkGC(L);
}


/*
** miscellaneous functions
*/

LUA_API void lua_settag (lua_State *L, int tag) {
  luaT_realtag(L, tag);
  switch (ttype(L->top-1)) {
    case LUA_TTABLE:
      hvalue(L->top-1)->htag = tag;
      break;
    case LUA_TUSERDATA:
      tsvalue(L->top-1)->u.d.tag = tag;
      break;
    default:
      luaO_verror(L, "cannot change the tag of a %.20s",
                  luaO_typename(L->top-1));
  }
}


LUA_API void lua_unref (lua_State *L, int ref) {
  if (ref >= 0) {
    LUA_ASSERT(ref < L->refSize && L->refArray[ref].st < 0, "invalid ref");
    L->refArray[ref].st = L->refFree;
    L->refFree = ref;
  }
}


LUA_API int lua_next (lua_State *L, int index) {
  StkId t = luaA_index(L, index);
  Node *n;
  LUA_ASSERT(ttype(t) == LUA_TTABLE, "table expected");
  n = luaH_next(L, hvalue(t), luaA_index(L, -1));
  if (n) {
    *(L->top-1) = *key(n);
    *L->top = *val(n);
    api_incr_top(L);
    return 1;
  }
  else {  /* no more elements */
    L->top -= 1;  /* remove key */
    return 0;
  }
}


LUA_API int lua_getn (lua_State *L, int index) {
  Hash *h = hvalue(luaA_index(L, index));
  const TObject *value = luaH_getstr(h, luaS_new(L, "n"));  /* value = h.n */
  if (ttype(value) == LUA_TNUMBER)
    return (int)nvalue(value);
  else {
    Number max = 0;
    int i = h->size;
    Node *n = h->node;
    while (i--) {
      if (ttype(key(n)) == LUA_TNUMBER &&
          ttype(val(n)) != LUA_TNIL &&
          nvalue(key(n)) > max)
        max = nvalue(key(n));
      n++;
    }
    return (int)max;
  }
}


LUA_API void lua_concat (lua_State *L, int n) {
  StkId top = L->top;
  luaV_strconc(L, n, top);
  L->top = top-(n-1);
  luaC_checkGC(L);
}


LUA_API void *lua_newuserdata (lua_State *L, size_t size) {
  TString *ts = luaS_newudata(L, size, NULL);
  tsvalue(L->top) = ts;
  ttype(L->top) = LUA_TUSERDATA;
  api_incr_top(L);
  return ts->u.d.value;
}

/* resumed: mluxsys.c */
/* include: lcode.c */
/*
** $Id: lcode.c,v 1.51 2000/09/29 12:42:13 roberto Exp $
** Code generator for Lua
** See Copyright Notice in lua.h
*/


#include "stdlib.h"

/* skipped: lua.h - see mluxsys.c */

/* include: lcode.h */
/*
** $Id: lcode.h,v 1.16 2000/08/09 14:49:13 roberto Exp $
** Code generator for Lua
** See Copyright Notice in lua.h
*/

#ifndef lcode_h
#define lcode_h

/* include: llex.h */
/*
** $Id: llex.h,v 1.31 2000/09/27 17:41:58 roberto Exp $
** Lexical Analyzer
** See Copyright Notice in lua.h
*/

#ifndef llex_h
#define llex_h

/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* include: lzio.h */
/*
** $Id: lzio.h,v 1.7 2000/10/20 16:36:32 roberto Exp $
** Buffered streams
** See Copyright Notice in lua.h
*/


#ifndef lzio_h
#define lzio_h

#include <stdio.h>



/* For Lua only */
#define zFopen	luaZ_Fopen
#define zsopen	luaZ_sopen
#define zmopen	luaZ_mopen
#define zread	luaZ_read

#define EOZ	(-1)			/* end of stream */

typedef struct zio ZIO;

ZIO* zFopen (ZIO* z, FILE* f, const char *name);	/* open FILEs */
ZIO* zsopen (ZIO* z, const char* s, const char *name);	/* string */
ZIO* zmopen (ZIO* z, const char* b, size_t size, const char *name); /* memory */

size_t zread (ZIO* z, void* b, size_t n);	/* read next n bytes */

#define zgetc(z)	(((z)->n--)>0 ? ((int)*(z)->p++): (z)->filbuf(z))
#define zungetc(z)	(++(z)->n,--(z)->p)
#define zname(z)	((z)->name)



/* --------- Private Part ------------------ */

#ifndef ZBSIZE
#define ZBSIZE	256			/* buffer size */
#endif

struct zio {
  size_t n;				/* bytes still unread */
  const unsigned char* p;		/* current position in buffer */
  int (*filbuf)(ZIO* z);
  void* u;				/* additional data */
  const char *name;
  unsigned char buffer[ZBSIZE];		/* buffer */
};


#endif
/* resumed: lua-4.0/src/llex.h */


#define FIRST_RESERVED	257

/* maximum length of a reserved word (+1 for final 0) */
#define TOKEN_LEN	15


/*
* WARNING: if you change the order of this enumeration,
* grep "ORDER RESERVED"
*/
enum RESERVED {
  /* terminal symbols denoted by reserved words */
  TK_AND = FIRST_RESERVED, TK_BREAK,
  TK_DO, TK_ELSE, TK_ELSEIF, TK_END, TK_FOR, TK_FUNCTION, TK_IF, TK_LOCAL,
  TK_NIL, TK_NOT, TK_OR, TK_REPEAT, TK_RETURN, TK_THEN, TK_UNTIL, TK_WHILE,
  /* other terminal symbols */
  TK_NAME, TK_CONCAT, TK_DOTS, TK_EQ, TK_GE, TK_LE, TK_NE, TK_NUMBER,
  TK_STRING, TK_EOS
};

/* number of reserved words */
#define NUM_RESERVED	((int)(TK_WHILE-FIRST_RESERVED+1))


typedef union {
  Number r;
  TString *ts;
} SemInfo;  /* semantics information */


typedef struct Token {
  int token;
  SemInfo seminfo;
} Token;


typedef struct LexState {
  int current;  /* current character */
  Token t;  /* current token */
  Token lookahead;  /* look ahead token */
  struct FuncState *fs;  /* `FuncState' is private to the parser */
  struct lua_State *L;
  struct zio *z;  /* input stream */
  int linenumber;  /* input line counter */
  int lastline;  /* line of last token `consumed' */
  TString *source;  /* current source name */
} LexState;


void luaX_init (lua_State *L);
void luaX_setinput (lua_State *L, LexState *LS, ZIO *z, TString *source);
int luaX_lex (LexState *LS, SemInfo *seminfo);
void luaX_checklimit (LexState *ls, int val, int limit, const char *msg);
void luaX_syntaxerror (LexState *ls, const char *s, const char *token);
void luaX_error (LexState *ls, const char *s, int token);
void luaX_token2str (int token, char *s);


#endif
/* resumed: lua-4.0/src/lcode.h */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* include: lopcodes.h */
/*
** $Id: lopcodes.h,v 1.68 2000/10/24 16:05:59 roberto Exp $
** Opcodes for Lua virtual machine
** See Copyright Notice in lua.h
*/

#ifndef lopcodes_h
#define lopcodes_h

/* skipped: llimits.h - see lua-4.0/src/lobject.h */


/*===========================================================================
  We assume that instructions are unsigned numbers.
  All instructions have an opcode in the first 6 bits. Moreover,
  an instruction can have 0, 1, or 2 arguments. Instructions can
  have the following types:
  type 0: no arguments
  type 1: 1 unsigned argument in the higher bits (called `U')
  type 2: 1 signed argument in the higher bits          (`S')
  type 3: 1st unsigned argument in the higher bits      (`A')
          2nd unsigned argument in the middle bits      (`B')

  A signed argument is represented in excess K; that is, the number
  value is the unsigned value minus K. K is exactly the maximum value
  for that argument (so that -max is represented by 0, and +max is
  represented by 2*max), which is half the maximum for the corresponding
  unsigned argument.

  The size of each argument is defined in `llimits.h'. The usual is an
  instruction with 32 bits, U arguments with 26 bits (32-6), B arguments
  with 9 bits, and A arguments with 17 bits (32-6-9). For small
  installations, the instruction size can be 16, so U has 10 bits,
  and A and B have 5 bits each.
===========================================================================*/




/* creates a mask with `n' 1 bits at position `p' */
#define MASK1(n,p)	((~((~(Instruction)0)<<n))<<p)

/* creates a mask with `n' 0 bits at position `p' */
#define MASK0(n,p)	(~MASK1(n,p))

/*
** the following macros help to manipulate instructions
*/

#define CREATE_0(o)	 ((Instruction)(o))
#define GET_OPCODE(i)	((OpCode)((i)&MASK1(SIZE_OP,0)))
#define SET_OPCODE(i,o)	((i) = (((i)&MASK0(SIZE_OP,0)) | (Instruction)(o)))

#define CREATE_U(o,u)	 ((Instruction)(o) | ((Instruction)(u)<<POS_U))
#define GETARG_U(i)	((int)((i)>>POS_U))
#define SETARG_U(i,u)	((i) = (((i)&MASK0(SIZE_U,POS_U)) | \
                               ((Instruction)(u)<<POS_U)))

#define CREATE_S(o,s)	CREATE_U((o),(s)+MAXARG_S)
#define GETARG_S(i)	(GETARG_U(i)-MAXARG_S)
#define SETARG_S(i,s)	SETARG_U((i),(s)+MAXARG_S)


#define CREATE_AB(o,a,b) ((Instruction)(o) | ((Instruction)(a)<<POS_A) \
                                           |  ((Instruction)(b)<<POS_B))
#define GETARG_A(i)	((int)((i)>>POS_A))
#define SETARG_A(i,a)	((i) = (((i)&MASK0(SIZE_A,POS_A)) | \
                               ((Instruction)(a)<<POS_A)))
#define GETARG_B(i)	((int)(((i)>>POS_B) & MASK1(SIZE_B,0)))
#define SETARG_B(i,b)	((i) = (((i)&MASK0(SIZE_B,POS_B)) | \
                               ((Instruction)(b)<<POS_B)))


/*
** K = U argument used as index to `kstr'
** J = S argument used as jump offset (relative to pc of next instruction)
** L = unsigned argument used as index of local variable
** N = U argument used as index to `knum'
*/

typedef enum {
/*----------------------------------------------------------------------
name		args	stack before	stack after	side effects
------------------------------------------------------------------------*/
OP_END,/*	-	-		(return)	no results	*/
OP_RETURN,/*	U	v_n-v_x(at u)	(return)	returns v_x-v_n	*/

OP_CALL,/*	A B	v_n-v_1 f(at a)	r_b-r_1		f(v1,...,v_n)	*/
OP_TAILCALL,/*	A B	v_n-v_1 f(at a)	(return)	f(v1,...,v_n)	*/

OP_PUSHNIL,/*	U	-		nil_1-nil_u			*/
OP_POP,/*	U	a_u-a_1		-				*/

OP_PUSHINT,/*	S	-		(Number)s			*/
OP_PUSHSTRING,/* K	-		KSTR[k]				*/
OP_PUSHNUM,/*	N	-		KNUM[n]				*/
OP_PUSHNEGNUM,/* N	-		-KNUM[n]			*/

OP_PUSHUPVALUE,/* U	-		Closure[u]			*/

OP_GETLOCAL,/*	L	-		LOC[l]				*/
OP_GETGLOBAL,/*	K	-		VAR[KSTR[k]]			*/

OP_GETTABLE,/*	-	i t		t[i]				*/
OP_GETDOTTED,/*	K	t		t[KSTR[k]]			*/
OP_GETINDEXED,/* L	t		t[LOC[l]]			*/
OP_PUSHSELF,/*	K	t		t t[KSTR[k]]			*/

OP_CREATETABLE,/* U	-		newarray(size = u)		*/

OP_SETLOCAL,/*	L	x		-		LOC[l]=x	*/
OP_SETGLOBAL,/*	K	x		-		VAR[KSTR[k]]=x	*/
OP_SETTABLE,/*	A B	v a_a-a_1 i t	(pops b values)	t[i]=v		*/

OP_SETLIST,/*	A B	v_b-v_1 t	t		t[i+a*FPF]=v_i	*/
OP_SETMAP,/*	U	v_u k_u - v_1 k_1 t	t	t[k_i]=v_i	*/

OP_ADD,/*	-	y x		x+y				*/
OP_ADDI,/*	S	x		x+s				*/
OP_SUB,/*	-	y x		x-y				*/
OP_MULT,/*	-	y x		x*y				*/
OP_DIV,/*	-	y x		x/y				*/
OP_POW,/*	-	y x		x^y				*/
OP_CONCAT,/*	U	v_u-v_1		v1..-..v_u			*/
OP_MINUS,/*	-	x		-x				*/
OP_NOT,/*	-	x		(x==nil)? 1 : nil		*/

OP_JMPNE,/*	J	y x		-		(x~=y)? PC+=s	*/
OP_JMPEQ,/*	J	y x		-		(x==y)? PC+=s	*/
OP_JMPLT,/*	J	y x		-		(x<y)? PC+=s	*/
OP_JMPLE,/*	J	y x		-		(x<y)? PC+=s	*/
OP_JMPGT,/*	J	y x		-		(x>y)? PC+=s	*/
OP_JMPGE,/*	J	y x		-		(x>=y)? PC+=s	*/

OP_JMPT,/*	J	x		-		(x~=nil)? PC+=s	*/
OP_JMPF,/*	J	x		-		(x==nil)? PC+=s	*/
OP_JMPONT,/*	J	x		(x~=nil)? x : -	(x~=nil)? PC+=s	*/
OP_JMPONF,/*	J	x		(x==nil)? x : -	(x==nil)? PC+=s	*/
OP_JMP,/*	J	-		-		PC+=s		*/

OP_PUSHNILJMP,/* -	-		nil		PC++;		*/

OP_FORPREP,/*	J							*/
OP_FORLOOP,/*	J							*/

OP_LFORPREP,/*	J							*/
OP_LFORLOOP,/*	J							*/

OP_CLOSURE/*	A B	v_b-v_1		closure(KPROTO[a], v_1-v_b)	*/

} OpCode;

#define NUM_OPCODES	((int)OP_CLOSURE+1)


#define ISJUMP(o)	(OP_JMPNE <= (o) && (o) <= OP_JMP)



/* special code to fit a LUA_MULTRET inside an argB */
#define MULT_RET        255	/* (<=MAXARG_B) */
#if MULT_RET>MAXARG_B
#undef MULT_RET
#define MULT_RET	MAXARG_B
#endif


#endif
/* resumed: lua-4.0/src/lcode.h */
/* include: lparser.h */
/*
** $Id: lparser.h,v 1.26 2000/10/09 13:47:46 roberto Exp $
** LL(1) Parser and code generator for Lua
** See Copyright Notice in lua.h
*/

#ifndef lparser_h
#define lparser_h

/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lzio.h - see lua-4.0/src/llex.h */


/*
** Expression descriptor
*/

typedef enum {
  VGLOBAL,
  VLOCAL,
  VINDEXED,
  VEXP
} expkind;

typedef struct expdesc {
  expkind k;
  union {
    int index;  /* VGLOBAL: `kstr' index of global name; VLOCAL: stack index */
    struct {
      int t;  /* patch list of `exit when true' */
      int f;  /* patch list of `exit when false' */
    } l;
  } u;
} expdesc;



/* state needed to generate code for a given function */
typedef struct FuncState {
  Proto *f;  /* current function header */
  struct FuncState *prev;  /* enclosing function */
  struct LexState *ls;  /* lexical state */
  struct lua_State *L;  /* copy of the Lua state */
  int pc;  /* next position to code */
  int lasttarget;   /* `pc' of last `jump target' */
  int jlt;  /* list of jumps to `lasttarget' */
  short stacklevel;  /* number of values on activation register */
  short nactloc;  /* number of active local variables */
  short nupvalues;  /* number of upvalues */
  int lastline;  /* line where last `lineinfo' was generated */
  struct Breaklabel *bl;  /* chain of breakable blocks */
  expdesc upvalues[MAXUPVALUES];  /* upvalues */
  int actloc[MAXLOCALS];  /* local-variable stack (indices to locvars) */
} FuncState;


Proto *luaY_parser (lua_State *L, ZIO *z);


#endif
/* resumed: lua-4.0/src/lcode.h */


/*
** Marks the end of a patch list. It is an invalid value both as an absolute
** address, and as a list link (would link an element to itself).
*/
#define NO_JUMP (-1)


/*
** grep "ORDER OPR" if you change these enums
*/
typedef enum BinOpr {
  OPR_ADD, OPR_SUB, OPR_MULT, OPR_DIV, OPR_POW,
  OPR_CONCAT,
  OPR_NE, OPR_EQ, OPR_LT, OPR_LE, OPR_GT, OPR_GE,
  OPR_AND, OPR_OR,
  OPR_NOBINOPR
} BinOpr;

typedef enum UnOpr { OPR_MINUS, OPR_NOT, OPR_NOUNOPR } UnOpr;


enum Mode {iO, iU, iS, iAB};  /* instruction format */

#define VD	100	/* flag for variable delta */

extern const struct OpProperties {
  char mode;
  unsigned char push;
  unsigned char pop;
} luaK_opproperties[];


void luaK_error (LexState *ls, const char *msg);
int luaK_code0 (FuncState *fs, OpCode o);
int luaK_code1 (FuncState *fs, OpCode o, int arg1);
int luaK_code2 (FuncState *fs, OpCode o, int arg1, int arg2);
int luaK_jump (FuncState *fs);
void luaK_patchlist (FuncState *fs, int list, int target);
void luaK_concat (FuncState *fs, int *l1, int l2);
void luaK_goiftrue (FuncState *fs, expdesc *v, int keepvalue);
int luaK_getlabel (FuncState *fs);
void luaK_deltastack (FuncState *fs, int delta);
void luaK_kstr (LexState *ls, int c);
void luaK_number (FuncState *fs, Number f);
void luaK_adjuststack (FuncState *fs, int n);
int luaK_lastisopen (FuncState *fs);
void luaK_setcallreturns (FuncState *fs, int nresults);
void luaK_tostack (LexState *ls, expdesc *v, int onlyone);
void luaK_storevar (LexState *ls, const expdesc *var);
void luaK_prefix (LexState *ls, UnOpr op, expdesc *v);
void luaK_infix (LexState *ls, BinOpr op, expdesc *v);
void luaK_posfix (LexState *ls, BinOpr op, expdesc *v1, expdesc *v2);


#endif
/* resumed: lua-4.0/src/lcode.c */
/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: llex.h - see lua-4.0/src/lcode.h */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lparser.h - see lua-4.0/src/lcode.h */


void luaK_error (LexState *ls, const char *msg) {
  luaX_error(ls, msg, ls->t.token);
}


/*
** Returns the the previous instruction, for optimizations.
** If there is a jump target between this and the current instruction,
** returns a dummy instruction to avoid wrong optimizations.
*/
static Instruction previous_instruction (FuncState *fs) {
  if (fs->pc > fs->lasttarget)  /* no jumps to current position? */
    return fs->f->code[fs->pc-1];  /* returns previous instruction */
  else
    return CREATE_0(OP_END);  /* no optimizations after an `END' */
}


int luaK_jump (FuncState *fs) {
  int j = luaK_code1(fs, OP_JMP, NO_JUMP);
  if (j == fs->lasttarget) {  /* possible jumps to this jump? */
    luaK_concat(fs, &j, fs->jlt);  /* keep them on hold */
    fs->jlt = NO_JUMP;
  }
  return j;
}


static void luaK_fixjump (FuncState *fs, int pc, int dest) {
  Instruction *jmp = &fs->f->code[pc];
  if (dest == NO_JUMP)
    SETARG_S(*jmp, NO_JUMP);  /* point to itself to represent end of list */
  else {  /* jump is relative to position following jump instruction */
    int offset = dest-(pc+1);
    if (abs(offset) > MAXARG_S)
      luaK_error(fs->ls, "control structure too long");
    SETARG_S(*jmp, offset);
  }
}


static int luaK_getjump (FuncState *fs, int pc) {
  int offset = GETARG_S(fs->f->code[pc]);
  if (offset == NO_JUMP)  /* point to itself represents end of list */
    return NO_JUMP;  /* end of list */
  else
    return (pc+1)+offset;  /* turn offset into absolute position */
}


/*
** returns current `pc' and marks it as a jump target (to avoid wrong
** optimizations with consecutive instructions not in the same basic block).
** discharge list of jumps to last target.
*/
int luaK_getlabel (FuncState *fs) {
  if (fs->pc != fs->lasttarget) {
    int lasttarget = fs->lasttarget;
    fs->lasttarget = fs->pc;
    luaK_patchlist(fs, fs->jlt, lasttarget);  /* discharge old list `jlt' */
    fs->jlt = NO_JUMP;  /* nobody jumps to this new label (yet) */
  }
  return fs->pc;
}


void luaK_deltastack (FuncState *fs, int delta) {
  fs->stacklevel += delta;
  if (fs->stacklevel > fs->f->maxstacksize) {
    if (fs->stacklevel > MAXSTACK)
      luaK_error(fs->ls, "function or expression too complex");
    fs->f->maxstacksize = fs->stacklevel;
  }
}


void luaK_kstr (LexState *ls, int c) {
  luaK_code1(ls->fs, OP_PUSHSTRING, c);
}


static int number_constant (FuncState *fs, Number r) {
  /* check whether `r' has appeared within the last LOOKBACKNUMS entries */
  Proto *f = fs->f;
  int c = f->nknum;
  int lim = c < LOOKBACKNUMS ? 0 : c-LOOKBACKNUMS;
  while (--c >= lim)
    if (f->knum[c] == r) return c;
  /* not found; create a new entry */
  luaM_growvector(fs->L, f->knum, f->nknum, 1, Number,
                  "constant table overflow", MAXARG_U);
  c = f->nknum++;
  f->knum[c] = r;
  return c;
}


void luaK_number (FuncState *fs, Number f) {
  if (f <= (Number)MAXARG_S && (Number)(int)f == f)
    luaK_code1(fs, OP_PUSHINT, (int)f);  /* f has a short integer value */
  else
    luaK_code1(fs, OP_PUSHNUM, number_constant(fs, f));
}


void luaK_adjuststack (FuncState *fs, int n) {
  if (n > 0)
    luaK_code1(fs, OP_POP, n);
  else
    luaK_code1(fs, OP_PUSHNIL, -n);
}


int luaK_lastisopen (FuncState *fs) {
  /* check whether last instruction is an open function call */
  Instruction i = previous_instruction(fs);
  if (GET_OPCODE(i) == OP_CALL && GETARG_B(i) == MULT_RET)
    return 1;
  else return 0;
}


void luaK_setcallreturns (FuncState *fs, int nresults) {
  if (luaK_lastisopen(fs)) {  /* expression is an open function call? */
    SETARG_B(fs->f->code[fs->pc-1], nresults);  /* set number of results */
    luaK_deltastack(fs, nresults);  /* push results */
  }
}


static int discharge (FuncState *fs, expdesc *var) {
  switch (var->k) {
    case VLOCAL:
      luaK_code1(fs, OP_GETLOCAL, var->u.index);
      break;
    case VGLOBAL:
      luaK_code1(fs, OP_GETGLOBAL, var->u.index);
      break;
    case VINDEXED:
      luaK_code0(fs, OP_GETTABLE);
      break;
    case VEXP:
      return 0;  /* nothing to do */
  }
  var->k = VEXP;
  var->u.l.t = var->u.l.f = NO_JUMP;
  return 1;
}


static void discharge1 (FuncState *fs, expdesc *var) {
  discharge(fs, var);
 /* if it has jumps then it is already discharged */
  if (var->u.l.t == NO_JUMP && var->u.l.f  == NO_JUMP)
    luaK_setcallreturns(fs, 1);  /* call must return 1 value */
}


void luaK_storevar (LexState *ls, const expdesc *var) {
  FuncState *fs = ls->fs;
  switch (var->k) {
    case VLOCAL:
      luaK_code1(fs, OP_SETLOCAL, var->u.index);
      break;
    case VGLOBAL:
      luaK_code1(fs, OP_SETGLOBAL, var->u.index);
      break;
    case VINDEXED:  /* table is at top-3; pop 3 elements after operation */
      luaK_code2(fs, OP_SETTABLE, 3, 3);
      break;
    default:
      LUA_INTERNALERROR("invalid var kind to store");
  }
}


static OpCode invertjump (OpCode op) {
  switch (op) {
    case OP_JMPNE: return OP_JMPEQ;
    case OP_JMPEQ: return OP_JMPNE;
    case OP_JMPLT: return OP_JMPGE;
    case OP_JMPLE: return OP_JMPGT;
    case OP_JMPGT: return OP_JMPLE;
    case OP_JMPGE: return OP_JMPLT;
    case OP_JMPT: case OP_JMPONT:  return OP_JMPF;
    case OP_JMPF: case OP_JMPONF:  return OP_JMPT;
    default:
      LUA_INTERNALERROR("invalid jump instruction");
      return OP_END;  /* to avoid warnings */
  }
}


static void luaK_patchlistaux (FuncState *fs, int list, int target,
                               OpCode special, int special_target) {
  Instruction *code = fs->f->code;
  while (list != NO_JUMP) {
    int next = luaK_getjump(fs, list);
    Instruction *i = &code[list];
    OpCode op = GET_OPCODE(*i);
    if (op == special)  /* this `op' already has a value */
      luaK_fixjump(fs, list, special_target);
    else {
      luaK_fixjump(fs, list, target);  /* do the patch */
      if (op == OP_JMPONT)  /* remove eventual values */
        SET_OPCODE(*i, OP_JMPT);
      else if (op == OP_JMPONF)
        SET_OPCODE(*i, OP_JMPF);
    }
    list = next;
  }
}


void luaK_patchlist (FuncState *fs, int list, int target) {
  if (target == fs->lasttarget)  /* same target that list `jlt'? */
    luaK_concat(fs, &fs->jlt, list);  /* delay fixing */
  else
    luaK_patchlistaux(fs, list, target, OP_END, 0);
}


static int need_value (FuncState *fs, int list, OpCode hasvalue) {
  /* check whether list has a jump without a value */
  for (; list != NO_JUMP; list = luaK_getjump(fs, list))
    if (GET_OPCODE(fs->f->code[list]) != hasvalue) return 1;
  return 0;  /* not found */
}


void luaK_concat (FuncState *fs, int *l1, int l2) {
  if (*l1 == NO_JUMP)
    *l1 = l2;
  else {
    int list = *l1;
    for (;;) {  /* traverse `l1' */
      int next = luaK_getjump(fs, list);
      if (next == NO_JUMP) {  /* end of list? */
        luaK_fixjump(fs, list, l2);
        return;
      }
      list = next;
    }
  }
}


static void luaK_testgo (FuncState *fs, expdesc *v, int invert, OpCode jump) {
  int prevpos;  /* position of last instruction */
  Instruction *previous;
  int *golist, *exitlist;
  if (!invert) {
    golist = &v->u.l.f;    /* go if false */
    exitlist = &v->u.l.t;  /* exit if true */
  }
  else {
    golist = &v->u.l.t;    /* go if true */
    exitlist = &v->u.l.f;  /* exit if false */
  }
  discharge1(fs, v);
  prevpos = fs->pc-1;
  previous = &fs->f->code[prevpos];
  LUA_ASSERT(*previous==previous_instruction(fs), "no jump allowed here");
  if (!ISJUMP(GET_OPCODE(*previous)))
    prevpos = luaK_code1(fs, jump, NO_JUMP);
  else {  /* last instruction is already a jump */
    if (invert)
      SET_OPCODE(*previous, invertjump(GET_OPCODE(*previous)));
  }
  luaK_concat(fs, exitlist, prevpos);  /* insert last jump in `exitlist' */
  luaK_patchlist(fs, *golist, luaK_getlabel(fs));
  *golist = NO_JUMP;
}


void luaK_goiftrue (FuncState *fs, expdesc *v, int keepvalue) {
  luaK_testgo(fs, v, 1, keepvalue ? OP_JMPONF : OP_JMPF);
}


static void luaK_goiffalse (FuncState *fs, expdesc *v, int keepvalue) {
  luaK_testgo(fs, v, 0, keepvalue ? OP_JMPONT : OP_JMPT);
}


static int code_label (FuncState *fs, OpCode op, int arg) {
  luaK_getlabel(fs);  /* those instructions may be jump targets */
  return luaK_code1(fs, op, arg);
}


void luaK_tostack (LexState *ls, expdesc *v, int onlyone) {
  FuncState *fs = ls->fs;
  if (!discharge(fs, v)) {  /* `v' is an expression? */
    OpCode previous = GET_OPCODE(fs->f->code[fs->pc-1]);
    if (!ISJUMP(previous) && v->u.l.f == NO_JUMP && v->u.l.t == NO_JUMP) {
      /* expression has no jumps */
      if (onlyone)
        luaK_setcallreturns(fs, 1);  /* call must return 1 value */
    }
    else {  /* expression has jumps */
      int final;  /* position after whole expression */
      int j = NO_JUMP;  /*  eventual  jump over values */
      int p_nil = NO_JUMP;  /* position of an eventual PUSHNIL */
      int p_1 = NO_JUMP;  /* position of an eventual PUSHINT */
      if (ISJUMP(previous) || need_value(fs, v->u.l.f, OP_JMPONF)
                           || need_value(fs, v->u.l.t, OP_JMPONT)) {
        /* expression needs values */
        if (ISJUMP(previous))
          luaK_concat(fs, &v->u.l.t, fs->pc-1);  /* put `previous' in t. list */
        else {
          j = code_label(fs, OP_JMP, NO_JUMP);  /* to jump over both pushes */
          /* correct stack for compiler and symbolic execution */
          luaK_adjuststack(fs, 1);
        }
        p_nil = code_label(fs, OP_PUSHNILJMP, 0);
        p_1 = code_label(fs, OP_PUSHINT, 1);
        luaK_patchlist(fs, j, luaK_getlabel(fs));
      }
      final = luaK_getlabel(fs);
      luaK_patchlistaux(fs, v->u.l.f, p_nil, OP_JMPONF, final);
      luaK_patchlistaux(fs, v->u.l.t, p_1, OP_JMPONT, final);
      v->u.l.f = v->u.l.t = NO_JUMP;
    }
  }
}


void luaK_prefix (LexState *ls, UnOpr op, expdesc *v) {
  FuncState *fs = ls->fs;
  if (op == OPR_MINUS) {
    luaK_tostack(ls, v, 1);
    luaK_code0(fs, OP_MINUS);
  }
  else {  /* op == NOT */
    Instruction *previous;
    discharge1(fs, v);
    previous = &fs->f->code[fs->pc-1];
    if (ISJUMP(GET_OPCODE(*previous)))
      SET_OPCODE(*previous, invertjump(GET_OPCODE(*previous)));
    else
      luaK_code0(fs, OP_NOT);
    /* interchange true and false lists */
    { int temp = v->u.l.f; v->u.l.f = v->u.l.t; v->u.l.t = temp; }
  }
}


void luaK_infix (LexState *ls, BinOpr op, expdesc *v) {
  FuncState *fs = ls->fs;
  switch (op) {
    case OPR_AND:
      luaK_goiftrue(fs, v, 1);
      break;
    case OPR_OR:
      luaK_goiffalse(fs, v, 1);
      break;
    default:
      luaK_tostack(ls, v, 1);  /* all other binary operators need a value */
  }
}



static const struct {
  OpCode opcode;  /* opcode for each binary operator */
  int arg;        /* default argument for the opcode */
} codes[] = {  /* ORDER OPR */
      {OP_ADD, 0}, {OP_SUB, 0}, {OP_MULT, 0}, {OP_DIV, 0},
      {OP_POW, 0}, {OP_CONCAT, 2},
      {OP_JMPNE, NO_JUMP}, {OP_JMPEQ, NO_JUMP},
      {OP_JMPLT, NO_JUMP}, {OP_JMPLE, NO_JUMP},
      {OP_JMPGT, NO_JUMP}, {OP_JMPGE, NO_JUMP}
};


void luaK_posfix (LexState *ls, BinOpr op, expdesc *v1, expdesc *v2) {
  FuncState *fs = ls->fs;
  switch (op) {
    case OPR_AND: {
      LUA_ASSERT(v1->u.l.t == NO_JUMP, "list must be closed");
      discharge1(fs, v2);
      v1->u.l.t = v2->u.l.t;
      luaK_concat(fs, &v1->u.l.f, v2->u.l.f);
      break;
    }
    case OPR_OR: {
      LUA_ASSERT(v1->u.l.f == NO_JUMP, "list must be closed");
      discharge1(fs, v2);
      v1->u.l.f = v2->u.l.f;
      luaK_concat(fs, &v1->u.l.t, v2->u.l.t);
      break;
    }
    default: {
      luaK_tostack(ls, v2, 1);  /* `v2' must be a value */
      luaK_code1(fs, codes[op].opcode, codes[op].arg);
    }
  }
}


static void codelineinfo (FuncState *fs) {
  Proto *f = fs->f;
  LexState *ls = fs->ls;
  if (ls->lastline > fs->lastline) {
    luaM_growvector(fs->L, f->lineinfo, f->nlineinfo, 2, int,
                    "line info overflow", MAX_INT);
    if (ls->lastline > fs->lastline+1)
      f->lineinfo[f->nlineinfo++] = -(ls->lastline - (fs->lastline+1));
    f->lineinfo[f->nlineinfo++] = fs->pc;
    fs->lastline = ls->lastline;
  }
}


int luaK_code0 (FuncState *fs, OpCode o) {
  return luaK_code2(fs, o, 0, 0);
}


int luaK_code1 (FuncState *fs, OpCode o, int arg1) {
  return luaK_code2(fs, o, arg1, 0);
}


int luaK_code2 (FuncState *fs, OpCode o, int arg1, int arg2) {
  Instruction i = previous_instruction(fs);
  int delta = luaK_opproperties[o].push - luaK_opproperties[o].pop;
  int optm = 0;  /* 1 when there is an optimization */
  switch (o) {
    case OP_CLOSURE: {
      delta = -arg2+1;
      break;
    }
    case OP_SETTABLE: {
      delta = -arg2;
      break;
    }
    case OP_SETLIST: {
      if (arg2 == 0) return NO_JUMP;  /* nothing to do */
      delta = -arg2;
      break;
    }
    case OP_SETMAP: {
      if (arg1 == 0) return NO_JUMP;  /* nothing to do */
      delta = -2*arg1;
      break;
    }
    case OP_RETURN: {
      if (GET_OPCODE(i) == OP_CALL && GETARG_B(i) == MULT_RET) {
        SET_OPCODE(i, OP_TAILCALL);
        SETARG_B(i, arg1);
        optm = 1;
      }
      break;
    }
    case OP_PUSHNIL: {
      if (arg1 == 0) return NO_JUMP;  /* nothing to do */
      delta = arg1;
      switch(GET_OPCODE(i)) {
        case OP_PUSHNIL: SETARG_U(i, GETARG_U(i)+arg1); optm = 1; break;
        default: break;
      }
      break;
    }
    case OP_POP: {
      if (arg1 == 0) return NO_JUMP;  /* nothing to do */
      delta = -arg1;
      switch(GET_OPCODE(i)) {
        case OP_SETTABLE: SETARG_B(i, GETARG_B(i)+arg1); optm = 1; break;
        default: break;
      }
      break;
    }
    case OP_GETTABLE: {
      switch(GET_OPCODE(i)) {
        case OP_PUSHSTRING:  /* `t.x' */
          SET_OPCODE(i, OP_GETDOTTED);
          optm = 1;
          break;
        case OP_GETLOCAL:  /* `t[i]' */
          SET_OPCODE(i, OP_GETINDEXED);
          optm = 1;
          break;
        default: break;
      }
      break;
    }
    case OP_ADD: {
      switch(GET_OPCODE(i)) {
        case OP_PUSHINT: SET_OPCODE(i, OP_ADDI); optm = 1; break;  /* `a+k' */
        default: break;
      }
      break;
    }
    case OP_SUB: {
      switch(GET_OPCODE(i)) {
        case OP_PUSHINT:  /* `a-k' */
          i = CREATE_S(OP_ADDI, -GETARG_S(i));
          optm = 1;
          break;
        default: break;
      }
      break;
    }
    case OP_CONCAT: {
      delta = -arg1+1;
      switch(GET_OPCODE(i)) {
        case OP_CONCAT:  /* `a..b..c' */
          SETARG_U(i, GETARG_U(i)+1);
          optm = 1;
          break;
        default: break;
      }
      break;
    }
    case OP_MINUS: {
      switch(GET_OPCODE(i)) {
        case OP_PUSHINT:  /* `-k' */
          SETARG_S(i, -GETARG_S(i));
          optm = 1;
          break;
        case OP_PUSHNUM:  /* `-k' */
          SET_OPCODE(i, OP_PUSHNEGNUM);
          optm = 1;
          break;
        default: break;
      }
      break;
    }
    case OP_JMPNE: {
      if (i == CREATE_U(OP_PUSHNIL, 1)) {  /* `a~=nil' */
        i = CREATE_S(OP_JMPT, NO_JUMP);
        optm = 1;
      }
      break;
    }
    case OP_JMPEQ: {
      if (i == CREATE_U(OP_PUSHNIL, 1)) {  /* `a==nil' */
        i = CREATE_0(OP_NOT);
        delta = -1;  /* just undo effect of previous PUSHNIL */
        optm = 1;
      }
      break;
    }
    case OP_JMPT:
    case OP_JMPONT: {
      switch (GET_OPCODE(i)) {
        case OP_NOT: {
          i = CREATE_S(OP_JMPF, NO_JUMP);
          optm = 1;
          break;
        }
        case OP_PUSHINT: {
          if (o == OP_JMPT) {  /* JMPONT must keep original integer value */
            i = CREATE_S(OP_JMP, NO_JUMP);
            optm = 1;
          }
          break;
        }
        case OP_PUSHNIL: {
          if (GETARG_U(i) == 1) {
            fs->pc--;  /* erase previous instruction */
            luaK_deltastack(fs, -1);  /* correct stack */
            return NO_JUMP; 
          }
          break;
        }
        default: break;
      }
      break;
    }
    case OP_JMPF:
    case OP_JMPONF: {
      switch (GET_OPCODE(i)) {
        case OP_NOT: {
          i = CREATE_S(OP_JMPT, NO_JUMP);
          optm = 1;
          break;
        }
        case OP_PUSHINT: {  /* `while 1 do ...' */
          fs->pc--;  /* erase previous instruction */
          luaK_deltastack(fs, -1);  /* correct stack */
          return NO_JUMP; 
        }
        case OP_PUSHNIL: {  /* `repeat ... until nil' */
          if (GETARG_U(i) == 1) {
            i = CREATE_S(OP_JMP, NO_JUMP);
            optm = 1;
          }
          break;
        }
        default: break;
      }
      break;
    }
    case OP_GETDOTTED:
    case OP_GETINDEXED:
    case OP_TAILCALL:
    case OP_ADDI: {
      LUA_INTERNALERROR("instruction used only for optimizations");
      break;
    }
    default: {
      LUA_ASSERT(delta != VD, "invalid delta");
      break;
    }
  }
  luaK_deltastack(fs, delta);
  if (optm) {  /* optimize: put instruction in place of last one */
      fs->f->code[fs->pc-1] = i;  /* change previous instruction */
      return fs->pc-1;  /* do not generate new instruction */
  }
  /* else build new instruction */
  switch ((enum Mode)luaK_opproperties[o].mode) {
    case iO: i = CREATE_0(o); break;
    case iU: i = CREATE_U(o, arg1); break;
    case iS: i = CREATE_S(o, arg1); break;
    case iAB: i = CREATE_AB(o, arg1, arg2); break;
  }
  codelineinfo(fs);
  /* put new instruction in code array */
  luaM_growvector(fs->L, fs->f->code, fs->pc, 1, Instruction,
                  "code size overflow", MAX_INT);
  fs->f->code[fs->pc] = i;
  return fs->pc++;
}


const struct OpProperties luaK_opproperties[NUM_OPCODES] = {
  {iO, 0, 0},	/* OP_END */
  {iU, 0, 0},	/* OP_RETURN */
  {iAB, 0, 0},	/* OP_CALL */
  {iAB, 0, 0},	/* OP_TAILCALL */
  {iU, VD, 0},	/* OP_PUSHNIL */
  {iU, VD, 0},	/* OP_POP */
  {iS, 1, 0},	/* OP_PUSHINT */
  {iU, 1, 0},	/* OP_PUSHSTRING */
  {iU, 1, 0},	/* OP_PUSHNUM */
  {iU, 1, 0},	/* OP_PUSHNEGNUM */
  {iU, 1, 0},	/* OP_PUSHUPVALUE */
  {iU, 1, 0},	/* OP_GETLOCAL */
  {iU, 1, 0},	/* OP_GETGLOBAL */
  {iO, 1, 2},	/* OP_GETTABLE */
  {iU, 1, 1},	/* OP_GETDOTTED */
  {iU, 1, 1},	/* OP_GETINDEXED */
  {iU, 2, 1},	/* OP_PUSHSELF */
  {iU, 1, 0},	/* OP_CREATETABLE */
  {iU, 0, 1},	/* OP_SETLOCAL */
  {iU, 0, 1},	/* OP_SETGLOBAL */
  {iAB, VD, 0},	/* OP_SETTABLE */
  {iAB, VD, 0},	/* OP_SETLIST */
  {iU, VD, 0},	/* OP_SETMAP */
  {iO, 1, 2},	/* OP_ADD */
  {iS, 1, 1},	/* OP_ADDI */
  {iO, 1, 2},	/* OP_SUB */
  {iO, 1, 2},	/* OP_MULT */
  {iO, 1, 2},	/* OP_DIV */
  {iO, 1, 2},	/* OP_POW */
  {iU, VD, 0},	/* OP_CONCAT */
  {iO, 1, 1},	/* OP_MINUS */
  {iO, 1, 1},	/* OP_NOT */
  {iS, 0, 2},	/* OP_JMPNE */
  {iS, 0, 2},	/* OP_JMPEQ */
  {iS, 0, 2},	/* OP_JMPLT */
  {iS, 0, 2},	/* OP_JMPLE */
  {iS, 0, 2},	/* OP_JMPGT */
  {iS, 0, 2},	/* OP_JMPGE */
  {iS, 0, 1},	/* OP_JMPT */
  {iS, 0, 1},	/* OP_JMPF */
  {iS, 0, 1},	/* OP_JMPONT */
  {iS, 0, 1},	/* OP_JMPONF */
  {iS, 0, 0},	/* OP_JMP */
  {iO, 0, 0},	/* OP_PUSHNILJMP */
  {iS, 0, 0},	/* OP_FORPREP */
  {iS, 0, 3},	/* OP_FORLOOP */
  {iS, 2, 0},	/* OP_LFORPREP */
  {iS, 0, 3},	/* OP_LFORLOOP */
  {iAB, VD, 0}	/* OP_CLOSURE */
};

/* resumed: mluxsys.c */
/* include: ldebug.c */
/*
** $Id: ldebug.c,v 1.50 2000/10/30 12:38:50 roberto Exp $
** Debug Interface
** See Copyright Notice in lua.h
*/


#include <stdlib.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lapi.h - see lua-4.0/src/lapi.c */
/* skipped: lcode.h - see lua-4.0/src/lcode.c */
/* include: ldebug.h */
/*
** $Id: ldebug.h,v 1.7 2000/10/05 12:14:08 roberto Exp $
** Auxiliary functions from Debug Interface module
** See Copyright Notice in lua.h
*/

#ifndef ldebug_h
#define ldebug_h


/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: luadebug.h - see mluxsys.c */


void luaG_typeerror (lua_State *L, StkId o, const char *op);
void luaG_binerror (lua_State *L, StkId p1, int t, const char *op);
int luaG_getline (int *lineinfo, int pc, int refline, int *refi);
void luaG_ordererror (lua_State *L, StkId top);


#endif
/* resumed: lua-4.0/src/ldebug.c */
/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */
/* skipped: luadebug.h - see mluxsys.c */



static const char *getfuncname (lua_State *L, StkId f, const char **name);


static void setnormalized (TObject *d, const TObject *s) {
  if (ttype(s) == LUA_TMARK) {
    clvalue(d) = infovalue(s)->func;
    ttype(d) = LUA_TFUNCTION;
  }
  else *d = *s;
}


static int isLmark (StkId o) {
  return (o && ttype(o) == LUA_TMARK && !infovalue(o)->func->isC);
}


LUA_API lua_Hook lua_setcallhook (lua_State *L, lua_Hook func) {
  lua_Hook oldhook = L->callhook;
  L->callhook = func;
  return oldhook;
}


LUA_API lua_Hook lua_setlinehook (lua_State *L, lua_Hook func) {
  lua_Hook oldhook = L->linehook;
  L->linehook = func;
  return oldhook;
}


static StkId aux_stackedfunction (lua_State *L, int level, StkId top) {
  int i;
  for (i = (top-1) - L->stack; i>=0; i--) {
    if (is_T_MARK(L->stack[i].ttype)) {
      if (level == 0)
        return L->stack+i;
      level--;
    }
  }
  return NULL;
}


LUA_API int lua_getstack (lua_State *L, int level, lua_Debug *ar) {
  StkId f = aux_stackedfunction(L, level, L->top);
  if (f == NULL) return 0;  /* there is no such level */
  else {
    ar->_func = f;
    return 1;
  }
}


static int nups (StkId f) {
  switch (ttype(f)) {
    case LUA_TFUNCTION:
      return clvalue(f)->nupvalues;
    case LUA_TMARK:
      return infovalue(f)->func->nupvalues;
    default:
      return 0;
  }
}


int luaG_getline (int *lineinfo, int pc, int refline, int *prefi) {
  int refi;
  if (lineinfo == NULL || pc == -1)
    return -1;  /* no line info or function is not active */
  refi = prefi ? *prefi : 0;
  if (lineinfo[refi] < 0)
    refline += -lineinfo[refi++]; 
  LUA_ASSERT(lineinfo[refi] >= 0, "invalid line info");
  while (lineinfo[refi] > pc) {
    refline--;
    refi--;
    if (lineinfo[refi] < 0)
      refline -= -lineinfo[refi--]; 
    LUA_ASSERT(lineinfo[refi] >= 0, "invalid line info");
  }
  for (;;) {
    int nextline = refline + 1;
    int nextref = refi + 1;
    if (lineinfo[nextref] < 0)
      nextline += -lineinfo[nextref++]; 
    LUA_ASSERT(lineinfo[nextref] >= 0, "invalid line info");
    if (lineinfo[nextref] > pc)
      break;
    refline = nextline;
    refi = nextref;
  }
  if (prefi) *prefi = refi;
  return refline;
}


static int currentpc (StkId f) {
  CallInfo *ci = infovalue(f);
  LUA_ASSERT(isLmark(f), "function has no pc");
  if (ci->pc)
    return (*ci->pc - ci->func->f.l->code) - 1;
  else
    return -1;  /* function is not active */
}


static int currentline (StkId f) {
  if (!isLmark(f))
    return -1;  /* only active lua functions have current-line information */
  else {
    CallInfo *ci = infovalue(f);
    int *lineinfo = ci->func->f.l->lineinfo;
    return luaG_getline(lineinfo, currentpc(f), 1, NULL);
  }
}



static Proto *getluaproto (StkId f) {
  return (isLmark(f) ?  infovalue(f)->func->f.l : NULL);
}


LUA_API const char *lua_getlocal (lua_State *L, const lua_Debug *ar, int n) {
  const char *name;
  StkId f = ar->_func;
  Proto *fp = getluaproto(f);
  if (!fp) return NULL;  /* `f' is not a Lua function? */
  name = luaF_getlocalname(fp, n, currentpc(f));
  if (!name) return NULL;
  luaA_pushobject(L, (f+1)+(n-1));  /* push value */
  return name;
}


LUA_API const char *lua_setlocal (lua_State *L, const lua_Debug *ar, int n) {
  const char *name;
  StkId f = ar->_func;
  Proto *fp = getluaproto(f);
  L->top--;  /* pop new value */
  if (!fp) return NULL;  /* `f' is not a Lua function? */
  name = luaF_getlocalname(fp, n, currentpc(f));
  if (!name || name[0] == '(') return NULL;  /* `(' starts private locals */
  *((f+1)+(n-1)) = *L->top;
  return name;
}


static void infoLproto (lua_Debug *ar, Proto *f) {
  ar->source = f->source->str;
  ar->linedefined = f->lineDefined;
  ar->what = "Lua";
}


static void funcinfo (lua_State *L, lua_Debug *ar, StkId func) {
  Closure *cl = NULL;
  switch (ttype(func)) {
    case LUA_TFUNCTION:
      cl = clvalue(func);
      break;
    case LUA_TMARK:
      cl = infovalue(func)->func;
      break;
    default:
      lua_error(L, "value for `lua_getinfo' is not a function");
  }
  if (cl->isC) {
    ar->source = "=C";
    ar->linedefined = -1;
    ar->what = "C";
  }
  else
    infoLproto(ar, cl->f.l);
  luaO_chunkid(ar->short_src, ar->source, sizeof(ar->short_src));
  if (ar->linedefined == 0)
    ar->what = "main";
}


static const char *travtagmethods (lua_State *L, const TObject *o) {
  if (ttype(o) == LUA_TFUNCTION) {
    int e;
    for (e=0; e<TM_N; e++) {
      int t;
      for (t=0; t<=L->last_tag; t++)
        if (clvalue(o) == luaT_gettm(L, t, e))
          return luaT_eventname[e];
    }
  }
  return NULL;
}


static const char *travglobals (lua_State *L, const TObject *o) {
  Hash *g = L->gt;
  int i;
  for (i=0; i<g->size; i++) {
    if (luaO_equalObj(o, val(node(g, i))) &&
        ttype(key(node(g, i))) == LUA_TSTRING) 
      return tsvalue(key(node(g, i)))->str;
  }
  return NULL;
}


static void getname (lua_State *L, StkId f, lua_Debug *ar) {
  TObject o;
  setnormalized(&o, f);
  /* try to find a name for given function */
  if ((ar->name = travglobals(L, &o)) != NULL)
    ar->namewhat = "global";
  /* not found: try tag methods */
  else if ((ar->name = travtagmethods(L, &o)) != NULL)
    ar->namewhat = "tag-method";
  else ar->namewhat = "";  /* not found at all */
}


LUA_API int lua_getinfo (lua_State *L, const char *what, lua_Debug *ar) {
  StkId func;
  int isactive = (*what != '>');
  if (isactive)
    func = ar->_func;
  else {
    what++;  /* skip the '>' */
    func = L->top - 1;
  }
  for (; *what; what++) {
    switch (*what) {
      case 'S': {
        funcinfo(L, ar, func);
        break;
      }
      case 'l': {
        ar->currentline = currentline(func);
        break;
      }
      case 'u': {
        ar->nups = nups(func);
        break;
      }
      case 'n': {
        ar->namewhat = (isactive) ? getfuncname(L, func, &ar->name) : NULL;
        if (ar->namewhat == NULL)
          getname(L, func, ar);
        break;
      }
      case 'f': {
        setnormalized(L->top, func);
        incr_top;  /* push function */
        break;
      }
      default: return 0;  /* invalid option */
    }
  }
  if (!isactive) L->top--;  /* pop function */
  return 1;
}


/*
** {======================================================
** Symbolic Execution
** =======================================================
*/


static int pushpc (int *stack, int pc, int top, int n) {
  while (n--)
    stack[top++] = pc-1;
  return top;
}


static Instruction luaG_symbexec (const Proto *pt, int lastpc, int stackpos) {
  int stack[MAXSTACK];  /* stores last instruction that changed a stack entry */
  const Instruction *code = pt->code;
  int top = pt->numparams;
  int pc = 0;
  if (pt->is_vararg)  /* varargs? */
    top++;  /* `arg' */
  while (pc < lastpc) {
    const Instruction i = code[pc++];
    LUA_ASSERT(0 <= top && top <= pt->maxstacksize, "wrong stack");
    switch (GET_OPCODE(i)) {
      case OP_RETURN: {
        LUA_ASSERT(top >= GETARG_U(i), "wrong stack");
        top = GETARG_U(i);
        break;
      }
      case OP_TAILCALL: {
        LUA_ASSERT(top >= GETARG_A(i), "wrong stack");
        top = GETARG_B(i);
        break;
      }
      case OP_CALL: {
        int nresults = GETARG_B(i);
        if (nresults == MULT_RET) nresults = 1;
        LUA_ASSERT(top >= GETARG_A(i), "wrong stack");
        top = pushpc(stack, pc, GETARG_A(i), nresults);
        break;
      }
      case OP_PUSHNIL: {
        top = pushpc(stack, pc, top, GETARG_U(i));
        break;
      }
      case OP_POP: {
        top -= GETARG_U(i);
        break;
      }
      case OP_SETTABLE:
      case OP_SETLIST: {
        top -= GETARG_B(i);
        break;
      }
      case OP_SETMAP: {
        top -= 2*GETARG_U(i);
        break;
      }
      case OP_CONCAT: {
        top -= GETARG_U(i);
        stack[top++] = pc-1;
        break;
      }
      case OP_CLOSURE: {
        top -= GETARG_B(i);
        stack[top++] = pc-1;
        break;
      }
      case OP_JMPONT:
      case OP_JMPONF: {
        int newpc = pc + GETARG_S(i);
        /* jump is forward and do not skip `lastpc'? */
        if (pc < newpc && newpc <= lastpc) {
          stack[top-1] = pc-1;  /* value comes from `and'/`or' */
          pc = newpc;  /* do the jump */
        }
        else
          top--;  /* do not jump; pop value */
        break;
      }
      default: {
        OpCode op = GET_OPCODE(i);
        LUA_ASSERT(luaK_opproperties[op].push != VD,
                   "invalid opcode for default");
        top -= luaK_opproperties[op].pop;
        LUA_ASSERT(top >= 0, "wrong stack");
        top = pushpc(stack, pc, top, luaK_opproperties[op].push);
      }
    }
  }
  return code[stack[stackpos]];
}


static const char *getobjname (lua_State *L, StkId obj, const char **name) {
  StkId func = aux_stackedfunction(L, 0, obj);
  if (!isLmark(func))
    return NULL;  /* not an active Lua function */
  else {
    Proto *p = infovalue(func)->func->f.l;
    int pc = currentpc(func);
    int stackpos = obj - (func+1);  /* func+1 == function base */
    Instruction i = luaG_symbexec(p, pc, stackpos);
    LUA_ASSERT(pc != -1, "function must be active");
    switch (GET_OPCODE(i)) {
      case OP_GETGLOBAL: {
        *name = p->kstr[GETARG_U(i)]->str;
        return "global";
      }
      case OP_GETLOCAL: {
        *name = luaF_getlocalname(p, GETARG_U(i)+1, pc);
        LUA_ASSERT(*name, "local must exist");
        return "local";
      }
      case OP_PUSHSELF:
      case OP_GETDOTTED: {
        *name = p->kstr[GETARG_U(i)]->str;
        return "field";
      }
      default:
        return NULL;  /* no useful name found */
    }
  }
}


static const char *getfuncname (lua_State *L, StkId f, const char **name) {
  StkId func = aux_stackedfunction(L, 0, f);  /* calling function */
  if (!isLmark(func))
    return NULL;  /* not an active Lua function */
  else {
    Proto *p = infovalue(func)->func->f.l;
    int pc = currentpc(func);
    Instruction i;
    if (pc == -1) return NULL;  /* function is not activated */
    i = p->code[pc];
    switch (GET_OPCODE(i)) {
      case OP_CALL: case OP_TAILCALL:
        return getobjname(L, (func+1)+GETARG_A(i), name);
      default:
        return NULL;  /* no useful name found */
    }
  }
}


/* }====================================================== */


void luaG_typeerror (lua_State *L, StkId o, const char *op) {
  const char *name;
  const char *kind = getobjname(L, o, &name);
  const char *t = luaO_typename(o);
  if (kind)
    luaO_verror(L, "attempt to %.30s %.20s `%.40s' (a %.10s value)",
                op, kind, name, t);
  else
    luaO_verror(L, "attempt to %.30s a %.10s value", op, t);
}


void luaG_binerror (lua_State *L, StkId p1, int t, const char *op) {
  if (ttype(p1) == t) p1++;
  LUA_ASSERT(ttype(p1) != t, "must be an error");
  luaG_typeerror(L, p1, op);
}


void luaG_ordererror (lua_State *L, StkId top) {
  const char *t1 = luaO_typename(top-2);
  const char *t2 = luaO_typename(top-1);
  if (t1[2] == t2[2])
    luaO_verror(L, "attempt to compare two %.10s values", t1);
  else
    luaO_verror(L, "attempt to compare %.10s with %.10s", t1, t2);
}

/* resumed: mluxsys.c */
/* include: ldo.c */
/*
** $Id: ldo.c,v 1.109 2000/10/30 12:38:50 roberto Exp $
** Stack and Call structure of Lua
** See Copyright Notice in lua.h
*/


#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: ldebug.h - see lua-4.0/src/ldebug.c */
/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lgc.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lparser.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */
/* include: lundump.h */
/*
** $Id: lundump.h,v 1.21 2000/10/31 16:57:23 lhf Exp $
** load pre-compiled Lua chunks
** See Copyright Notice in lua.h
*/

#ifndef lundump_h
#define lundump_h

/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lzio.h - see lua-4.0/src/llex.h */

/* load one chunk */
Proto* luaU_undump (lua_State* L, ZIO* Z);

/* find byte order */
int luaU_endianess (void);

/* definitions for headers of binary files */
#define	VERSION		0x40		/* last format change was in 4.0 */
#define	VERSION0	0x40		/* last major  change was in 4.0 */
#define ID_CHUNK	27		/* binary files start with ESC... */
#define	SIGNATURE	"Lua"		/* ...followed by this signature */

/* formats for error messages */
#define SOURCE_FMT	"<%d:%.99s>"
#define SOURCE		tf->lineDefined,tf->source->str
#define IN_FMT		" in %p " SOURCE_FMT
#define luaIN		tf,SOURCE

/* a multiple of PI for testing native format */
/* multiplying by 1E8 gives non-trivial integer values */
#define	TEST_NUMBER	3.14159265358979323846E8

#endif
/* resumed: lua-4.0/src/ldo.c */
/* skipped: lvm.h - see lua-4.0/src/lapi.c */
/* skipped: lzio.h - see lua-4.0/src/llex.h */


/* space to handle stack overflow errors */
#define DO_EXTRA_STACK	(2*LUA_MINSTACK)


void luaD_init (lua_State *L, int stacksize) {
  L->stack = luaM_newvector(L, stacksize+DO_EXTRA_STACK, TObject);
  L->nblocks += stacksize*sizeof(TObject);
  L->stack_last = L->stack+(stacksize-1);
  L->stacksize = stacksize;
  L->Cbase = L->top = L->stack;
}


void luaD_checkstack (lua_State *L, int n) {
  if (L->stack_last - L->top <= n) {  /* stack overflow? */
    if (L->stack_last-L->stack > (L->stacksize-1)) {
      /* overflow while handling overflow */
      luaD_breakrun(L, LUA_ERRERR);  /* break run without error message */
    }
    else {
      L->stack_last += DO_EXTRA_STACK;  /* to be used by error message */
      lua_error(L, "stack overflow");
    }
  }
}


static void restore_stack_limit (lua_State *L) {
  if (L->top - L->stack < L->stacksize - 1)
    L->stack_last = L->stack + (L->stacksize-1);
}


/*
** Adjust stack. Set top to base+extra, pushing NILs if needed.
** (we cannot add base+extra unless we are sure it fits in the stack;
**  otherwise the result of such operation on pointers is undefined)
*/
void luaD_adjusttop (lua_State *L, StkId base, int extra) {
  int diff = extra-(L->top-base);
  if (diff <= 0)
    L->top = base+extra;
  else {
    luaD_checkstack(L, diff);
    while (diff--)
      ttype(L->top++) = LUA_TNIL;
  }
}


/*
** Open a hole inside the stack at `pos'
*/
static void luaD_openstack (lua_State *L, StkId pos) {
  int i = L->top-pos; 
  while (i--) pos[i+1] = pos[i];
  incr_top;
}


static void dohook (lua_State *L, lua_Debug *ar, lua_Hook hook) {
  StkId old_Cbase = L->Cbase;
  StkId old_top = L->Cbase = L->top;
  luaD_checkstack(L, LUA_MINSTACK);  /* ensure minimum stack size */
  L->allowhooks = 0;  /* cannot call hooks inside a hook */
  (*hook)(L, ar);
  LUA_ASSERT(L->allowhooks == 0, "invalid allow");
  L->allowhooks = 1;
  L->top = old_top;
  L->Cbase = old_Cbase;
}


void luaD_lineHook (lua_State *L, StkId func, int line, lua_Hook linehook) {
  if (L->allowhooks) {
    lua_Debug ar;
    ar._func = func;
    ar.event = "line";
    ar.currentline = line;
    dohook(L, &ar, linehook);
  }
}


static void luaD_callHook (lua_State *L, StkId func, lua_Hook callhook,
                    const char *event) {
  if (L->allowhooks) {
    lua_Debug ar;
    ar._func = func;
    ar.event = event;
    infovalue(func)->pc = NULL;  /* function is not active */
    dohook(L, &ar, callhook);
  }
}


static StkId callCclosure (lua_State *L, const struct Closure *cl, StkId base) {
  int nup = cl->nupvalues;  /* number of upvalues */
  StkId old_Cbase = L->Cbase;
  int n;
  L->Cbase = base;       /* new base for C function */
  luaD_checkstack(L, nup+LUA_MINSTACK);  /* ensure minimum stack size */
  for (n=0; n<nup; n++)  /* copy upvalues as extra arguments */
    *(L->top++) = cl->upvalue[n];
  n = (*cl->f.c)(L);  /* do the actual call */
  L->Cbase = old_Cbase;  /* restore old C base */
  return L->top - n;  /* return index of first result */
}


void luaD_callTM (lua_State *L, Closure *f, int nParams, int nResults) {
  StkId base = L->top - nParams;
  luaD_openstack(L, base);
  clvalue(base) = f;
  ttype(base) = LUA_TFUNCTION;
  luaD_call(L, base, nResults);
}


/*
** Call a function (C or Lua). The function to be called is at *func.
** The arguments are on the stack, right after the function.
** When returns, the results are on the stack, starting at the original
** function position.
** The number of results is nResults, unless nResults=LUA_MULTRET.
*/ 
void luaD_call (lua_State *L, StkId func, int nResults) {
  lua_Hook callhook;
  StkId firstResult;
  CallInfo ci;
  Closure *cl;
  if (ttype(func) != LUA_TFUNCTION) {
    /* `func' is not a function; check the `function' tag method */
    Closure *tm = luaT_gettmbyObj(L, func, TM_FUNCTION);
    if (tm == NULL)
      luaG_typeerror(L, func, "call");
    luaD_openstack(L, func);
    clvalue(func) = tm;  /* tag method is the new function to be called */
    ttype(func) = LUA_TFUNCTION;
  }
  cl = clvalue(func);
  ci.func = cl;
  infovalue(func) = &ci;
  ttype(func) = LUA_TMARK;
  callhook = L->callhook;
  if (callhook)
    luaD_callHook(L, func, callhook, "call");
  firstResult = (cl->isC ? callCclosure(L, cl, func+1) :
                           luaV_execute(L, cl, func+1));
  if (callhook)  /* same hook that was active at entry */
    luaD_callHook(L, func, callhook, "return");
  LUA_ASSERT(ttype(func) == LUA_TMARK, "invalid tag");
  /* move results to `func' (to erase parameters and function) */
  if (nResults == LUA_MULTRET) {
    while (firstResult < L->top)  /* copy all results */
      *func++ = *firstResult++;
    L->top = func;
  }
  else {  /* copy at most `nResults' */
    for (; nResults > 0 && firstResult < L->top; nResults--)
      *func++ = *firstResult++;
    L->top = func;
    for (; nResults > 0; nResults--) {  /* if there are not enough results */
      ttype(L->top) = LUA_TNIL;  /* adjust the stack */
      incr_top;  /* must check stack space */
    }
  }
  luaC_checkGC(L);
}


/*
** Execute a protected call.
*/
struct CallS {  /* data to `f_call' */
  StkId func;
  int nresults;
};

static void f_call (lua_State *L, void *ud) {
  struct CallS *c = (struct CallS *)ud;
  luaD_call(L, c->func, c->nresults);
}


LUA_API int lua_call (lua_State *L, int nargs, int nresults) {
  StkId func = L->top - (nargs+1);  /* function to be called */
  struct CallS c;
  int status;
  c.func = func; c.nresults = nresults;
  status = luaD_runprotected(L, f_call, &c);
  if (status != 0)  /* an error occurred? */
    L->top = func;  /* remove parameters from the stack */
  return status;
}


/*
** Execute a protected parser.
*/
struct ParserS {  /* data to `f_parser' */
  ZIO *z;
  int bin;
};

static void f_parser (lua_State *L, void *ud) {
  struct ParserS *p = (struct ParserS *)ud;
  Proto *tf = p->bin ? luaU_undump(L, p->z) : luaY_parser(L, p->z);
  luaV_Lclosure(L, tf, 0);
}


static int protectedparser (lua_State *L, ZIO *z, int bin) {
  struct ParserS p;
  unsigned long old_blocks;
  int status;
  p.z = z; p.bin = bin;
  luaC_checkGC(L);
  old_blocks = L->nblocks;
  status = luaD_runprotected(L, f_parser, &p);
  if (status == 0) {
    /* add new memory to threshold (as it probably will stay) */
    L->GCthreshold += (L->nblocks - old_blocks);
  }
  else if (status == LUA_ERRRUN)  /* an error occurred: correct error code */
    status = LUA_ERRSYNTAX;
  return status;
}


static int parse_file (lua_State *L, const char *filename) {
  ZIO z;
  int status;
  int bin;  /* flag for file mode */
  int c;    /* look ahead char */
  FILE *f = (filename == NULL) ? stdin : fopen(filename, "r");
  if (f == NULL) return LUA_ERRFILE;  /* unable to open file */
  c = fgetc(f);
  ungetc(c, f);
  bin = (c == ID_CHUNK);
  if (bin && f != stdin) {
    f = freopen(filename, "rb", f);  /* set binary mode */
    if (f == NULL) return LUA_ERRFILE;  /* unable to reopen file */
  }
  lua_pushstring(L, "@");
  lua_pushstring(L, (filename == NULL) ? "(stdin)" : filename);
  lua_concat(L, 2);
  filename = lua_tostring(L, -1);  /* filename = '@'..filename */
  lua_pop(L, 1);  /* OK: there is no GC during parser */
  luaZ_Fopen(&z, f, filename);
  status = protectedparser(L, &z, bin);
  if (f != stdin)
    fclose(f);
  return status;
}


LUA_API int lua_dofile (lua_State *L, const char *filename) {
  int status = parse_file(L, filename);
  if (status == 0)  /* parse OK? */
    status = lua_call(L, 0, LUA_MULTRET);  /* call main */
  return status;
}


static int parse_buffer (lua_State *L, const char *buff, size_t size,
                         const char *name) {
  ZIO z;
  if (!name) name = "?";
  luaZ_mopen(&z, buff, size, name);
  return protectedparser(L, &z, buff[0]==ID_CHUNK);
}


LUA_API int lua_dobuffer (lua_State *L, const char *buff, size_t size, const char *name) {
  int status = parse_buffer(L, buff, size, name);
  if (status == 0)  /* parse OK? */
    status = lua_call(L, 0, LUA_MULTRET);  /* call main */
  return status;
}


LUA_API int lua_dostring (lua_State *L, const char *str) {
  return lua_dobuffer(L, str, strlen(str), str);
}


/*
** {======================================================
** Error-recover functions (based on long jumps)
** =======================================================
*/

/* chain list of long jump buffers */
struct lua_longjmp {
  jmp_buf b;
  struct lua_longjmp *previous;
  volatile int status;  /* error code */
};


static void message (lua_State *L, const char *s) {
  const TObject *em = luaH_getglobal(L, LUA_ERRORMESSAGE);
  if (ttype(em) == LUA_TFUNCTION) {
    *L->top = *em;
    incr_top;
    lua_pushstring(L, s);
    luaD_call(L, L->top-2, 0);
  }
}


/*
** Reports an error, and jumps up to the available recovery label
*/
LUA_API void lua_error (lua_State *L, const char *s) {
  if (s) message(L, s);
  luaD_breakrun(L, LUA_ERRRUN);
}


void luaD_breakrun (lua_State *L, int errcode) {
  if (L->errorJmp) {
    L->errorJmp->status = errcode;
    longjmp(L->errorJmp->b, 1);
  }
  else {
    if (errcode != LUA_ERRMEM)
      message(L, "unable to recover; exiting\n");
    exit(EXIT_FAILURE);
  }
}


int luaD_runprotected (lua_State *L, void (*f)(lua_State *, void *), void *ud) {
  StkId oldCbase = L->Cbase;
  StkId oldtop = L->top;
  struct lua_longjmp lj;
  int allowhooks = L->allowhooks;
  lj.status = 0;
  lj.previous = L->errorJmp;  /* chain new error handler */
  L->errorJmp = &lj;
  if (setjmp(lj.b) == 0)
    (*f)(L, ud);
  else {  /* an error occurred: restore the state */
    L->allowhooks = allowhooks;
    L->Cbase = oldCbase;
    L->top = oldtop;
    restore_stack_limit(L);
  }
  L->errorJmp = lj.previous;  /* restore old error handler */
  return lj.status;
}

/* }====================================================== */

/* resumed: mluxsys.c */
/* include: lfunc.c */
/*
** $Id: lfunc.c,v 1.34 2000/10/30 12:20:29 roberto Exp $
** Auxiliary functions to manipulate prototypes and closures
** See Copyright Notice in lua.h
*/


#include <stdlib.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */


#define sizeclosure(n)	((int)sizeof(Closure) + (int)sizeof(TObject)*((n)-1))


Closure *luaF_newclosure (lua_State *L, int nelems) {
  int size = sizeclosure(nelems);
  Closure *c = (Closure *)luaM_malloc(L, size);
  c->next = L->rootcl;
  L->rootcl = c;
  c->mark = c;
  c->nupvalues = nelems;
  L->nblocks += size;
  return c;
}


Proto *luaF_newproto (lua_State *L) {
  Proto *f = luaM_new(L, Proto);
  f->knum = NULL;
  f->nknum = 0;
  f->kstr = NULL;
  f->nkstr = 0;
  f->kproto = NULL;
  f->nkproto = 0;
  f->code = NULL;
  f->ncode = 0;
  f->numparams = 0;
  f->is_vararg = 0;
  f->maxstacksize = 0;
  f->marked = 0;
  f->lineinfo = NULL;
  f->nlineinfo = 0;
  f->nlocvars = 0;
  f->locvars = NULL;
  f->lineDefined = 0;
  f->source = NULL;
  f->next = L->rootproto;  /* chain in list of protos */
  L->rootproto = f;
  return f;
}


static size_t protosize (Proto *f) {
  return sizeof(Proto)
       + f->nknum*sizeof(Number)
       + f->nkstr*sizeof(TString *)
       + f->nkproto*sizeof(Proto *)
       + f->ncode*sizeof(Instruction)
       + f->nlocvars*sizeof(struct LocVar)
       + f->nlineinfo*sizeof(int);
}


void luaF_protook (lua_State *L, Proto *f, int pc) {
  f->ncode = pc;  /* signal that proto was properly created */
  L->nblocks += protosize(f);
}


void luaF_freeproto (lua_State *L, Proto *f) {
  if (f->ncode > 0)  /* function was properly created? */
    L->nblocks -= protosize(f);
  luaM_free(L, f->code);
  luaM_free(L, f->locvars);
  luaM_free(L, f->kstr);
  luaM_free(L, f->knum);
  luaM_free(L, f->kproto);
  luaM_free(L, f->lineinfo);
  luaM_free(L, f);
}


void luaF_freeclosure (lua_State *L, Closure *c) {
  L->nblocks -= sizeclosure(c->nupvalues);
  luaM_free(L, c);
}


/*
** Look for n-th local variable at line `line' in function `func'.
** Returns NULL if not found.
*/
const char *luaF_getlocalname (const Proto *f, int local_number, int pc) {
  int i;
  for (i = 0; i<f->nlocvars && f->locvars[i].startpc <= pc; i++) {
    if (pc < f->locvars[i].endpc) {  /* is variable active? */
      local_number--;
      if (local_number == 0)
        return f->locvars[i].varname->str;
    }
  }
  return NULL;  /* not found */
}

/* resumed: mluxsys.c */
/* include: lgc.c */
/*
** $Id: lgc.c,v 1.72 2000/10/26 12:47:05 roberto Exp $
** Garbage Collector
** See Copyright Notice in lua.h
*/

/* skipped: lua.h - see mluxsys.c */

/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lgc.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */


typedef struct GCState {
  Hash *tmark;  /* list of marked tables to be visited */
  Closure *cmark;  /* list of marked closures to be visited */
} GCState;



static void markobject (GCState *st, TObject *o);


/* mark a string; marks larger than 1 cannot be changed */
#define strmark(s)    {if ((s)->marked == 0) (s)->marked = 1;}



static void protomark (Proto *f) {
  if (!f->marked) {
    int i;
    f->marked = 1;
    strmark(f->source);
    for (i=0; i<f->nkstr; i++)
      strmark(f->kstr[i]);
    for (i=0; i<f->nkproto; i++)
      protomark(f->kproto[i]);
    for (i=0; i<f->nlocvars; i++)  /* mark local-variable names */
      strmark(f->locvars[i].varname);
  }
}


static void markstack (lua_State *L, GCState *st) {
  StkId o;
  for (o=L->stack; o<L->top; o++)
    markobject(st, o);
}


static void marklock (lua_State *L, GCState *st) {
  int i;
  for (i=0; i<L->refSize; i++) {
    if (L->refArray[i].st == LOCK)
      markobject(st, &L->refArray[i].o);
  }
}


static void markclosure (GCState *st, Closure *cl) {
  if (!ismarked(cl)) {
    if (!cl->isC)
      protomark(cl->f.l);
    cl->mark = st->cmark;  /* chain it for later traversal */
    st->cmark = cl;
  }
}


static void marktagmethods (lua_State *L, GCState *st) {
  int e;
  for (e=0; e<TM_N; e++) {
    int t;
    for (t=0; t<=L->last_tag; t++) {
      Closure *cl = luaT_gettm(L, t, e);
      if (cl) markclosure(st, cl);
    }
  }
}


static void markobject (GCState *st, TObject *o) {
  switch (ttype(o)) {
    case LUA_TUSERDATA:  case LUA_TSTRING:
      strmark(tsvalue(o));
      break;
    case LUA_TMARK:
      markclosure(st, infovalue(o)->func);
      break;
    case LUA_TFUNCTION:
      markclosure(st, clvalue(o));
      break;
    case LUA_TTABLE: {
      if (!ismarked(hvalue(o))) {
        hvalue(o)->mark = st->tmark;  /* chain it in list of marked */
        st->tmark = hvalue(o);
      }
      break;
    }
    default: break;  /* numbers, etc */
  }
}


static void markall (lua_State *L) {
  GCState st;
  st.cmark = NULL;
  st.tmark = L->gt;  /* put table of globals in mark list */
  L->gt->mark = NULL;
  marktagmethods(L, &st);  /* mark tag methods */
  markstack(L, &st); /* mark stack objects */
  marklock(L, &st); /* mark locked objects */
  for (;;) {  /* mark tables and closures */
    if (st.cmark) {
      int i;
      Closure *f = st.cmark;  /* get first closure from list */
      st.cmark = f->mark;  /* remove it from list */
      for (i=0; i<f->nupvalues; i++)  /* mark its upvalues */
        markobject(&st, &f->upvalue[i]);
    }
    else if (st.tmark) {
      int i;
      Hash *h = st.tmark;  /* get first table from list */
      st.tmark = h->mark;  /* remove it from list */
      for (i=0; i<h->size; i++) {
        Node *n = node(h, i);
        if (ttype(key(n)) != LUA_TNIL) {
          if (ttype(val(n)) == LUA_TNIL)
            luaH_remove(h, key(n));  /* dead element; try to remove it */
          markobject(&st, &n->key);
          markobject(&st, &n->val);
        }
      }
    }
    else break;  /* nothing else to mark */
  }
}


static int hasmark (const TObject *o) {
  /* valid only for locked objects */
  switch (o->ttype) {
    case LUA_TSTRING: case LUA_TUSERDATA:
      return tsvalue(o)->marked;
    case LUA_TTABLE:
      return ismarked(hvalue(o));
    case LUA_TFUNCTION:
      return ismarked(clvalue(o));
    default:  /* number */
      return 1;
  }
}


/* macro for internal debugging; check if a link of free refs is valid */
#define VALIDLINK(L, st,n)      (NONEXT <= (st) && (st) < (n))

static void invalidaterefs (lua_State *L) {
  int n = L->refSize;
  int i;
  for (i=0; i<n; i++) {
    struct Ref *r = &L->refArray[i];
    if (r->st == HOLD && !hasmark(&r->o))
      r->st = COLLECTED;
    LUA_ASSERT((r->st == LOCK && hasmark(&r->o)) ||
               (r->st == HOLD && hasmark(&r->o)) ||
                r->st == COLLECTED ||
                r->st == NONEXT ||
               (r->st < n && VALIDLINK(L, L->refArray[r->st].st, n)),
               "inconsistent ref table");
  }
  LUA_ASSERT(VALIDLINK(L, L->refFree, n), "inconsistent ref table");
}



static void collectproto (lua_State *L) {
  Proto **p = &L->rootproto;
  Proto *next;
  while ((next = *p) != NULL) {
    if (next->marked) {
      next->marked = 0;
      p = &next->next;
    }
    else {
      *p = next->next;
      luaF_freeproto(L, next);
    }
  }
}


static void collectclosure (lua_State *L) {
  Closure **p = &L->rootcl;
  Closure *next;
  while ((next = *p) != NULL) {
    if (ismarked(next)) {
      next->mark = next;  /* unmark */
      p = &next->next;
    }
    else {
      *p = next->next;
      luaF_freeclosure(L, next);
    }
  }
}


static void collecttable (lua_State *L) {
  Hash **p = &L->roottable;
  Hash *next;
  while ((next = *p) != NULL) {
    if (ismarked(next)) {
      next->mark = next;  /* unmark */
      p = &next->next;
    }
    else {
      *p = next->next;
      luaH_free(L, next);
    }
  }
}


static void checktab (lua_State *L, stringtable *tb) {
  if (tb->nuse < (lint32)(tb->size/4) && tb->size > 10)
    luaS_resize(L, tb, tb->size/2);  /* table is too big */
}


static void collectstrings (lua_State *L, int all) {
  int i;
  for (i=0; i<L->strt.size; i++) {  /* for each list */
    TString **p = &L->strt.hash[i];
    TString *next;
    while ((next = *p) != NULL) {
      if (next->marked && !all) {  /* preserve? */
        if (next->marked < FIXMARK)  /* does not change FIXMARKs */
          next->marked = 0;
        p = &next->nexthash;
      } 
      else {  /* collect */
        *p = next->nexthash;
        L->strt.nuse--;
        L->nblocks -= sizestring(next->len);
        luaM_free(L, next);
      }
    }
  }
  checktab(L, &L->strt);
}


static void collectudata (lua_State *L, int all) {
  int i;
  for (i=0; i<L->udt.size; i++) {  /* for each list */
    TString **p = &L->udt.hash[i];
    TString *next;
    while ((next = *p) != NULL) {
      LUA_ASSERT(next->marked <= 1, "udata cannot be fixed");
      if (next->marked && !all) {  /* preserve? */
        next->marked = 0;
        p = &next->nexthash;
      } 
      else {  /* collect */
        int tag = next->u.d.tag;
        *p = next->nexthash;
        next->nexthash = L->TMtable[tag].collected;  /* chain udata */
        L->TMtable[tag].collected = next;
        L->nblocks -= sizestring(next->len);
        L->udt.nuse--;
      }
    }
  }
  checktab(L, &L->udt);
}


#define MINBUFFER	256
static void checkMbuffer (lua_State *L) {
  if (L->Mbuffsize > MINBUFFER*2) {  /* is buffer too big? */
    size_t newsize = L->Mbuffsize/2;  /* still larger than MINBUFFER */
    L->nblocks += (newsize - L->Mbuffsize)*sizeof(char);
    L->Mbuffsize = newsize;
    luaM_reallocvector(L, L->Mbuffer, newsize, char);
  }
}


static void callgcTM (lua_State *L, const TObject *o) {
  Closure *tm = luaT_gettmbyObj(L, o, TM_GC);
  if (tm != NULL) {
    int oldah = L->allowhooks;
    L->allowhooks = 0;  /* stop debug hooks during GC tag methods */
    luaD_checkstack(L, 2);
    clvalue(L->top) = tm;
    ttype(L->top) = LUA_TFUNCTION;
    *(L->top+1) = *o;
    L->top += 2;
    luaD_call(L, L->top-2, 0);
    L->allowhooks = oldah;  /* restore hooks */
  }
}


static void callgcTMudata (lua_State *L) {
  int tag;
  TObject o;
  ttype(&o) = LUA_TUSERDATA;
  L->GCthreshold = 2*L->nblocks;  /* avoid GC during tag methods */
  for (tag=L->last_tag; tag>=0; tag--) {  /* for each tag (in reverse order) */
    TString *udata;
    while ((udata = L->TMtable[tag].collected) != NULL) {
      L->TMtable[tag].collected = udata->nexthash;  /* remove it from list */
      tsvalue(&o) = udata;
      callgcTM(L, &o);
      luaM_free(L, udata);
    }
  }
}


void luaC_collect (lua_State *L, int all) {
  collectudata(L, all);
  callgcTMudata(L);
  collectstrings(L, all);
  collecttable(L);
  collectproto(L);
  collectclosure(L);
}


static void luaC_collectgarbage (lua_State *L) {
  markall(L);
  invalidaterefs(L);  /* check unlocked references */
  luaC_collect(L, 0);
  checkMbuffer(L);
  L->GCthreshold = 2*L->nblocks;  /* set new threshold */
  callgcTM(L, &luaO_nilobject);
}


void luaC_checkGC (lua_State *L) {
  if (L->nblocks >= L->GCthreshold)
    luaC_collectgarbage(L);
}

/* resumed: mluxsys.c */

#ifdef NOPARSER
void luaX_init(lua_State *L) {
  UNUSED(L);
}
#define MAXSRC          80
void luaX_syntaxerror (LexState *ls, const char *s, const char *token) {
  char buff[MAXSRC];
  luaO_chunkid(buff, ls->source->str, sizeof(buff));
  luaO_verror(ls->L, "%.99s;\n  last token read: `%.30s' at line %d in %.80s",
	  s, token, ls->linenumber, buff);
}
void luaX_error (LexState *ls, const char *s, int token) {
  UNUSED(token);
  luaX_syntaxerror(ls, s, ls->L->Mbuffer);
}                                                                               
#else
/* include: llex.c */
/*
** $Id: llex.c,v 1.72 2000/10/20 16:39:03 roberto Exp $
** Lexical Analyzer
** See Copyright Notice in lua.h
*/


#include <ctype.h>
#include <stdio.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: llex.h - see lua-4.0/src/lcode.h */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lparser.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: luadebug.h - see mluxsys.c */
/* skipped: lzio.h - see lua-4.0/src/llex.h */



#define llex_next(LS) (LS->current = zgetc(LS->z))



/* ORDER RESERVED */
static const char *const token2string [] = {
    "and", "break", "do", "else", "elseif", "end", "for",
    "function", "if", "local", "nil", "not", "or", "repeat", "return", "then",
    "until", "while", "", "..", "...", "==", ">=", "<=", "~=", "", "", "<eof>"};


void luaX_init (lua_State *L) {
  int i;
  for (i=0; i<NUM_RESERVED; i++) {
    TString *ts = luaS_new(L, token2string[i]);
    ts->marked = (unsigned char)(RESERVEDMARK+i);  /* reserved word */
  }
}


#define MAXSRC          80


void luaX_checklimit (LexState *ls, int val, int limit, const char *msg) {
  if (val > limit) {
    char buff[100];
    sprintf(buff, "too many %.50s (limit=%d)", msg, limit);
    luaX_error(ls, buff, ls->t.token);
  }
}


void luaX_syntaxerror (LexState *ls, const char *s, const char *token) {
  char buff[MAXSRC];
  luaO_chunkid(buff, ls->source->str, sizeof(buff));
  luaO_verror(ls->L, "%.99s;\n  last token read: `%.30s' at line %d in %.80s",
              s, token, ls->linenumber, buff);
}


void luaX_error (LexState *ls, const char *s, int token) {
  char buff[TOKEN_LEN];
  luaX_token2str(token, buff);
  if (buff[0] == '\0')
    luaX_syntaxerror(ls, s, ls->L->Mbuffer);
  else
    luaX_syntaxerror(ls, s, buff);
}


void luaX_token2str (int token, char *s) {
  if (token < 256) {
    s[0] = (char)token;
    s[1] = '\0';
  }
  else
    strcpy(s, token2string[token-FIRST_RESERVED]);
}


static void luaX_invalidchar (LexState *ls, int c) {
  char buff[8];
  sprintf(buff, "0x%02X", c);
  luaX_syntaxerror(ls, "invalid control char", buff);
}


static void inclinenumber (LexState *LS) {
  llex_next(LS);  /* skip '\n' */
  ++LS->linenumber;
  luaX_checklimit(LS, LS->linenumber, MAX_INT, "lines in a chunk");
}


void luaX_setinput (lua_State *L, LexState *LS, ZIO *z, TString *source) {
  LS->L = L;
  LS->lookahead.token = TK_EOS;  /* no look-ahead token */
  LS->z = z;
  LS->fs = NULL;
  LS->linenumber = 1;
  LS->lastline = 1;
  LS->source = source;
  llex_next(LS);  /* read first char */
  if (LS->current == '#') {
    do {  /* skip first line */
      llex_next(LS);
    } while (LS->current != '\n' && LS->current != EOZ);
  }
}



/*
** =======================================================
** LEXICAL ANALYZER
** =======================================================
*/


/* use Mbuffer to store names, literal strings and numbers */

#define EXTRABUFF	128
#define checkbuffer(L, n, len)	if ((len)+(n) > L->Mbuffsize) \
                                  luaO_openspace(L, (len)+(n)+EXTRABUFF)

#define save(L, c, l)	(L->Mbuffer[l++] = (char)c)
#define save_and_next(L, LS, l)  (save(L, LS->current, l), llex_next(LS))


static const char *readname (LexState *LS) {
  lua_State *L = LS->L;
  size_t l = 0;
  checkbuffer(L, 10, l);
  do {
    checkbuffer(L, 10, l);
    save_and_next(L, LS, l);
  } while (isalnum(LS->current) || LS->current == '_');
  save(L, '\0', l);
  return L->Mbuffer;
}


/* LUA_NUMBER */
static void llex_read_number (LexState *LS, int comma, SemInfo *seminfo) {
  lua_State *L = LS->L;
  size_t l = 0;
  checkbuffer(L, 10, l);
  if (comma) save(L, '.', l);
  while (isdigit(LS->current)) {
    checkbuffer(L, 10, l);
    save_and_next(L, LS, l);
  }
  if (LS->current == '.') {
    save_and_next(L, LS, l);
    if (LS->current == '.') {
      save_and_next(L, LS, l);
      save(L, '\0', l);
      luaX_error(LS, "ambiguous syntax"
           " (decimal point x string concatenation)", TK_NUMBER);
    }
  }
  while (isdigit(LS->current)) {
    checkbuffer(L, 10, l);
    save_and_next(L, LS, l);
  }
  if (LS->current == 'e' || LS->current == 'E') {
    save_and_next(L, LS, l);  /* read 'E' */
    if (LS->current == '+' || LS->current == '-')
      save_and_next(L, LS, l);  /* optional exponent sign */
    while (isdigit(LS->current)) {
      checkbuffer(L, 10, l);
      save_and_next(L, LS, l);
    }
  }
  save(L, '\0', l);
  if (!luaO_str2d(L->Mbuffer, &seminfo->r))
    luaX_error(LS, "malformed number", TK_NUMBER);
}


static void read_long_string (LexState *LS, SemInfo *seminfo) {
  lua_State *L = LS->L;
  int cont = 0;
  size_t l = 0;
  checkbuffer(L, 10, l);
  save(L, '[', l);  /* save first '[' */
  save_and_next(L, LS, l);  /* pass the second '[' */
  for (;;) {
    checkbuffer(L, 10, l);
    switch (LS->current) {
      case EOZ:
        save(L, '\0', l);
        luaX_error(LS, "unfinished long string", TK_STRING);
        break;  /* to avoid warnings */
      case '[':
        save_and_next(L, LS, l);
        if (LS->current == '[') {
          cont++;
          save_and_next(L, LS, l);
        }
        continue;
      case ']':
        save_and_next(L, LS, l);
        if (LS->current == ']') {
          if (cont == 0) goto endloop;
          cont--;
          save_and_next(L, LS, l);
        }
        continue;
      case '\n':
        save(L, '\n', l);
        inclinenumber(LS);
        continue;
      default:
        save_and_next(L, LS, l);
    }
  } endloop:
  save_and_next(L, LS, l);  /* skip the second ']' */
  save(L, '\0', l);
  seminfo->ts = luaS_newlstr(L, L->Mbuffer+2, l-5);
}


static void read_string (LexState *LS, int del, SemInfo *seminfo) {
  lua_State *L = LS->L;
  size_t l = 0;
  checkbuffer(L, 10, l);
  save_and_next(L, LS, l);
  while (LS->current != del) {
    checkbuffer(L, 10, l);
    switch (LS->current) {
      case EOZ:  case '\n':
        save(L, '\0', l);
        luaX_error(LS, "unfinished string", TK_STRING);
        break;  /* to avoid warnings */
      case '\\':
        llex_next(LS);  /* do not save the '\' */
        switch (LS->current) {
          case 'a': save(L, '\a', l); llex_next(LS); break;
          case 'b': save(L, '\b', l); llex_next(LS); break;
          case 'f': save(L, '\f', l); llex_next(LS); break;
          case 'n': save(L, '\n', l); llex_next(LS); break;
          case 'r': save(L, '\r', l); llex_next(LS); break;
          case 't': save(L, '\t', l); llex_next(LS); break;
          case 'v': save(L, '\v', l); llex_next(LS); break;
          case '\n': save(L, '\n', l); inclinenumber(LS); break;
          case '0': case '1': case '2': case '3': case '4':
          case '5': case '6': case '7': case '8': case '9': {
            int c = 0;
            int i = 0;
            do {
              c = 10*c + (LS->current-'0');
              llex_next(LS);
            } while (++i<3 && isdigit(LS->current));
            if (c != (unsigned char)c) {
              save(L, '\0', l);
              luaX_error(LS, "escape sequence too large", TK_STRING);
            }
            save(L, c, l);
            break;
          }
          default:  /* handles \\, \", \', and \? */
            save_and_next(L, LS, l);
        }
        break;
      default:
        save_and_next(L, LS, l);
    }
  }
  save_and_next(L, LS, l);  /* skip delimiter */
  save(L, '\0', l);
  seminfo->ts = luaS_newlstr(L, L->Mbuffer+1, l-3);
}


int luaX_lex (LexState *LS, SemInfo *seminfo) {
  for (;;) {
    switch (LS->current) {

      case ' ': case '\t': case '\r':  /* `\r' to avoid problems with DOS */
        llex_next(LS);
        continue;

      case '\n':
        inclinenumber(LS);
        continue;

      case '$':
        luaX_error(LS, "unexpected `$' (pragmas are no longer supported)", '$');
        break;

      case '-':
        llex_next(LS);
        if (LS->current != '-') return '-';
        do { llex_next(LS); } while (LS->current != '\n' && LS->current != EOZ);
        continue;

      case '[':
        llex_next(LS);
        if (LS->current != '[') return '[';
        else {
          read_long_string(LS, seminfo);
          return TK_STRING;
        }

      case '=':
        llex_next(LS);
        if (LS->current != '=') return '=';
        else { llex_next(LS); return TK_EQ; }

      case '<':
        llex_next(LS);
        if (LS->current != '=') return '<';
        else { llex_next(LS); return TK_LE; }

      case '>':
        llex_next(LS);
        if (LS->current != '=') return '>';
        else { llex_next(LS); return TK_GE; }

      case '~':
        llex_next(LS);
        if (LS->current != '=') return '~';
        else { llex_next(LS); return TK_NE; }

      case '"':
      case '\'':
        read_string(LS, LS->current, seminfo);
        return TK_STRING;

      case '.':
        llex_next(LS);
        if (LS->current == '.') {
          llex_next(LS);
          if (LS->current == '.') {
            llex_next(LS);
            return TK_DOTS;   /* ... */
          }
          else return TK_CONCAT;   /* .. */
        }
        else if (!isdigit(LS->current)) return '.';
        else {
          llex_read_number(LS, 1, seminfo);
          return TK_NUMBER;
        }

      case '0': case '1': case '2': case '3': case '4':
      case '5': case '6': case '7': case '8': case '9':
        llex_read_number(LS, 0, seminfo);
        return TK_NUMBER;

      case EOZ:
        return TK_EOS;

      case '_': goto tname;

      default:
        if (!isalpha(LS->current)) {
          int c = LS->current;
          if (iscntrl(c))
            luaX_invalidchar(LS, c);
          llex_next(LS);
          return c;
        }
        tname: {  /* identifier or reserved word */
          TString *ts = luaS_new(LS->L, readname(LS));
          if (ts->marked >= RESERVEDMARK)  /* reserved word? */
            return ts->marked-RESERVEDMARK+FIRST_RESERVED;
          seminfo->ts = ts;
          return TK_NAME;
        }
    }
  }
}

/* resumed: mluxsys.c */
#endif

/* include: lmem.c */
/*
** $Id: lmem.c,v 1.39 2000/10/30 16:29:59 roberto Exp $
** Interface to Memory Manager
** See Copyright Notice in lua.h
*/


#include <stdlib.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */




#ifdef LUA_DEBUG
/*
** {======================================================================
** Controlled version for realloc.
** =======================================================================
*/


#include <assert.h>
#include <limits.h>
#include <string.h>

#define realloc(b, s)	debug_realloc(b, s)
#define malloc(b)	debug_realloc(NULL, b)
#define free(b)		debug_realloc(b, 0)


/* ensures maximum alignment for HEADER */
#define HEADER	(sizeof(union L_Umaxalign))

#define MARKSIZE	16
#define MARK		0x55  /* 01010101 (a nice pattern) */


#define blocksize(b)	((unsigned long *)((char *)(b) - HEADER))

unsigned long memdebug_numblocks = 0;
unsigned long memdebug_total = 0;
unsigned long memdebug_maxmem = 0;
unsigned long memdebug_memlimit = LONG_MAX;


static void *checkblock (void *block) {
  unsigned long *b = blocksize(block);
  unsigned long size = *b;
  int i;
  for (i=0;i<MARKSIZE;i++)
    assert(*(((char *)b)+HEADER+size+i) == MARK+i);  /* corrupted block? */
  memdebug_numblocks--;
  memdebug_total -= size;
  return b;
}


static void freeblock (void *block) {
  if (block) {
    size_t size = *blocksize(block);
    block = checkblock(block);
    memset(block, -1, size+HEADER+MARKSIZE);  /* erase block */
    (free)(block);  /* free original block */
  }
}


static void *debug_realloc (void *block, size_t size) {
  if (size == 0) {
    freeblock(block);
    return NULL;
  }
  else if (memdebug_total+size > memdebug_memlimit)
    return NULL;  /* to test memory allocation errors */
  else {
    size_t realsize = HEADER+size+MARKSIZE;
    char *newblock = (char *)(malloc)(realsize);  /* alloc a new block */
    int i;
    if (realsize < size) return NULL;  /* overflow! */
    if (newblock == NULL) return NULL;
    if (block) {
      size_t oldsize = *blocksize(block);
      if (oldsize > size) oldsize = size;
      memcpy(newblock+HEADER, block, oldsize);
      freeblock(block);  /* erase (and check) old copy */
    }
    memdebug_total += size;
    if (memdebug_total > memdebug_maxmem) memdebug_maxmem = memdebug_total;
    memdebug_numblocks++;
    *(unsigned long *)newblock = size;
    for (i=0;i<MARKSIZE;i++)
      *(newblock+HEADER+size+i) = (char)(MARK+i);
    return newblock+HEADER;
  }
}


/* }====================================================================== */
#endif



/*
** Real ISO (ANSI) systems do not need these tests;
** but some systems (Sun OS) are not that ISO...
*/
#ifdef OLD_ANSI
#define realloc(b,s)	((b) == NULL ? malloc(s) : (realloc)(b, s))
#define free(b)		if (b) (free)(b)
#endif


void *luaM_growaux (lua_State *L, void *block, size_t nelems,
               int inc, size_t size, const char *errormsg, size_t limit) {
  size_t newn = nelems+inc;
  if (nelems >= limit-inc) lua_error(L, errormsg);
  if ((newn ^ nelems) <= nelems ||  /* still the same power-of-2 limit? */
       (nelems > 0 && newn < MINPOWER2))  /* or block already is MINPOWER2? */
      return block;  /* do not need to reallocate */
  else  /* it crossed a power-of-2 boundary; grow to next power */
    return luaM_realloc(L, block, luaO_power2(newn)*size);
}


/*
** generic allocation routine.
*/
void *luaM_realloc (lua_State *L, void *block, lint32 size) {
  if (size == 0) {
    free(block);  /* block may be NULL; that is OK for free */
    return NULL;
  }
  else if (size >= MAX_SIZET)
    lua_error(L, "memory allocation error: block too big");
  block = realloc(block, size);
  if (block == NULL) {
    if (L)
      luaD_breakrun(L, LUA_ERRMEM);  /* break run without error message */
    else return NULL;  /* error before creating state! */
  }
  return block;
}


/* resumed: mluxsys.c */
/* include: lobject.c */
/*
** $Id: lobject.c,v 1.55 2000/10/20 16:36:32 roberto Exp $
** Some generic functions over Lua objects
** See Copyright Notice in lua.h
*/

#include <ctype.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */



const TObject luaO_nilobject = {LUA_TNIL, {NULL}};


const char *const luaO_typenames[] = {
  "userdata", "nil", "number", "string", "table", "function"
};



/*
** returns smaller power of 2 larger than `n' (minimum is MINPOWER2) 
*/
lint32 luaO_power2 (lint32 n) {
  lint32 p = MINPOWER2;
  while (p<=n) p<<=1;
  return p;
}


int luaO_equalObj (const TObject *t1, const TObject *t2) {
  if (ttype(t1) != ttype(t2)) return 0;
  switch (ttype(t1)) {
    case LUA_TNUMBER:
      return nvalue(t1) == nvalue(t2);
    case LUA_TSTRING: case LUA_TUSERDATA:
      return tsvalue(t1) == tsvalue(t2);
    case LUA_TTABLE: 
      return hvalue(t1) == hvalue(t2);
    case LUA_TFUNCTION:
      return clvalue(t1) == clvalue(t2);
    default:
      LUA_ASSERT(ttype(t1) == LUA_TNIL, "invalid type");
      return 1; /* LUA_TNIL */
  }
}


char *luaO_openspace (lua_State *L, size_t n) {
  if (n > L->Mbuffsize) {
    luaM_reallocvector(L, L->Mbuffer, n, char);
    L->nblocks += (n - L->Mbuffsize)*sizeof(char);
    L->Mbuffsize = n;
  }
  return L->Mbuffer;
}


int luaO_str2d (const char *s, Number *result) {  /* LUA_NUMBER */
  char *endptr;
  Number res = lua_str2number(s, &endptr);
  if (endptr == s) return 0;  /* no conversion */
  while (isspace((unsigned char)*endptr)) endptr++;
  if (*endptr != '\0') return 0;  /* invalid trailing characters? */
  *result = res;
  return 1;
}


/* maximum length of a string format for `luaO_verror' */
#define MAX_VERROR	280

/* this function needs to handle only '%d' and '%.XXs' formats */
void luaO_verror (lua_State *L, const char *fmt, ...) {
  va_list argp;
  char buff[MAX_VERROR];  /* to hold formatted message */
  va_start(argp, fmt);
  vsprintf(buff, fmt, argp);
  va_end(argp);
  lua_error(L, buff);
}


void luaO_chunkid (char *out, const char *source, int bufflen) {
  if (*source == '=') {
    strncpy(out, source+1, bufflen);  /* remove first char */
    out[bufflen-1] = '\0';  /* ensures null termination */
  }
  else {
    if (*source == '@') {
      int l;
      source++;  /* skip the `@' */
      bufflen -= sizeof("file `...%s'");
      l = strlen(source);
      if (l>bufflen) {
        source += (l-bufflen);  /* get last part of file name */
        sprintf(out, "file `...%.99s'", source);
      }
      else
        sprintf(out, "file `%.99s'", source);
    }
    else {
      int len = strcspn(source, "\n");  /* stop at first newline */
      bufflen -= sizeof("string \"%.*s...\"");
      if (len > bufflen) len = bufflen;
      if (source[len] != '\0') {  /* must truncate? */
        strcpy(out, "string \"");
        out += strlen(out);
        strncpy(out, source, len);
        strcpy(out+len, "...\"");
      }
      else
        sprintf(out, "string \"%.99s\"", source);
    }
  }
}
/* resumed: mluxsys.c */

#ifdef NOPARSER
Proto *luaY_parser(lua_State *L, ZIO *z) {
  UNUSED(z);
  lua_error(L,"parser not loaded");
  return NULL;
}
#else
/* include: lparser.c */
/*
** $Id: lparser.c,v 1.116 2000/10/27 11:39:52 roberto Exp $
** LL(1) Parser and code generator for Lua
** See Copyright Notice in lua.h
*/


#include <stdio.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lcode.h - see lua-4.0/src/lcode.c */
/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: llex.h - see lua-4.0/src/lcode.h */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lparser.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */


/*
** Constructors descriptor:
** `n' indicates number of elements, and `k' signals whether
** it is a list constructor (k = 0) or a record constructor (k = 1)
** or empty (k = ';' or '}')
*/
typedef struct Constdesc {
  int n;
  int k;
} Constdesc;


typedef struct Breaklabel {
  struct Breaklabel *previous;  /* chain */
  int breaklist;
  int stacklevel;
} Breaklabel;




/*
** prototypes for recursive non-terminal functions
*/
static void body (LexState *ls, int needself, int line);
static void chunk (LexState *ls);
static void constructor (LexState *ls);
static void expr (LexState *ls, expdesc *v);
static void exp1 (LexState *ls);



static void next (LexState *ls) {
  ls->lastline = ls->linenumber;
  if (ls->lookahead.token != TK_EOS) {  /* is there a look-ahead token? */
    ls->t = ls->lookahead;  /* use this one */
    ls->lookahead.token = TK_EOS;  /* and discharge it */
  }
  else
    ls->t.token = luaX_lex(ls, &ls->t.seminfo);  /* read next token */
}


static void lookahead (LexState *ls) {
  LUA_ASSERT(ls->lookahead.token == TK_EOS, "two look-aheads");
  ls->lookahead.token = luaX_lex(ls, &ls->lookahead.seminfo);
}


static void error_expected (LexState *ls, int token) {
  char buff[100], t[TOKEN_LEN];
  luaX_token2str(token, t);
  sprintf(buff, "`%.20s' expected", t);
  luaK_error(ls, buff);
}


static void check (LexState *ls, int c) {
  if (ls->t.token != c)
    error_expected(ls, c);
  next(ls);
}


static void check_condition (LexState *ls, int c, const char *msg) {
  if (!c) luaK_error(ls, msg);
}


static int optional (LexState *ls, int c) {
  if (ls->t.token == c) {
    next(ls);
    return 1;
  }
  else return 0;
}


static void check_match (LexState *ls, int what, int who, int where) {
  if (ls->t.token != what) {
    if (where == ls->linenumber)
      error_expected(ls, what);
    else {
      char buff[100];
      char t_what[TOKEN_LEN], t_who[TOKEN_LEN];
      luaX_token2str(what, t_what);
      luaX_token2str(who, t_who);
      sprintf(buff, "`%.20s' expected (to close `%.20s' at line %d)",
              t_what, t_who, where);
      luaK_error(ls, buff);
    }
  }
  next(ls);
}


static int string_constant (FuncState *fs, TString *s) {
  Proto *f = fs->f;
  int c = s->u.s.constindex;
  if (c >= f->nkstr || f->kstr[c] != s) {
    luaM_growvector(fs->L, f->kstr, f->nkstr, 1, TString *,
                    "constant table overflow", MAXARG_U);
    c = f->nkstr++;
    f->kstr[c] = s;
    s->u.s.constindex = c;  /* hint for next time */
  }
  return c;
}


static void code_string (LexState *ls, TString *s) {
  luaK_kstr(ls, string_constant(ls->fs, s));
}


static TString *str_checkname (LexState *ls) {
  TString *ts;
  check_condition(ls, (ls->t.token == TK_NAME), "<name> expected");
  ts = ls->t.seminfo.ts;
  next(ls);
  return ts;
}


static int checkname (LexState *ls) {
  return string_constant(ls->fs, str_checkname(ls));
}


static int luaI_registerlocalvar (LexState *ls, TString *varname) {
  Proto *f = ls->fs->f;
  luaM_growvector(ls->L, f->locvars, f->nlocvars, 1, LocVar, "", MAX_INT);
  f->locvars[f->nlocvars].varname = varname;
  return f->nlocvars++;
}


static void new_localvar (LexState *ls, TString *name, int n) {
  FuncState *fs = ls->fs;
  luaX_checklimit(ls, fs->nactloc+n+1, MAXLOCALS, "local variables");
  fs->actloc[fs->nactloc+n] = luaI_registerlocalvar(ls, name);
}


static void adjustlocalvars (LexState *ls, int nvars) {
  FuncState *fs = ls->fs;
  while (nvars--)
    fs->f->locvars[fs->actloc[fs->nactloc++]].startpc = fs->pc;
}


static void removelocalvars (LexState *ls, int nvars) {
  FuncState *fs = ls->fs;
  while (nvars--)
    fs->f->locvars[fs->actloc[--fs->nactloc]].endpc = fs->pc;
}


static void new_localvarstr (LexState *ls, const char *name, int n) {
  new_localvar(ls, luaS_newfixed(ls->L, name), n);
}


static int search_local (LexState *ls, TString *n, expdesc *var) {
  FuncState *fs;
  int level = 0;
  for (fs=ls->fs; fs; fs=fs->prev) {
    int i;
    for (i=fs->nactloc-1; i >= 0; i--) {
      if (n == fs->f->locvars[fs->actloc[i]].varname) {
        var->k = VLOCAL;
        var->u.index = i;
        return level;
      }
    }
    level++;  /* `var' not found; check outer level */
  }
  var->k = VGLOBAL;  /* not found in any level; must be global */
  return -1;
}


static void singlevar (LexState *ls, TString *n, expdesc *var) {
  int level = search_local(ls, n, var);
  if (level >= 1)  /* neither local (0) nor global (-1)? */
    luaX_syntaxerror(ls, "cannot access a variable in outer scope", n->str);
  else if (level == -1)  /* global? */
    var->u.index = string_constant(ls->fs, n);
}


static int indexupvalue (LexState *ls, expdesc *v) {
  FuncState *fs = ls->fs;
  int i;
  for (i=0; i<fs->nupvalues; i++) {
    if (fs->upvalues[i].k == v->k && fs->upvalues[i].u.index == v->u.index)
      return i;
  }
  /* new one */
  luaX_checklimit(ls, fs->nupvalues+1, MAXUPVALUES, "upvalues");
  fs->upvalues[fs->nupvalues] = *v;
  return fs->nupvalues++;
}


static void pushupvalue (LexState *ls, TString *n) {
  FuncState *fs = ls->fs;
  expdesc v;
  int level = search_local(ls, n, &v);
  if (level == -1) {  /* global? */
    if (fs->prev == NULL)
      luaX_syntaxerror(ls, "cannot access upvalue in main", n->str);
    v.u.index = string_constant(fs->prev, n);
  }
  else if (level != 1)
    luaX_syntaxerror(ls,
         "upvalue must be global or local to immediately outer scope", n->str);
  luaK_code1(fs, OP_PUSHUPVALUE, indexupvalue(ls, &v));
}


static void adjust_mult_assign (LexState *ls, int nvars, int nexps) {
  FuncState *fs = ls->fs;
  int diff = nexps - nvars;
  if (nexps > 0 && luaK_lastisopen(fs)) { /* list ends in a function call */
    diff--;  /* do not count function call itself */
    if (diff <= 0) {  /* more variables than values? */
      luaK_setcallreturns(fs, -diff);  /* function call provide extra values */
      diff = 0;  /* no more difference */
    }
    else  /* more values than variables */
      luaK_setcallreturns(fs, 0);  /* call should provide no value */
  }
  /* push or pop eventual difference between list lengths */
  luaK_adjuststack(fs, diff);
}


static void code_params (LexState *ls, int nparams, int dots) {
  FuncState *fs = ls->fs;
  adjustlocalvars(ls, nparams);
  luaX_checklimit(ls, fs->nactloc, MAXPARAMS, "parameters");
  fs->f->numparams = fs->nactloc;  /* `self' could be there already */
  fs->f->is_vararg = dots;
  if (dots) {
    new_localvarstr(ls, "arg", 0);
    adjustlocalvars(ls, 1);
  }
  luaK_deltastack(fs, fs->nactloc);  /* count parameters in the stack */
}


static void enterbreak (FuncState *fs, Breaklabel *bl) {
  bl->stacklevel = fs->stacklevel;
  bl->breaklist = NO_JUMP;
  bl->previous = fs->bl;
  fs->bl = bl;
}


static void leavebreak (FuncState *fs, Breaklabel *bl) {
  fs->bl = bl->previous;
  LUA_ASSERT(bl->stacklevel == fs->stacklevel, "wrong levels");
  luaK_patchlist(fs, bl->breaklist, luaK_getlabel(fs));
}


static void pushclosure (LexState *ls, FuncState *func) {
  FuncState *fs = ls->fs;
  Proto *f = fs->f;
  int i;
  for (i=0; i<func->nupvalues; i++)
    luaK_tostack(ls, &func->upvalues[i], 1);
  luaM_growvector(ls->L, f->kproto, f->nkproto, 1, Proto *,
                  "constant table overflow", MAXARG_A);
  f->kproto[f->nkproto++] = func->f;
  luaK_code2(fs, OP_CLOSURE, f->nkproto-1, func->nupvalues);
}


static void open_func (LexState *ls, FuncState *fs) {
  Proto *f = luaF_newproto(ls->L);
  fs->prev = ls->fs;  /* linked list of funcstates */
  fs->ls = ls;
  fs->L = ls->L;
  ls->fs = fs;
  fs->stacklevel = 0;
  fs->nactloc = 0;
  fs->nupvalues = 0;
  fs->bl = NULL;
  fs->f = f;
  f->source = ls->source;
  fs->pc = 0;
  fs->lasttarget = 0;
  fs->lastline = 0;
  fs->jlt = NO_JUMP;
  f->code = NULL;
  f->maxstacksize = 0;
  f->numparams = 0;  /* default for main chunk */
  f->is_vararg = 0;  /* default for main chunk */
}


static void close_func (LexState *ls) {
  lua_State *L = ls->L;
  FuncState *fs = ls->fs;
  Proto *f = fs->f;
  luaK_code0(fs, OP_END);
  luaK_getlabel(fs);  /* close eventual list of pending jumps */
  luaM_reallocvector(L, f->code, fs->pc, Instruction);
  luaM_reallocvector(L, f->kstr, f->nkstr, TString *);
  luaM_reallocvector(L, f->knum, f->nknum, Number);
  luaM_reallocvector(L, f->kproto, f->nkproto, Proto *);
  removelocalvars(ls, fs->nactloc);
  luaM_reallocvector(L, f->locvars, f->nlocvars, LocVar);
  luaM_reallocvector(L, f->lineinfo, f->nlineinfo+1, int);
  f->lineinfo[f->nlineinfo++] = MAX_INT;  /* end flag */
  luaF_protook(L, f, fs->pc);  /* proto is ok now */
  ls->fs = fs->prev;
  LUA_ASSERT(fs->bl == NULL, "wrong list end");
}


Proto *luaY_parser (lua_State *L, ZIO *z) {
  struct LexState lexstate;
  struct FuncState funcstate;
  luaX_setinput(L, &lexstate, z, luaS_new(L, zname(z)));
  open_func(&lexstate, &funcstate);
  next(&lexstate);  /* read first token */
  chunk(&lexstate);
  check_condition(&lexstate, (lexstate.t.token == TK_EOS), "<eof> expected");
  close_func(&lexstate);
  LUA_ASSERT(funcstate.prev == NULL, "wrong list end");
  LUA_ASSERT(funcstate.nupvalues == 0, "no upvalues in main");
  return funcstate.f;
}



/*============================================================*/
/* GRAMMAR RULES */
/*============================================================*/


static int explist1 (LexState *ls) {
  /* explist1 -> expr { ',' expr } */
  int n = 1;  /* at least one expression */
  expdesc v;
  expr(ls, &v);
  while (ls->t.token == ',') {
    luaK_tostack(ls, &v, 1);  /* gets only 1 value from previous expression */
    next(ls);  /* skip comma */
    expr(ls, &v);
    n++;
  }
  luaK_tostack(ls, &v, 0);  /* keep open number of values of last expression */
  return n;
}


static void funcargs (LexState *ls, int slf) {
  FuncState *fs = ls->fs;
  int slevel = fs->stacklevel - slf - 1;  /* where is func in the stack */
  switch (ls->t.token) {
    case '(': {  /* funcargs -> '(' [ explist1 ] ')' */
      int line = ls->linenumber;
      int nargs = 0;
      next(ls);
      if (ls->t.token != ')')  /* arg list not empty? */
        nargs = explist1(ls);
      check_match(ls, ')', '(', line);
#ifdef LUA_COMPAT_ARGRET
      if (nargs > 0)  /* arg list is not empty? */
        luaK_setcallreturns(fs, 1);  /* last call returns only 1 value */
#else
      UNUSED(nargs);  /* to avoid warnings */
#endif
      break;
    }
    case '{': {  /* funcargs -> constructor */
      constructor(ls);
      break;
    }
    case TK_STRING: {  /* funcargs -> STRING */
      code_string(ls, ls->t.seminfo.ts);  /* must use `seminfo' before `next' */
      next(ls);
      break;
    }
    default: {
      luaK_error(ls, "function arguments expected");
      break;
    }
  }
  fs->stacklevel = slevel;  /* call will remove function and arguments */
  luaK_code2(fs, OP_CALL, slevel, MULT_RET);
}


static void var_or_func_tail (LexState *ls, expdesc *v) {
  for (;;) {
    switch (ls->t.token) {
      case '.': {  /* var_or_func_tail -> '.' NAME */
        next(ls);
        luaK_tostack(ls, v, 1);  /* `v' must be on stack */
        luaK_kstr(ls, checkname(ls));
        v->k = VINDEXED;
        break;
      }
      case '[': {  /* var_or_func_tail -> '[' exp1 ']' */
        next(ls);
        luaK_tostack(ls, v, 1);  /* `v' must be on stack */
        v->k = VINDEXED;
        exp1(ls);
        check(ls, ']');
        break;
      }
      case ':': {  /* var_or_func_tail -> ':' NAME funcargs */
        int name;
        next(ls);
        name = checkname(ls);
        luaK_tostack(ls, v, 1);  /* `v' must be on stack */
        luaK_code1(ls->fs, OP_PUSHSELF, name);
        funcargs(ls, 1);
        v->k = VEXP;
        v->u.l.t = v->u.l.f = NO_JUMP;
        break;
      }
      case '(': case TK_STRING: case '{': {  /* var_or_func_tail -> funcargs */
        luaK_tostack(ls, v, 1);  /* `v' must be on stack */
        funcargs(ls, 0);
        v->k = VEXP;
        v->u.l.t = v->u.l.f = NO_JUMP;
        break;
      }
      default: return;  /* should be follow... */
    }
  }
}


static void var_or_func (LexState *ls, expdesc *v) {
  /* var_or_func -> ['%'] NAME var_or_func_tail */
  if (optional(ls, '%')) {  /* upvalue? */
    pushupvalue(ls, str_checkname(ls));
    v->k = VEXP;
    v->u.l.t = v->u.l.f = NO_JUMP;
  }
  else  /* variable name */
    singlevar(ls, str_checkname(ls), v);
  var_or_func_tail(ls, v);
}



/*
** {======================================================================
** Rules for Constructors
** =======================================================================
*/


static void recfield (LexState *ls) {
  /* recfield -> (NAME | '['exp1']') = exp1 */
  switch (ls->t.token) {
    case TK_NAME: {
      luaK_kstr(ls, checkname(ls));
      break;
    }
    case '[': {
      next(ls);
      exp1(ls);
      check(ls, ']');
      break;
    }
    default: luaK_error(ls, "<name> or `[' expected");
  }
  check(ls, '=');
  exp1(ls);
}


static int recfields (LexState *ls) {
  /* recfields -> recfield { ',' recfield } [','] */
  FuncState *fs = ls->fs;
  int n = 1;  /* at least one element */
  recfield(ls);
  while (ls->t.token == ',') {
    next(ls);
    if (ls->t.token == ';' || ls->t.token == '}')
      break;
    recfield(ls);
    n++;
    if (n%RFIELDS_PER_FLUSH == 0)
      luaK_code1(fs, OP_SETMAP, RFIELDS_PER_FLUSH);
  }
  luaK_code1(fs, OP_SETMAP, n%RFIELDS_PER_FLUSH);
  return n;
}


static int listfields (LexState *ls) {
  /* listfields -> exp1 { ',' exp1 } [','] */
  FuncState *fs = ls->fs;
  int n = 1;  /* at least one element */
  exp1(ls);
  while (ls->t.token == ',') {
    next(ls);
    if (ls->t.token == ';' || ls->t.token == '}')
      break;
    exp1(ls);
    n++;
    luaX_checklimit(ls, n/LFIELDS_PER_FLUSH, MAXARG_A,
               "`item groups' in a list initializer");
    if (n%LFIELDS_PER_FLUSH == 0)
      luaK_code2(fs, OP_SETLIST, n/LFIELDS_PER_FLUSH - 1, LFIELDS_PER_FLUSH);
  }
  luaK_code2(fs, OP_SETLIST, n/LFIELDS_PER_FLUSH, n%LFIELDS_PER_FLUSH);
  return n;
}



static void constructor_part (LexState *ls, Constdesc *cd) {
  switch (ls->t.token) {
    case ';': case '}': {  /* constructor_part -> empty */
      cd->n = 0;
      cd->k = ls->t.token;
      break;
    }
    case TK_NAME: {  /* may be listfields or recfields */
      lookahead(ls);
      if (ls->lookahead.token != '=')  /* expression? */
        goto case_default;
      /* else go through to recfields */
    }
    case '[': {  /* constructor_part -> recfields */
      cd->n = recfields(ls);
      cd->k = 1;  /* record */
      break;
    }
    default: {  /* constructor_part -> listfields */
    case_default:
      cd->n = listfields(ls);
      cd->k = 0;  /* list */
      break;
    }
  }
}


static void constructor (LexState *ls) {
  /* constructor -> '{' constructor_part [';' constructor_part] '}' */
  FuncState *fs = ls->fs;
  int line = ls->linenumber;
  int pc = luaK_code1(fs, OP_CREATETABLE, 0);
  int nelems;
  Constdesc cd;
  check(ls, '{');
  constructor_part(ls, &cd);
  nelems = cd.n;
  if (optional(ls, ';')) {
    Constdesc other_cd;
    constructor_part(ls, &other_cd);
    check_condition(ls, (cd.k != other_cd.k), "invalid constructor syntax");
    nelems += other_cd.n;
  }
  check_match(ls, '}', '{', line);
  luaX_checklimit(ls, nelems, MAXARG_U, "elements in a table constructor");
  SETARG_U(fs->f->code[pc], nelems);  /* set initial table size */
}

/* }====================================================================== */




/*
** {======================================================================
** Expression parsing
** =======================================================================
*/


static void simpleexp (LexState *ls, expdesc *v) {
  FuncState *fs = ls->fs;
  switch (ls->t.token) {
    case TK_NUMBER: {  /* simpleexp -> NUMBER */
      Number r = ls->t.seminfo.r;
      next(ls);
      luaK_number(fs, r);
      break;
    }
    case TK_STRING: {  /* simpleexp -> STRING */
      code_string(ls, ls->t.seminfo.ts);  /* must use `seminfo' before `next' */
      next(ls);
      break;
    }
    case TK_NIL: {  /* simpleexp -> NIL */
      luaK_adjuststack(fs, -1);
      next(ls);
      break;
    }
    case '{': {  /* simpleexp -> constructor */
      constructor(ls);
      break;
    }
    case TK_FUNCTION: {  /* simpleexp -> FUNCTION body */
      next(ls);
      body(ls, 0, ls->linenumber);
      break;
    }
    case '(': {  /* simpleexp -> '(' expr ')' */
      next(ls);
      expr(ls, v);
      check(ls, ')');
      return;
    }
    case TK_NAME: case '%': {
      var_or_func(ls, v);
      return;
    }
    default: {
      luaK_error(ls, "<expression> expected");
      return;
    }
  }
  v->k = VEXP;
  v->u.l.t = v->u.l.f = NO_JUMP;
}


static void exp1 (LexState *ls) {
  expdesc v;
  expr(ls, &v);
  luaK_tostack(ls, &v, 1);
}


static UnOpr getunopr (int op) {
  switch (op) {
    case TK_NOT: return OPR_NOT;
    case '-': return OPR_MINUS;
    default: return OPR_NOUNOPR;
  }
}


static BinOpr getbinopr (int op) {
  switch (op) {
    case '+': return OPR_ADD;
    case '-': return OPR_SUB;
    case '*': return OPR_MULT;
    case '/': return OPR_DIV;
    case '^': return OPR_POW;
    case TK_CONCAT: return OPR_CONCAT;
    case TK_NE: return OPR_NE;
    case TK_EQ: return OPR_EQ;
    case '<': return OPR_LT;
    case TK_LE: return OPR_LE;
    case '>': return OPR_GT;
    case TK_GE: return OPR_GE;
    case TK_AND: return OPR_AND;
    case TK_OR: return OPR_OR;
    default: return OPR_NOBINOPR;
  }
}


static const struct {
  char left;  /* left priority for each binary operator */
  char right; /* right priority */
} priority[] = {  /* ORDER OPR */
   {5, 5}, {5, 5}, {6, 6}, {6, 6},  /* arithmetic */
   {9, 8}, {4, 3},                  /* power and concat (right associative) */
   {2, 2}, {2, 2},                  /* equality */
   {2, 2}, {2, 2}, {2, 2}, {2, 2},  /* order */
   {1, 1}, {1, 1}                   /* logical */
};

#define UNARY_PRIORITY	7  /* priority for unary operators */


/*
** subexpr -> (simplexep | unop subexpr) { binop subexpr }
** where `binop' is any binary operator with a priority higher than `limit'
*/
static BinOpr subexpr (LexState *ls, expdesc *v, int limit) {
  BinOpr op;
  UnOpr uop = getunopr(ls->t.token);
  if (uop != OPR_NOUNOPR) {
    next(ls);
    subexpr(ls, v, UNARY_PRIORITY);
    luaK_prefix(ls, uop, v);
  }
  else simpleexp(ls, v);
  /* expand while operators have priorities higher than `limit' */
  op = getbinopr(ls->t.token);
  while (op != OPR_NOBINOPR && priority[op].left > limit) {
    expdesc v2;
    BinOpr nextop;
    next(ls);
    luaK_infix(ls, op, v);
    /* read sub-expression with higher priority */
    nextop = subexpr(ls, &v2, priority[op].right);
    luaK_posfix(ls, op, v, &v2);
    op = nextop;
  }
  return op;  /* return first untreated operator */
}


static void expr (LexState *ls, expdesc *v) {
  subexpr(ls, v, -1);
}

/* }==================================================================== */


/*
** {======================================================================
** Rules for Statements
** =======================================================================
*/


static int block_follow (int token) {
  switch (token) {
    case TK_ELSE: case TK_ELSEIF: case TK_END:
    case TK_UNTIL: case TK_EOS:
      return 1;
    default: return 0;
  }
}


static void block (LexState *ls) {
  /* block -> chunk */
  FuncState *fs = ls->fs;
  int nactloc = fs->nactloc;
  chunk(ls);
  luaK_adjuststack(fs, fs->nactloc - nactloc);  /* remove local variables */
  removelocalvars(ls, fs->nactloc - nactloc);
}


static int assignment (LexState *ls, expdesc *v, int nvars) {
  int left = 0;  /* number of values left in the stack after assignment */
  luaX_checklimit(ls, nvars, MAXVARSLH, "variables in a multiple assignment");
  if (ls->t.token == ',') {  /* assignment -> ',' NAME assignment */
    expdesc nv;
    next(ls);
    var_or_func(ls, &nv);
    check_condition(ls, (nv.k != VEXP), "syntax error");
    left = assignment(ls, &nv, nvars+1);
  }
  else {  /* assignment -> '=' explist1 */
    int nexps;
    check(ls, '=');
    nexps = explist1(ls);
    adjust_mult_assign(ls, nvars, nexps);
  }
  if (v->k != VINDEXED)
    luaK_storevar(ls, v);
  else {  /* there may be garbage between table-index and value */
    luaK_code2(ls->fs, OP_SETTABLE, left+nvars+2, 1);
    left += 2;
  }
  return left;
}


static void cond (LexState *ls, expdesc *v) {
  /* cond -> exp */
  expr(ls, v);  /* read condition */
  luaK_goiftrue(ls->fs, v, 0);
}


static void whilestat (LexState *ls, int line) {
  /* whilestat -> WHILE cond DO block END */
  FuncState *fs = ls->fs;
  int while_init = luaK_getlabel(fs);
  expdesc v;
  Breaklabel bl;
  enterbreak(fs, &bl);
  next(ls);
  cond(ls, &v);
  check(ls, TK_DO);
  block(ls);
  luaK_patchlist(fs, luaK_jump(fs), while_init);
  luaK_patchlist(fs, v.u.l.f, luaK_getlabel(fs));
  check_match(ls, TK_END, TK_WHILE, line);
  leavebreak(fs, &bl);
}


static void repeatstat (LexState *ls, int line) {
  /* repeatstat -> REPEAT block UNTIL cond */
  FuncState *fs = ls->fs;
  int repeat_init = luaK_getlabel(fs);
  expdesc v;
  Breaklabel bl;
  enterbreak(fs, &bl);
  next(ls);
  block(ls);
  check_match(ls, TK_UNTIL, TK_REPEAT, line);
  cond(ls, &v);
  luaK_patchlist(fs, v.u.l.f, repeat_init);
  leavebreak(fs, &bl);
}


static void forbody (LexState *ls, int nvar, OpCode prepfor, OpCode loopfor) {
  /* forbody -> DO block END */
  FuncState *fs = ls->fs;
  int prep = luaK_code1(fs, prepfor, NO_JUMP);
  int blockinit = luaK_getlabel(fs);
  check(ls, TK_DO);
  adjustlocalvars(ls, nvar);  /* scope for control variables */
  block(ls);
  luaK_patchlist(fs, luaK_code1(fs, loopfor, NO_JUMP), blockinit);
  luaK_patchlist(fs, prep, luaK_getlabel(fs));
  removelocalvars(ls, nvar);
}


static void fornum (LexState *ls, TString *varname) {
  /* fornum -> NAME = exp1,exp1[,exp1] forbody */
  FuncState *fs = ls->fs;
  check(ls, '=');
  exp1(ls);  /* initial value */
  check(ls, ',');
  exp1(ls);  /* limit */
  if (optional(ls, ','))
    exp1(ls);  /* optional step */
  else
    luaK_code1(fs, OP_PUSHINT, 1);  /* default step */
  new_localvar(ls, varname, 0);
  new_localvarstr(ls, "(limit)", 1);
  new_localvarstr(ls, "(step)", 2);
  forbody(ls, 3, OP_FORPREP, OP_FORLOOP);
}


static void forlist (LexState *ls, TString *indexname) {
  /* forlist -> NAME,NAME IN exp1 forbody */
  TString *valname;
  check(ls, ',');
  valname = str_checkname(ls);
  /* next test is dirty, but avoids `in' being a reserved word */
  check_condition(ls,
       (ls->t.token == TK_NAME && ls->t.seminfo.ts == luaS_new(ls->L, "in")),
       "`in' expected");
  next(ls);  /* skip `in' */
  exp1(ls);  /* table */
  new_localvarstr(ls, "(table)", 0);
  new_localvar(ls, indexname, 1);
  new_localvar(ls, valname, 2);
  forbody(ls, 3, OP_LFORPREP, OP_LFORLOOP);
}


static void forstat (LexState *ls, int line) {
  /* forstat -> fornum | forlist */
  FuncState *fs = ls->fs;
  TString *varname;
  Breaklabel bl;
  enterbreak(fs, &bl);
  next(ls);  /* skip `for' */
  varname = str_checkname(ls);  /* first variable name */
  switch (ls->t.token) {
    case '=': fornum(ls, varname); break;
    case ',': forlist(ls, varname); break;
    default: luaK_error(ls, "`=' or `,' expected");
  }
  check_match(ls, TK_END, TK_FOR, line);
  leavebreak(fs, &bl);
}


static void test_then_block (LexState *ls, expdesc *v) {
  /* test_then_block -> [IF | ELSEIF] cond THEN block */
  next(ls);  /* skip IF or ELSEIF */
  cond(ls, v);
  check(ls, TK_THEN);
  block(ls);  /* `then' part */
}


static void ifstat (LexState *ls, int line) {
  /* ifstat -> IF cond THEN block {ELSEIF cond THEN block} [ELSE block] END */
  FuncState *fs = ls->fs;
  expdesc v;
  int escapelist = NO_JUMP;
  test_then_block(ls, &v);  /* IF cond THEN block */
  while (ls->t.token == TK_ELSEIF) {
    luaK_concat(fs, &escapelist, luaK_jump(fs));
    luaK_patchlist(fs, v.u.l.f, luaK_getlabel(fs));
    test_then_block(ls, &v);  /* ELSEIF cond THEN block */
  }
  if (ls->t.token == TK_ELSE) {
    luaK_concat(fs, &escapelist, luaK_jump(fs));
    luaK_patchlist(fs, v.u.l.f, luaK_getlabel(fs));
    next(ls);  /* skip ELSE */
    block(ls);  /* `else' part */
  }
  else
    luaK_concat(fs, &escapelist, v.u.l.f);
  luaK_patchlist(fs, escapelist, luaK_getlabel(fs));
  check_match(ls, TK_END, TK_IF, line);
}


static void localstat (LexState *ls) {
  /* stat -> LOCAL NAME {',' NAME} ['=' explist1] */
  int nvars = 0;
  int nexps;
  do {
    next(ls);  /* skip LOCAL or ',' */
    new_localvar(ls, str_checkname(ls), nvars++);
  } while (ls->t.token == ',');
  if (optional(ls, '='))
    nexps = explist1(ls);
  else
    nexps = 0;
  adjust_mult_assign(ls, nvars, nexps);
  adjustlocalvars(ls, nvars);
}


static int funcname (LexState *ls, expdesc *v) {
  /* funcname -> NAME [':' NAME | '.' NAME] */
  int needself = 0;
  singlevar(ls, str_checkname(ls), v);
  if (ls->t.token == ':' || ls->t.token == '.') {
    needself = (ls->t.token == ':');
    next(ls);
    luaK_tostack(ls, v, 1);
    luaK_kstr(ls, checkname(ls));
    v->k = VINDEXED;
  }
  return needself;
}


static void funcstat (LexState *ls, int line) {
  /* funcstat -> FUNCTION funcname body */
  int needself;
  expdesc v;
  next(ls);  /* skip FUNCTION */
  needself = funcname(ls, &v);
  body(ls, needself, line);
  luaK_storevar(ls, &v);
}


static void namestat (LexState *ls) {
  /* stat -> func | ['%'] NAME assignment */
  FuncState *fs = ls->fs;
  expdesc v;
  var_or_func(ls, &v);
  if (v.k == VEXP) {  /* stat -> func */
    check_condition(ls, luaK_lastisopen(fs), "syntax error");  /* an upvalue? */
    luaK_setcallreturns(fs, 0);  /* call statement uses no results */
  }
  else {  /* stat -> ['%'] NAME assignment */
    int left = assignment(ls, &v, 1);
    luaK_adjuststack(fs, left);  /* remove eventual garbage left on stack */
  }
}


static void retstat (LexState *ls) {
  /* stat -> RETURN explist */
  FuncState *fs = ls->fs;
  next(ls);  /* skip RETURN */
  if (!block_follow(ls->t.token))
    explist1(ls);  /* optional return values */
  luaK_code1(fs, OP_RETURN, ls->fs->nactloc);
  fs->stacklevel = fs->nactloc;  /* removes all temp values */
}


static void breakstat (LexState *ls) {
  /* stat -> BREAK [NAME] */
  FuncState *fs = ls->fs;
  int currentlevel = fs->stacklevel;
  Breaklabel *bl = fs->bl;
  if (!bl)
    luaK_error(ls, "no loop to break");
  next(ls);  /* skip BREAK */
  luaK_adjuststack(fs, currentlevel - bl->stacklevel);
  luaK_concat(fs, &bl->breaklist, luaK_jump(fs));
  /* correct stack for compiler and symbolic execution */
  luaK_adjuststack(fs, bl->stacklevel - currentlevel);
}


static int luaP_stat (LexState *ls) {
  int line = ls->linenumber;  /* may be needed for error messages */
  switch (ls->t.token) {
    case TK_IF: {  /* stat -> ifstat */
      ifstat(ls, line);
      return 0;
    }
    case TK_WHILE: {  /* stat -> whilestat */
      whilestat(ls, line);
      return 0;
    }
    case TK_DO: {  /* stat -> DO block END */
      next(ls);  /* skip DO */
      block(ls);
      check_match(ls, TK_END, TK_DO, line);
      return 0;
    }
    case TK_FOR: {  /* stat -> forstat */
      forstat(ls, line);
      return 0;
    }
    case TK_REPEAT: {  /* stat -> repeatstat */
      repeatstat(ls, line);
      return 0;
    }
    case TK_FUNCTION: {  /* stat -> funcstat */
      funcstat(ls, line);
      return 0;
    }
    case TK_LOCAL: {  /* stat -> localstat */
      localstat(ls);
      return 0;
    }
    case TK_NAME: case '%': {  /* stat -> namestat */
      namestat(ls);
      return 0;
    }
    case TK_RETURN: {  /* stat -> retstat */
      retstat(ls);
      return 1;  /* must be last statement */
    }
    case TK_BREAK: {  /* stat -> breakstat */
      breakstat(ls);
      return 1;  /* must be last statement */
    }
    default: {
      luaK_error(ls, "<statement> expected");
      return 0;  /* to avoid warnings */
    }
  }
}


static void parlist (LexState *ls) {
  /* parlist -> [ param { ',' param } ] */
  int nparams = 0;
  int dots = 0;
  if (ls->t.token != ')') {  /* is `parlist' not empty? */
    do {
      switch (ls->t.token) {
        case TK_DOTS: next(ls); dots = 1; break;
        case TK_NAME: new_localvar(ls, str_checkname(ls), nparams++); break;
        default: luaK_error(ls, "<name> or `...' expected");
      }
    } while (!dots && optional(ls, ','));
  }
  code_params(ls, nparams, dots);
}


static void body (LexState *ls, int needself, int line) {
  /* body ->  '(' parlist ')' chunk END */
  FuncState new_fs;
  open_func(ls, &new_fs);
  new_fs.f->lineDefined = line;
  check(ls, '(');
  if (needself) {
    new_localvarstr(ls, "self", 0);
    adjustlocalvars(ls, 1);
  }
  parlist(ls);
  check(ls, ')');
  chunk(ls);
  check_match(ls, TK_END, TK_FUNCTION, line);
  close_func(ls);
  pushclosure(ls, &new_fs);
}


/* }====================================================================== */


static void chunk (LexState *ls) {
  /* chunk -> { stat [';'] } */
  int islast = 0;
  while (!islast && !block_follow(ls->t.token)) {
    islast = luaP_stat(ls);
    optional(ls, ';');
    LUA_ASSERT(ls->fs->stacklevel == ls->fs->nactloc,
               "stack size != # local vars");
  }
}

/* resumed: mluxsys.c */
#endif

/* include: lstate.c */
/*
** $Id: lstate.c,v 1.48 2000/10/30 16:29:59 roberto Exp $
** Global State
** See Copyright Notice in lua.h
*/


#include <stdio.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lgc.h - see lua-4.0/src/lapi.c */
/* skipped: llex.h - see lua-4.0/src/lcode.h */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */


#ifdef LUA_DEBUG
static lua_State *lua_state = NULL;
void luaB_opentests (lua_State *L);
#endif


/*
** built-in implementation for ERRORMESSAGE. In a "correct" environment
** ERRORMESSAGE should have an external definition, and so this function
** would not be used.
*/
static int errormessage (lua_State *L) {
  const char *s = lua_tostring(L, 1);
  if (s == NULL) s = "(no message)";
  fprintf(stderr, "error: %s\n", s);
  return 0;
}


/*
** open parts that may cause memory-allocation errors
*/
static void f_luaopen (lua_State *L, void *ud) {
  int stacksize = *(int *)ud;
  if (stacksize == 0)
    stacksize = DEFAULT_STACK_SIZE;
  else
    stacksize += LUA_MINSTACK;
  L->gt = luaH_new(L, 10);  /* table of globals */
  luaD_init(L, stacksize);
  luaS_init(L);
  luaX_init(L);
  luaT_init(L);
  lua_newtable(L);
  lua_ref(L, 1);  /* create registry */
  lua_register(L, LUA_ERRORMESSAGE, errormessage);
#ifdef LUA_DEBUG
  luaB_opentests(L);
  if (lua_state == NULL) lua_state = L;  /* keep first state to be opened */
#endif
  LUA_ASSERT(lua_gettop(L) == 0, "wrong API stack");
}


LUA_API lua_State *lua_open (int stacksize) {
  lua_State *L = luaM_new(NULL, lua_State);
  if (L == NULL) return NULL;  /* memory allocation error */
  L->stack = NULL;
  L->strt.size = L->udt.size = 0;
  L->strt.nuse = L->udt.nuse = 0;
  L->strt.hash = NULL;
  L->udt.hash = NULL;
  L->Mbuffer = NULL;
  L->Mbuffsize = 0;
  L->rootproto = NULL;
  L->rootcl = NULL;
  L->roottable = NULL;
  L->TMtable = NULL;
  L->last_tag = -1;
  L->refArray = NULL;
  L->refSize = 0;
  L->refFree = NONEXT;
  L->nblocks = sizeof(lua_State);
  L->GCthreshold = MAX_INT;  /* to avoid GC during pre-definitions */
  L->callhook = NULL;
  L->linehook = NULL;
  L->allowhooks = 1;
  L->errorJmp = NULL;
  if (luaD_runprotected(L, f_luaopen, &stacksize) != 0) {
    /* memory allocation error: free partial state */
    lua_close(L);
    return NULL;
  }
  L->GCthreshold = 2*L->nblocks;
  return L;
}


LUA_API void lua_close (lua_State *L) {
  LUA_ASSERT(L != lua_state || lua_gettop(L) == 0, "garbage in C stack");
  luaC_collect(L, 1);  /* collect all elements */
  LUA_ASSERT(L->rootproto == NULL, "list should be empty");
  LUA_ASSERT(L->rootcl == NULL, "list should be empty");
  LUA_ASSERT(L->roottable == NULL, "list should be empty");
  luaS_freeall(L);
  if (L->stack)
    L->nblocks -= (L->stack_last - L->stack + 1)*sizeof(TObject);
  luaM_free(L, L->stack);
  L->nblocks -= (L->last_tag+1)*sizeof(struct TM);
  luaM_free(L, L->TMtable);
  L->nblocks -= (L->refSize)*sizeof(struct Ref);
  luaM_free(L, L->refArray);
  L->nblocks -= (L->Mbuffsize)*sizeof(char);
  luaM_free(L, L->Mbuffer);
  LUA_ASSERT(L->nblocks == sizeof(lua_State), "wrong count for nblocks");
  luaM_free(L, L);
  LUA_ASSERT(L != lua_state || memdebug_numblocks == 0, "memory leak!");
  LUA_ASSERT(L != lua_state || memdebug_total == 0,"memory leak!");
}

/* resumed: mluxsys.c */
/* include: lstring.c */
/*
** $Id: lstring.c,v 1.45 2000/10/30 17:49:19 roberto Exp $
** String table (keeps all strings handled by Lua)
** See Copyright Notice in lua.h
*/


#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */


/*
** type equivalent to TString, but with maximum alignment requirements
*/
union L_UTString {
  TString ts;
  union L_Umaxalign dummy;  /* ensures maximum alignment for `local' udata */
};



void luaS_init (lua_State *L) {
  L->strt.hash = luaM_newvector(L, 1, TString *);
  L->udt.hash = luaM_newvector(L, 1, TString *);
  L->nblocks += 2*sizeof(TString *);
  L->strt.size = L->udt.size = 1;
  L->strt.nuse = L->udt.nuse = 0;
  L->strt.hash[0] = L->udt.hash[0] = NULL;
}


void luaS_freeall (lua_State *L) {
  LUA_ASSERT(L->strt.nuse==0, "non-empty string table");
  L->nblocks -= (L->strt.size + L->udt.size)*sizeof(TString *);
  luaM_free(L, L->strt.hash);
  LUA_ASSERT(L->udt.nuse==0, "non-empty udata table");
  luaM_free(L, L->udt.hash);
}


static unsigned long hash_s (const char *s, size_t l) {
  unsigned long h = l;  /* seed */
  size_t step = (l>>5)|1;  /* if string is too long, don't hash all its chars */
  for (; l>=step; l-=step)
    h = h ^ ((h<<5)+(h>>2)+(unsigned char)*(s++));
  return h;
}


void luaS_resize (lua_State *L, stringtable *tb, int newsize) {
  TString **newhash = luaM_newvector(L, newsize, TString *);
  int i;
  for (i=0; i<newsize; i++) newhash[i] = NULL;
  /* rehash */
  for (i=0; i<tb->size; i++) {
    TString *p = tb->hash[i];
    while (p) {  /* for each node in the list */
      TString *next = p->nexthash;  /* save next */
      unsigned long h = (tb == &L->strt) ? p->u.s.hash : IntPoint(p->u.d.value);
      int h1 = h&(newsize-1);  /* new position */
      LUA_ASSERT(h%newsize == (h&(newsize-1)),
                    "a&(x-1) == a%x, for x power of 2");
      p->nexthash = newhash[h1];  /* chain it in new position */
      newhash[h1] = p;
      p = next;
    }
  }
  luaM_free(L, tb->hash);
  L->nblocks += (newsize - tb->size)*sizeof(TString *);
  tb->size = newsize;
  tb->hash = newhash;
}


static void newentry (lua_State *L, stringtable *tb, TString *ts, int h) {
  ts->nexthash = tb->hash[h];  /* chain new entry */
  tb->hash[h] = ts;
  tb->nuse++;
  if (tb->nuse > (lint32)tb->size && tb->size < MAX_INT/2)  /* too crowded? */
    luaS_resize(L, tb, tb->size*2);
}



TString *luaS_newlstr (lua_State *L, const char *str, size_t l) {
  unsigned long h = hash_s(str, l);
  int h1 = h & (L->strt.size-1);
  TString *ts;
  for (ts = L->strt.hash[h1]; ts; ts = ts->nexthash) {
    if (ts->len == l && (memcmp(str, ts->str, l) == 0))
      return ts;
  }
  /* not found */
  ts = (TString *)luaM_malloc(L, sizestring(l));
  ts->marked = 0;
  ts->nexthash = NULL;
  ts->len = l;
  ts->u.s.hash = h;
  ts->u.s.constindex = 0;
  memcpy(ts->str, str, l);
  ts->str[l] = 0;  /* ending 0 */
  L->nblocks += sizestring(l);
  newentry(L, &L->strt, ts, h1);  /* insert it on table */
  return ts;
}


TString *luaS_newudata (lua_State *L, size_t s, void *udata) {
  union L_UTString *uts = (union L_UTString *)luaM_malloc(L,
                                (lint32)sizeof(union L_UTString)+s);
  TString *ts = &uts->ts;
  ts->marked = 0;
  ts->nexthash = NULL;
  ts->len = s;
  ts->u.d.tag = 0;
  ts->u.d.value = (udata == NULL) ? uts+1 : udata;
  L->nblocks += sizestring(s);
 /* insert it on table */
  newentry(L, &L->udt, ts, IntPoint(ts->u.d.value) & (L->udt.size-1));
  return ts;
}


TString *luaS_createudata (lua_State *L, void *udata, int tag) {
  int h1 = IntPoint(udata) & (L->udt.size-1);
  TString *ts;
  for (ts = L->udt.hash[h1]; ts; ts = ts->nexthash) {
    if (udata == ts->u.d.value && (tag == ts->u.d.tag || tag == LUA_ANYTAG))
      return ts;
  }
  /* not found */
  ts = luaS_newudata(L, 0, udata);
  if (tag != LUA_ANYTAG)
    ts->u.d.tag = tag;
  return ts;
}


TString *luaS_new (lua_State *L, const char *str) {
  return luaS_newlstr(L, str, strlen(str));
}


TString *luaS_newfixed (lua_State *L, const char *str) {
  TString *ts = luaS_new(L, str);
  if (ts->marked == 0) ts->marked = FIXMARK;  /* avoid GC */
  return ts;
}

/* resumed: mluxsys.c */
/* include: ltable.c */
/*
** $Id: ltable.c,v 1.58 2000/10/26 12:47:05 roberto Exp $
** Lua tables (hash)
** See Copyright Notice in lua.h
*/


/*
** Implementation of tables (aka arrays, objects, or hash tables);
** uses a mix of chained scatter table with Brent's variation.
** A main invariant of these tables is that, if an element is not
** in its main position (i.e. the `original' position that its hash gives
** to it), then the colliding element is in its own main position.
** In other words, there are collisions only when two elements have the
** same main position (i.e. the same hash values for that table size).
** Because of that, the load factor of these tables can be 100% without
** performance penalties.
*/


/* skipped: lua.h - see mluxsys.c */

/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */


#define gcsize(L, n)	(sizeof(Hash)+(n)*sizeof(Node))



#define TagDefault LUA_TTABLE



/*
** returns the `main' position of an element in a table (that is, the index
** of its hash value)
*/
Node *luaH_mainposition (const Hash *t, const TObject *key) {
  unsigned long h;
  switch (ttype(key)) {
    case LUA_TNUMBER:
      h = (unsigned long)(long)nvalue(key);
      break;
    case LUA_TSTRING:
      h = tsvalue(key)->u.s.hash;
      break;
    case LUA_TUSERDATA:
      h = IntPoint(tsvalue(key));
      break;
    case LUA_TTABLE:
      h = IntPoint(hvalue(key));
      break;
    case LUA_TFUNCTION:
      h = IntPoint(clvalue(key));
      break;
    default:
      return NULL;  /* invalid key */
  }
  LUA_ASSERT(h%(unsigned int)t->size == (h&((unsigned int)t->size-1)),
            "a&(x-1) == a%x, for x power of 2");
  return &t->node[h&(t->size-1)];
}


static const TObject *luaH_getany (lua_State *L, const Hash *t,
                                   const TObject *key) {
  Node *n = luaH_mainposition(t, key);
  if (!n)
    lua_error(L, "table index is nil");
  else do {
    if (luaO_equalObj(key, &n->key))
      return &n->val;
    n = n->next;
  } while (n);
  return &luaO_nilobject;  /* key not found */
}


/* specialized version for numbers */
const TObject *luaH_getnum (const Hash *t, Number key) {
  Node *n = &t->node[(unsigned long)(long)key&(t->size-1)];
  do {
    if (ttype(&n->key) == LUA_TNUMBER && nvalue(&n->key) == key)
      return &n->val;
    n = n->next;
  } while (n);
  return &luaO_nilobject;  /* key not found */
}


/* specialized version for strings */
const TObject *luaH_getstr (const Hash *t, TString *key) {
  Node *n = &t->node[key->u.s.hash&(t->size-1)];
  do {
    if (ttype(&n->key) == LUA_TSTRING && tsvalue(&n->key) == key)
      return &n->val;
    n = n->next;
  } while (n);
  return &luaO_nilobject;  /* key not found */
}


const TObject *luaH_get (lua_State *L, const Hash *t, const TObject *key) {
  switch (ttype(key)) {
    case LUA_TNUMBER: return luaH_getnum(t, nvalue(key));
    case LUA_TSTRING: return luaH_getstr(t, tsvalue(key));
    default:         return luaH_getany(L, t, key);
  }
}


Node *luaH_next (lua_State *L, const Hash *t, const TObject *key) {
  int i;
  if (ttype(key) == LUA_TNIL)
    i = 0;  /* first iteration */
  else {
    const TObject *v = luaH_get(L, t, key);
    if (v == &luaO_nilobject)
      lua_error(L, "invalid key for `next'");
    i = (int)(((const char *)v -
               (const char *)(&t->node[0].val)) / sizeof(Node)) + 1;
  }
  for (; i<t->size; i++) {
    Node *n = node(t, i);
    if (ttype(val(n)) != LUA_TNIL)
      return n;
  }
  return NULL;  /* no more elements */
}


/*
** try to remove a key without value from a table. To avoid problems with
** hash, change `key' for a number with the same hash.
*/
void luaH_remove (Hash *t, TObject *key) {
  if (ttype(key) == LUA_TNUMBER ||
       (ttype(key) == LUA_TSTRING && tsvalue(key)->len <= 30))
  return;  /* do not remove numbers nor small strings */
  else {
    /* try to find a number `n' with the same hash as `key' */
    Node *mp = luaH_mainposition(t, key);
    int n = mp - &t->node[0];
    /* make sure `n' is not in `t' */
    while (luaH_getnum(t, n) != &luaO_nilobject) {
      if (n >= MAX_INT - t->size)
        return;  /* give up; (to avoid overflow) */
      n += t->size;
    }
    ttype(key) = LUA_TNUMBER;
    nvalue(key) = n;
    LUA_ASSERT(luaH_mainposition(t, key) == mp, "cannot change hash");
  }
}


static void setnodevector (lua_State *L, Hash *t, lint32 size) {
  int i;
  if (size > MAX_INT)
    lua_error(L, "table overflow");
  t->node = luaM_newvector(L, size, Node);
  for (i=0; i<(int)size; i++) {
    ttype(&t->node[i].key) = ttype(&t->node[i].val) = LUA_TNIL;
    t->node[i].next = NULL;
  }
  L->nblocks += gcsize(L, size) - gcsize(L, t->size);
  t->size = size;
  t->firstfree = &t->node[size-1];  /* first free position to be used */
}


Hash *luaH_new (lua_State *L, int size) {
  Hash *t = luaM_new(L, Hash);
  t->htag = TagDefault;
  t->next = L->roottable;
  L->roottable = t;
  t->mark = t;
  t->size = 0;
  L->nblocks += gcsize(L, 0);
  t->node = NULL;
  setnodevector(L, t, luaO_power2(size));
  return t;
}


void luaH_free (lua_State *L, Hash *t) {
  L->nblocks -= gcsize(L, t->size);
  luaM_free(L, t->node);
  luaM_free(L, t);
}


static int numuse (const Hash *t) {
  Node *v = t->node;
  int size = t->size;
  int realuse = 0;
  int i;
  for (i=0; i<size; i++) {
    if (ttype(&v[i].val) != LUA_TNIL)
      realuse++;
  }
  return realuse;
}


static void rehash (lua_State *L, Hash *t) {
  int oldsize = t->size;
  Node *nold = t->node;
  int nelems = numuse(t);
  int i;
  LUA_ASSERT(nelems<=oldsize, "wrong count");
  if (nelems >= oldsize-oldsize/4)  /* using more than 3/4? */
    setnodevector(L, t, (lint32)oldsize*2);
  else if (nelems <= oldsize/4 &&  /* less than 1/4? */
           oldsize > MINPOWER2)
    setnodevector(L, t, oldsize/2);
  else
    setnodevector(L, t, oldsize);
  for (i=0; i<oldsize; i++) {
    Node *old = nold+i;
    if (ttype(&old->val) != LUA_TNIL)
      *luaH_set(L, t, &old->key) = old->val;
  }
  luaM_free(L, nold);  /* free old array */
}


/*
** inserts a key into a hash table; first, check whether key is
** already present; if not, check whether key's main position is free;
** if not, check whether colliding node is in its main position or not;
** if it is not, move colliding node to an empty place and put new key
** in its main position; otherwise (colliding node is in its main position),
** new key goes to an empty position.
*/
TObject *luaH_set (lua_State *L, Hash *t, const TObject *key) {
  Node *mp = luaH_mainposition(t, key);
  Node *n = mp;
  if (!mp)
    lua_error(L, "table index is nil");
  do {  /* check whether `key' is somewhere in the chain */
    if (luaO_equalObj(key, &n->key))
      return &n->val;  /* that's all */
    else n = n->next;
  } while (n);
  /* `key' not found; must insert it */
  if (ttype(&mp->key) != LUA_TNIL) {  /* main position is not free? */
    Node *othern;  /* main position of colliding node */
    n = t->firstfree;  /* get a free place */
    /* is colliding node out of its main position? (can only happens if
       its position is after "firstfree") */
    if (mp > n && (othern=luaH_mainposition(t, &mp->key)) != mp) {
      /* yes; move colliding node into free position */
      while (othern->next != mp) othern = othern->next;  /* find previous */
      othern->next = n;  /* redo the chain with `n' in place of `mp' */
      *n = *mp;  /* copy colliding node into free pos. (mp->next also goes) */
      mp->next = NULL;  /* now `mp' is free */
    }
    else {  /* colliding node is in its own main position */
      /* new node will go into free position */
      n->next = mp->next;  /* chain new position */
      mp->next = n;
      mp = n;
    }
  }
  mp->key = *key;
  for (;;) {  /* correct `firstfree' */
    if (ttype(&t->firstfree->key) == LUA_TNIL)
      return &mp->val;  /* OK; table still has a free place */
    else if (t->firstfree == t->node) break;  /* cannot decrement from here */
    else (t->firstfree)--;
  }
  rehash(L, t);  /* no more free places */
  return luaH_set(L, t, key);  /* `rehash' invalidates this insertion */
}


TObject *luaH_setint (lua_State *L, Hash *t, int key) {
  TObject index;
  ttype(&index) = LUA_TNUMBER;
  nvalue(&index) = key;
  return luaH_set(L, t, &index);
}


void luaH_setstrnum (lua_State *L, Hash *t, TString *key, Number val) {
  TObject *value, index;
  ttype(&index) = LUA_TSTRING;
  tsvalue(&index) = key;
  value = luaH_set(L, t, &index);
  ttype(value) = LUA_TNUMBER;
  nvalue(value) = val;
}


const TObject *luaH_getglobal (lua_State *L, const char *name) {
  return luaH_getstr(L->gt, luaS_new(L, name));
}

/* resumed: mluxsys.c */

#ifndef NOPARSER
/* include: ltests.c */
/*
** $Id: ltests.c,v 1.54 2000/10/31 13:10:24 roberto Exp $
** Internal Module for Debugging of the Lua Implementation
** See Copyright Notice in lua.h
*/


#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* skipped: lua.h - see mluxsys.c */

/* skipped: lapi.h - see lua-4.0/src/lapi.c */
/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: lcode.h - see lua-4.0/src/lcode.c */
/* skipped: ldebug.h - see lua-4.0/src/ldebug.c */
/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: luadebug.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */


void luaB_opentests (lua_State *L);


/*
** The whole module only makes sense with LUA_DEBUG on
*/
#ifdef LUA_DEBUG



static void setnameval (lua_State *L, const char *name, int val) {
  lua_pushstring(L, name);
  lua_pushnumber(L, val);
  lua_settable(L, -3);
}


/*
** {======================================================
** Disassembler
** =======================================================
*/


static const char *const instrname[NUM_OPCODES] = {
  "END", "RETURN", "CALL", "TAILCALL", "PUSHNIL", "POP", "PUSHINT", 
  "PUSHSTRING", "PUSHNUM", "PUSHNEGNUM", "PUSHUPVALUE", "GETLOCAL", 
  "GETGLOBAL", "GETTABLE", "GETDOTTED", "GETINDEXED", "PUSHSELF", 
  "CREATETABLE", "SETLOCAL", "SETGLOBAL", "SETTABLE", "SETLIST", "SETMAP", 
  "ADD", "ADDI", "SUB", "MULT", "DIV", "POW", "CONCAT", "MINUS", "NOT", 
  "JMPNE", "JMPEQ", "JMPLT", "JMPLE", "JMPGT", "JMPGE", "JMPT", "JMPF", 
  "JMPONT", "JMPONF", "JMP", "PUSHNILJMP", "FORPREP", "FORLOOP", "LFORPREP", 
  "LFORLOOP", "CLOSURE"
};


static int pushop (lua_State *L, Proto *p, int pc) {
  char buff[100];
  Instruction i = p->code[pc];
  OpCode o = GET_OPCODE(i);
  const char *name = instrname[o];
  sprintf(buff, "%5d - ", luaG_getline(p->lineinfo, pc, 1, NULL));
  switch ((enum Mode)luaK_opproperties[o].mode) {  
    case iO:
      sprintf(buff+8, "%-12s", name);
      break;
    case iU:
      sprintf(buff+8, "%-12s%4u", name, GETARG_U(i));
      break;
    case iS:
      sprintf(buff+8, "%-12s%4d", name, GETARG_S(i));
      break;
    case iAB:
      sprintf(buff+8, "%-12s%4d %4d", name, GETARG_A(i), GETARG_B(i));
      break;
  }
  lua_pushstring(L, buff);
  return (o != OP_END);
}


static int listcode (lua_State *L) {
  int pc;
  Proto *p;
  int res;
  luaL_arg_check(L, lua_isfunction(L, 1) && !lua_iscfunction(L, 1),
                 1, "Lua function expected");
  p = clvalue(luaA_index(L, 1))->f.l;
  lua_newtable(L);
  setnameval(L, "maxstack", p->maxstacksize);
  setnameval(L, "numparams", p->numparams);
  pc = 0;
  do {
    lua_pushnumber(L, pc+1);
    res = pushop(L, p, pc++);
    lua_settable(L, -3);
  } while (res);
  return 1;
}


static int liststrings (lua_State *L) {
  Proto *p;
  int i;
  luaL_arg_check(L, lua_isfunction(L, 1) && !lua_iscfunction(L, 1),
                 1, "Lua function expected");
  p = clvalue(luaA_index(L, 1))->f.l;
  lua_newtable(L);
  for (i=0; i<p->nkstr; i++) {
    lua_pushnumber(L, i+1);
    lua_pushstring(L, p->kstr[i]->str);
    lua_settable(L, -3);
  }
  return 1;
}


static int listlocals (lua_State *L) {
  Proto *p;
  int pc = luaL_check_int(L, 2) - 1;
  int i = 0;
  const char *name;
  luaL_arg_check(L, lua_isfunction(L, 1) && !lua_iscfunction(L, 1),
                 1, "Lua function expected");
  p = clvalue(luaA_index(L, 1))->f.l;
  while ((name = luaF_getlocalname(p, ++i, pc)) != NULL)
    lua_pushstring(L, name);
  return i-1;
}

/* }====================================================== */



static int get_limits (lua_State *L) {
  lua_newtable(L);
  setnameval(L, "BITS_INT", BITS_INT);
  setnameval(L, "LFPF", LFIELDS_PER_FLUSH);
  setnameval(L, "MAXARG_A", MAXARG_A);
  setnameval(L, "MAXARG_B", MAXARG_B);
  setnameval(L, "MAXARG_S", MAXARG_S);
  setnameval(L, "MAXARG_U", MAXARG_U);
  setnameval(L, "MAXLOCALS", MAXLOCALS);
  setnameval(L, "MAXPARAMS", MAXPARAMS);
  setnameval(L, "MAXSTACK", MAXSTACK);
  setnameval(L, "MAXUPVALUES", MAXUPVALUES);
  setnameval(L, "MAXVARSLH", MAXVARSLH);
  setnameval(L, "RFPF", RFIELDS_PER_FLUSH);
  setnameval(L, "SIZE_A", SIZE_A);
  setnameval(L, "SIZE_B", SIZE_B);
  setnameval(L, "SIZE_OP", SIZE_OP);
  setnameval(L, "SIZE_U", SIZE_U);
  return 1;
}


static int mem_query (lua_State *L) {
  if (lua_isnull(L, 1)) {
    lua_pushnumber(L, memdebug_total);
    lua_pushnumber(L, memdebug_numblocks);
    lua_pushnumber(L, memdebug_maxmem);
    return 3;
  }
  else {
    memdebug_memlimit = luaL_check_int(L, 1);
    return 0;
  }
}


static int hash_query (lua_State *L) {
  if (lua_isnull(L, 2)) {
    luaL_arg_check(L, lua_tag(L, 1) == LUA_TSTRING, 1, "string expected");
    lua_pushnumber(L, tsvalue(luaA_index(L, 1))->u.s.hash);
  }
  else {
    Hash *t;
    luaL_checktype(L, 2, LUA_TTABLE);
    t = hvalue(luaA_index(L, 2));
    lua_pushnumber(L, luaH_mainposition(t, luaA_index(L, 1)) - t->node);
  }
  return 1;
}


static int table_query (lua_State *L) {
  const Hash *t;
  int i = luaL_opt_int(L, 2, -1);
  luaL_checktype(L, 1, LUA_TTABLE);
  t = hvalue(luaA_index(L, 1));
  if (i == -1) {
    lua_pushnumber(L, t->size);
    lua_pushnumber(L, t->firstfree - t->node);
    return 2;
  }
  else if (i < t->size) {
    luaA_pushobject(L, &t->node[i].key);
    luaA_pushobject(L, &t->node[i].val);
    if (t->node[i].next) {
      lua_pushnumber(L, t->node[i].next - t->node);
      return 3;
    }
    else
      return 2;
  }
  return 0;
}


static int string_query (lua_State *L) {
  stringtable *tb = (*luaL_check_string(L, 1) == 's') ? &L->strt : &L->udt;
  int s = luaL_opt_int(L, 2, 0) - 1;
  if (s==-1) {
    lua_pushnumber(L ,tb->nuse);
    lua_pushnumber(L ,tb->size);
    return 2;
  }
  else if (s < tb->size) {
    TString *ts;
    int n = 0;
    for (ts = tb->hash[s]; ts; ts = ts->nexthash) {
      ttype(L->top) = LUA_TSTRING;
      tsvalue(L->top) = ts;
      incr_top;
      n++;
    }
    return n;
  }
  return 0;
}


static int tref (lua_State *L) {
  luaL_checkany(L, 1);
  lua_pushvalue(L, 1);
  lua_pushnumber(L, lua_ref(L, luaL_opt_int(L, 2, 1)));
  return 1;
}

static int getref (lua_State *L) {
  if (lua_getref(L, luaL_check_int(L, 1)))
    return 1;
  else
    return 0;
}

static int unref (lua_State *L) {
  lua_unref(L, luaL_check_int(L, 1));
  return 0;
}

static int newuserdata (lua_State *L) {
  if (lua_isnumber(L, 2))
    lua_pushusertag(L, (void *)luaL_check_int(L, 1), luaL_check_int(L, 2));
  else
    lua_newuserdata(L, luaL_check_int(L, 1));
  return 1;
}

static int udataval (lua_State *L) {
  luaL_checktype(L, 1, LUA_TUSERDATA);
  lua_pushnumber(L, (int)lua_touserdata(L, 1));
  return 1;
}

static int newstate (lua_State *L) {
  lua_State *L1 = lua_open(luaL_check_int(L, 1));
  if (L1)
    lua_pushuserdata(L, L1);
  else
    lua_pushnil(L);
  return 1;
}

static int loadlib (lua_State *L) {
  lua_State *L1 = (lua_State *)lua_touserdata(L, 1);
  switch (*luaL_check_string(L, 2)) {
    case 'm': lua_mathlibopen(L1); break;
    case 's': lua_strlibopen(L1); break;
    case 'i': lua_iolibopen(L1); break;
    case 'd': lua_dblibopen(L1); break;
    case 'b': lua_baselibopen(L1); break;
    default: luaL_argerror(L, 2, "invalid option");
  }
  return 0;
}

static int closestate (lua_State *L) {
  luaL_checktype(L, 1, LUA_TUSERDATA);
  lua_close((lua_State *)lua_touserdata(L, 1));
  return 0;
}

static int doremote (lua_State *L) {
  lua_State *L1;
  const char *code = luaL_check_string(L, 2);
  int status;
  luaL_checktype(L, 1, LUA_TUSERDATA);
  L1 = (lua_State *)lua_touserdata(L, 1);
  status = lua_dostring(L1, code);
  if (status != 0) {
    lua_pushnil(L);
    lua_pushnumber(L, status);
    return 2;
  }
  else {
    int i = 0;
    while (!lua_isnull(L1, ++i))
      lua_pushstring(L, lua_tostring(L1, i));
    return i-1;
  }
}

static int settagmethod (lua_State *L) {
  int tag = luaL_check_int(L, 1);
  const char *event = luaL_check_string(L, 2);
  luaL_checkany(L, 3);
  lua_gettagmethod(L, tag, event);
  lua_pushvalue(L, 3);
  lua_settagmethod(L, tag, event);
  return 1;
}

static int pushbool (lua_State *L, int b) {
  if (b) lua_pushnumber(L, 1);
  else lua_pushnil(L);
  return 1;
}

static int equal (lua_State *L) {
  return pushbool(L, lua_equal(L, 1, 2));
}

  

/*
** {======================================================
** function to test the API with C. It interprets a kind of "assembler"
** language with calls to the API, so the test can be driven by Lua code
** =======================================================
*/

static const char *const delimits = " \t\n,;";

static void skip (const char **pc) {
  while (**pc != '\0' && strchr(delimits, **pc)) (*pc)++;
}

static int getnum (lua_State *L, const char **pc) {
  int res = 0;
  int sig = 1;
  skip(pc);
  if (**pc == '.') {
    res = (int)lua_tonumber(L, -1);
    lua_pop(L, 1);
    (*pc)++;
    return res;
  }
  else if (**pc == '-') {
    sig = -1;
    (*pc)++;
  }
  while (isdigit(**pc)) res = res*10 + (*(*pc)++) - '0';
  return sig*res;
}
  
static const char *test_getname (char *buff, const char **pc) {
  int i = 0;
  skip(pc);
  while (**pc != '\0' && !strchr(delimits, **pc))
    buff[i++] = *(*pc)++;
  buff[i] = '\0';
  return buff;
}


#define EQ(s1)	(strcmp(s1, inst) == 0)

#define getnum	((getnum)(L, &pc))
#define getname	((test_getname)(buff, &pc))


static int testC (lua_State *L) {
  char buff[30];
  const char *pc = luaL_check_string(L, 1);
  for (;;) {
    const char *inst = getname;
    if EQ("") return 0;
    else if EQ("isnumber") {
      lua_pushnumber(L, lua_isnumber(L, getnum));
    }
    else if EQ("isstring") {
      lua_pushnumber(L, lua_isstring(L, getnum));
    }
    else if EQ("istable") {
      lua_pushnumber(L, lua_istable(L, getnum));
    }
    else if EQ("iscfunction") {
      lua_pushnumber(L, lua_iscfunction(L, getnum));
    }
    else if EQ("isfunction") {
      lua_pushnumber(L, lua_isfunction(L, getnum));
    }
    else if EQ("isuserdata") {
      lua_pushnumber(L, lua_isuserdata(L, getnum));
    }
    else if EQ("isnil") {
      lua_pushnumber(L, lua_isnil(L, getnum));
    }
    else if EQ("isnull") {
      lua_pushnumber(L, lua_isnull(L, getnum));
    }
    else if EQ("tonumber") {
      lua_pushnumber(L, lua_tonumber(L, getnum));
    }
    else if EQ("tostring") {
      lua_pushstring(L, lua_tostring(L, getnum));
    }
    else if EQ("tonumber") {
      lua_pushnumber(L, lua_tonumber(L, getnum));
    }
    else if EQ("strlen") {
      lua_pushnumber(L, lua_strlen(L, getnum));
    }
    else if EQ("tocfunction") {
      lua_pushcfunction(L, lua_tocfunction(L, getnum));
    }
    else if EQ("return") {
      return getnum;
    }
    else if EQ("gettop") {
      lua_pushnumber(L, lua_gettop(L));
    }
    else if EQ("settop") {
      lua_settop(L, getnum);
    }
    else if EQ("pop") {
      lua_pop(L, getnum);
    }
    else if EQ("pushnum") {
      lua_pushnumber(L, getnum);
    }
    else if EQ("pushvalue") {
      lua_pushvalue(L, getnum);
    }
    else if EQ("remove") {
      lua_remove(L, getnum);
    }
    else if EQ("insert") {
      lua_insert(L, getnum);
    }
    else if EQ("gettable") {
      lua_gettable(L, getnum);
    }
    else if EQ("settable") {
      lua_settable(L, getnum);
    }
    else if EQ("next") {
      lua_next(L, -2);
    }
    else if EQ("concat") {
      lua_concat(L, getnum);
    }
    else if EQ("rawcall") {
      int narg = getnum;
      int nres = getnum;
      lua_rawcall(L, narg, nres);
    }
    else if EQ("call") {
      int narg = getnum;
      int nres = getnum;
      lua_call(L, narg, nres);
    }
    else if EQ("dostring") {
      lua_dostring(L, luaL_check_string(L, getnum));
    }
    else if EQ("settagmethod") {
      int tag = getnum;
      const char *event = getname;
      lua_settagmethod(L, tag, event);
    }
    else if EQ("gettagmethod") {
      int tag = getnum;
      const char *event = getname;
      lua_gettagmethod(L, tag, event);
    }
    else if EQ("type") {
      lua_pushstring(L, lua_typename(L, lua_type(L, getnum)));
    }
    else luaL_verror(L, "unknown instruction %.30s", buff);
  }
  return 0;
}

/* }====================================================== */



static const struct luaL_reg tests_funcs[] = {
  {"hash", hash_query},
  {"limits", get_limits},
  {"listcode", listcode},
  {"liststrings", liststrings},
  {"listlocals", listlocals},
  {"loadlib", loadlib},
  {"querystr", string_query},
  {"querytab", table_query},
  {"testC", testC},
  {"ref", tref},
  {"getref", getref},
  {"unref", unref},
  {"newuserdata", newuserdata},
  {"udataval", udataval},
  {"newstate", newstate},
  {"closestate", closestate},
  {"doremote", doremote},
  {"settagmethod", settagmethod},
  {"equal", equal},
  {"totalmem", mem_query}
};


void luaB_opentests (lua_State *L) {
  lua_newtable(L);
  lua_getglobals(L);
  lua_pushvalue(L, -2);
  lua_setglobals(L);
  luaL_openl(L, tests_funcs);  /* open functions inside new table */
  lua_setglobals(L);  /* restore old table of globals */
  lua_setglobal(L, "T");  /* set new table as global T */
}

#endif
/* resumed: mluxsys.c */
#endif

/* include: ltm.c */
/*
** $Id: ltm.c,v 1.56 2000/10/31 13:10:24 roberto Exp $
** Tag methods
** See Copyright Notice in lua.h
*/


#include <stdio.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */


const char *const luaT_eventname[] = {  /* ORDER TM */
  "gettable", "settable", "index", "getglobal", "setglobal", "add", "sub",
  "mul", "div", "pow", "unm", "lt", "concat", "gc", "function",
  "le", "gt", "ge",  /* deprecated options!! */
  NULL
};


static int findevent (const char *name) {
  int i;
  for (i=0; luaT_eventname[i]; i++)
    if (strcmp(luaT_eventname[i], name) == 0)
      return i;
  return -1;  /* name not found */
}


static int luaI_checkevent (lua_State *L, const char *name, int t) {
  int e = findevent(name);
  if (e >= TM_N)
    luaO_verror(L, "event `%.50s' is deprecated", name);
  if (e == TM_GC && t == LUA_TTABLE)
    luaO_verror(L, "event `gc' for tables is deprecated");
  if (e < 0)
    luaO_verror(L, "`%.50s' is not a valid event name", name);
  return e;
}



/* events in LUA_TNIL are all allowed, since this is used as a
*  'placeholder' for "default" fallbacks
*/
/* ORDER LUA_T, ORDER TM */
static const char luaT_validevents[NUM_TAGS][TM_N] = {
  {1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1},  /* LUA_TUSERDATA */
  {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1},  /* LUA_TNIL */
  {1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1},  /* LUA_TNUMBER */
  {1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1},  /* LUA_TSTRING */
  {0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1},  /* LUA_TTABLE */
  {1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0}   /* LUA_TFUNCTION */
};

int luaT_validevent (int t, int e) {  /* ORDER LUA_T */
  return (t >= NUM_TAGS) ?  1 : luaT_validevents[t][e];
}


static void init_entry (lua_State *L, int tag) {
  int i;
  for (i=0; i<TM_N; i++)
    luaT_gettm(L, tag, i) = NULL;
  L->TMtable[tag].collected = NULL;
}


void luaT_init (lua_State *L) {
  int t;
  luaM_growvector(L, L->TMtable, 0, NUM_TAGS, struct TM, "", MAX_INT);
  L->nblocks += NUM_TAGS*sizeof(struct TM);
  L->last_tag = NUM_TAGS-1;
  for (t=0; t<=L->last_tag; t++)
    init_entry(L, t);
}


LUA_API int lua_newtag (lua_State *L) {
  luaM_growvector(L, L->TMtable, L->last_tag, 1, struct TM,
                  "tag table overflow", MAX_INT);
  L->nblocks += sizeof(struct TM);
  L->last_tag++;
  init_entry(L, L->last_tag);
  return L->last_tag;
}


static void checktag (lua_State *L, int tag) {
  if (!(0 <= tag && tag <= L->last_tag))
    luaO_verror(L, "%d is not a valid tag", tag);
}

void luaT_realtag (lua_State *L, int tag) {
  if (!validtag(tag))
    luaO_verror(L, "tag %d was not created by `newtag'", tag);
}


LUA_API int lua_copytagmethods (lua_State *L, int tagto, int tagfrom) {
  int e;
  checktag(L, tagto);
  checktag(L, tagfrom);
  for (e=0; e<TM_N; e++) {
    if (luaT_validevent(tagto, e))
      luaT_gettm(L, tagto, e) = luaT_gettm(L, tagfrom, e);
  }
  return tagto;
}


int luaT_tag (const TObject *o) {
  int t = ttype(o);
  switch (t) {
    case LUA_TUSERDATA: return tsvalue(o)->u.d.tag;
    case LUA_TTABLE:    return hvalue(o)->htag;
    default:            return t;
  }
}


LUA_API void lua_gettagmethod (lua_State *L, int t, const char *event) {
  int e;
  e = luaI_checkevent(L, event, t);
  checktag(L, t);
  if (luaT_validevent(t, e) && luaT_gettm(L, t, e)) {
    clvalue(L->top) = luaT_gettm(L, t, e);
    ttype(L->top) = LUA_TFUNCTION;
  }
  else
    ttype(L->top) = LUA_TNIL;
  incr_top;
}


LUA_API void lua_settagmethod (lua_State *L, int t, const char *event) {
  int e = luaI_checkevent(L, event, t);
  checktag(L, t);
  if (!luaT_validevent(t, e))
    luaO_verror(L, "cannot change `%.20s' tag method for type `%.20s'%.20s",
                luaT_eventname[e], luaO_typenames[t],
                (t == LUA_TTABLE || t == LUA_TUSERDATA) ?
                   " with default tag" : "");
  switch (ttype(L->top - 1)) {
    case LUA_TNIL:
      luaT_gettm(L, t, e) = NULL;
      break;
    case LUA_TFUNCTION:
      luaT_gettm(L, t, e) = clvalue(L->top - 1);
      break;
    default:
      lua_error(L, "tag method must be a function (or nil)");
  }
  L->top--;
}

/* resumed: mluxsys.c */
/* include: lundump.c */
/*
** $Id: lundump.c,v 1.33 2000/10/31 16:57:23 lhf Exp $
** load bytecodes from files
** See Copyright Notice in lua.h
*/

#include <stdio.h>
#include <string.h>

/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lmem.h - see lua-4.0/src/lapi.c */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: lundump.h - see lua-4.0/src/ldo.c */

#define	LoadByte		ezgetc

static const char* ZNAME (ZIO* Z)
{
 const char* s=zname(Z);
 return (*s=='@') ? s+1 : s;
}

static void unexpectedEOZ (lua_State* L, ZIO* Z)
{
 luaO_verror(L,"unexpected end of file in `%.99s'",ZNAME(Z));
}

static int ezgetc (lua_State* L, ZIO* Z)
{
 int c=zgetc(Z);
 if (c==EOZ) unexpectedEOZ(L,Z);
 return c;
}

static void ezread (lua_State* L, ZIO* Z, void* b, int n)
{
 int r=zread(Z,b,n);
 if (r!=0) unexpectedEOZ(L,Z);
}

static void LoadBlock (lua_State* L, void* b, size_t size, ZIO* Z, int swap)
{
 if (swap)
 {
  char *p=(char *) b+size-1;
  int n=size;
  while (n--) *p--=(char)ezgetc(L,Z);
 }
 else
  ezread(L,Z,b,size);
}

static void LoadVector (lua_State* L, void* b, int m, size_t size, ZIO* Z, int swap)
{
 if (swap)
 {
  char *q=(char *) b;
  while (m--)
  {
   char *p=q+size-1;
   int n=size;
   while (n--) *p--=(char)ezgetc(L,Z);
   q+=size;
  }
 }
 else
  ezread(L,Z,b,m*size);
}

static int LoadInt (lua_State* L, ZIO* Z, int swap)
{
 int x;
 LoadBlock(L,&x,sizeof(x),Z,swap);
 return x;
}

static size_t LoadSize (lua_State* L, ZIO* Z, int swap)
{
 size_t x;
 LoadBlock(L,&x,sizeof(x),Z,swap);
 return x;
}

static Number LoadNumber (lua_State* L, ZIO* Z, int swap)
{
 Number x;
 LoadBlock(L,&x,sizeof(x),Z,swap);
 return x;
}

static TString* LoadString (lua_State* L, ZIO* Z, int swap)
{
 size_t size=LoadSize(L,Z,swap);
 if (size==0)
  return NULL;
 else
 {
  char* s=luaO_openspace(L,size);
  LoadBlock(L,s,size,Z,0);
  return luaS_newlstr(L,s,size-1);	/* remove trailing '\0' */
 }
}

static void LoadCode (lua_State* L, Proto* tf, ZIO* Z, int swap)
{
 int size=LoadInt(L,Z,swap);
 tf->code=luaM_newvector(L,size,Instruction);
 LoadVector(L,tf->code,size,sizeof(*tf->code),Z,swap);
 if (tf->code[size-1]!=OP_END) luaO_verror(L,"bad code in `%.99s'",ZNAME(Z));
 luaF_protook(L,tf,size);
}

static void LoadLocals (lua_State* L, Proto* tf, ZIO* Z, int swap)
{
 int i,n;
 tf->nlocvars=n=LoadInt(L,Z,swap);
 tf->locvars=luaM_newvector(L,n,LocVar);
 for (i=0; i<n; i++)
 {
  tf->locvars[i].varname=LoadString(L,Z,swap);
  tf->locvars[i].startpc=LoadInt(L,Z,swap);
  tf->locvars[i].endpc=LoadInt(L,Z,swap);
 }
}

static void LoadLines (lua_State* L, Proto* tf, ZIO* Z, int swap)
{
 int n;
 tf->nlineinfo=n=LoadInt(L,Z,swap);
 tf->lineinfo=luaM_newvector(L,n,int);
 LoadVector(L,tf->lineinfo,n,sizeof(*tf->lineinfo),Z,swap);
}

static Proto* LoadFunction (lua_State* L, ZIO* Z, int swap);

static void LoadConstants (lua_State* L, Proto* tf, ZIO* Z, int swap)
{
 int i,n;
 tf->nkstr=n=LoadInt(L,Z,swap);
 tf->kstr=luaM_newvector(L,n,TString*);
 for (i=0; i<n; i++)
  tf->kstr[i]=LoadString(L,Z,swap);
 tf->nknum=n=LoadInt(L,Z,swap);
 tf->knum=luaM_newvector(L,n,Number);
 LoadVector(L,tf->knum,n,sizeof(*tf->knum),Z,swap);
 tf->nkproto=n=LoadInt(L,Z,swap);
 tf->kproto=luaM_newvector(L,n,Proto*);
 for (i=0; i<n; i++)
  tf->kproto[i]=LoadFunction(L,Z,swap);
}

static Proto* LoadFunction (lua_State* L, ZIO* Z, int swap)
{
 Proto* tf=luaF_newproto(L);
 tf->source=LoadString(L,Z,swap);
 tf->lineDefined=LoadInt(L,Z,swap);
 tf->numparams=LoadInt(L,Z,swap);
 tf->is_vararg=LoadByte(L,Z);
 tf->maxstacksize=LoadInt(L,Z,swap);
 LoadLocals(L,tf,Z,swap);
 LoadLines(L,tf,Z,swap);
 LoadConstants(L,tf,Z,swap);
 LoadCode(L,tf,Z,swap);
 return tf;
}

static void LoadSignature (lua_State* L, ZIO* Z)
{
 const char* s=SIGNATURE;
 while (*s!=0 && ezgetc(L,Z)==*s)
  ++s;
 if (*s!=0) luaO_verror(L,"bad signature in `%.99s'",ZNAME(Z));
}

static void TestSize (lua_State* L, int s, const char* what, ZIO* Z)
{
 int r=ezgetc(L,Z);
 if (r!=s)
  luaO_verror(L,"virtual machine mismatch in `%.99s':\n"
	"  %.20s is %d but read %d",ZNAME(Z),what,s,r);
}

#define TESTSIZE(s)	TestSize(L,s,#s,Z)
#define V(v)	v/16,v%16

static int LoadHeader (lua_State* L, ZIO* Z)
{
 int version,swap;
 Number f=0,tf=TEST_NUMBER;
 LoadSignature(L,Z);
 version=ezgetc(L,Z);
 if (version>VERSION)
  luaO_verror(L,"`%.99s' too new:\n"
	"  read version %d.%d; expected at most %d.%d",
	ZNAME(Z),V(version),V(VERSION));
 if (version<VERSION0)			/* check last major change */
  luaO_verror(L,"`%.99s' too old:\n"
	"  read version %d.%d; expected at least %d.%d",
	ZNAME(Z),V(version),V(VERSION));
 swap=(luaU_endianess()!=ezgetc(L,Z));	/* need to swap bytes? */
 TESTSIZE(sizeof(int));
 TESTSIZE(sizeof(size_t));
 TESTSIZE(sizeof(Instruction));
 TESTSIZE(SIZE_INSTRUCTION);
 TESTSIZE(SIZE_OP);
 TESTSIZE(SIZE_B);
 TESTSIZE(sizeof(Number));
 f=LoadNumber(L,Z,swap);
 if ((long)f!=(long)tf)		/* disregard errors in last bit of fraction */
  luaO_verror(L,"unknown number format in `%.99s':\n"
      "  read " NUMBER_FMT "; expected " NUMBER_FMT, ZNAME(Z),f,tf);
 return swap;
}

static Proto* LoadChunk (lua_State* L, ZIO* Z)
{
 return LoadFunction(L,Z,LoadHeader(L,Z));
}

/*
** load one chunk from a file or buffer
** return main if ok and NULL at EOF
*/
Proto* luaU_undump (lua_State* L, ZIO* Z)
{
 Proto* tf=NULL;
 int c=zgetc(Z);
 if (c==ID_CHUNK)
  tf=LoadChunk(L,Z);
 c=zgetc(Z);
 if (c!=EOZ)
  luaO_verror(L,"`%.99s' apparently contains more than one chunk",ZNAME(Z));
 return tf;
}

/*
** find byte order
*/
int luaU_endianess (void)
{
 int x=1;
 return *(char*)&x;
}
/* resumed: mluxsys.c */
/* include: lvm.c */
/*
** $Id: lvm.c,v 1.146 2000/10/26 12:47:05 roberto Exp $
** Lua virtual machine
** See Copyright Notice in lua.h
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lapi.h - see lua-4.0/src/lapi.c */
/* skipped: ldebug.h - see lua-4.0/src/ldebug.c */
/* skipped: ldo.h - see lua-4.0/src/lapi.c */
/* skipped: lfunc.h - see lua-4.0/src/lapi.c */
/* skipped: lgc.h - see lua-4.0/src/lapi.c */
/* skipped: lobject.h - see lua-4.0/src/lapi.h */
/* skipped: lopcodes.h - see lua-4.0/src/lcode.h */
/* skipped: lstate.h - see lua-4.0/src/ldo.h */
/* skipped: lstring.h - see lua-4.0/src/lapi.c */
/* skipped: ltable.h - see lua-4.0/src/lapi.c */
/* skipped: ltm.h - see lua-4.0/src/lapi.c */
/* skipped: lvm.h - see lua-4.0/src/lapi.c */


#ifdef OLD_ANSI
#define strcoll(a,b)	strcmp(a,b)
#endif



/*
** Extra stack size to run a function:
** TAG_LINE(1), NAME(1), TM calls(3) (plus some extra...)
*/
#define	EXTRA_STACK	8



int luaV_tonumber (TObject *obj) {
  if (ttype(obj) != LUA_TSTRING)
    return 1;
  else {
    if (!luaO_str2d(svalue(obj), &nvalue(obj)))
      return 2;
    ttype(obj) = LUA_TNUMBER;
    return 0;
  }
}


int luaV_tostring (lua_State *L, TObject *obj) {  /* LUA_NUMBER */
  if (ttype(obj) != LUA_TNUMBER)
    return 1;
  else {
    char s[32];  /* 16 digits, sign, point and \0  (+ some extra...) */
    lua_number2str(s, nvalue(obj));  /* convert `s' to number */
    tsvalue(obj) = luaS_new(L, s);
    ttype(obj) = LUA_TSTRING;
    return 0;
  }
}


static void traceexec (lua_State *L, StkId base, StkId top, lua_Hook linehook) {
  CallInfo *ci = infovalue(base-1);
  int *lineinfo = ci->func->f.l->lineinfo;
  int pc = (*ci->pc - ci->func->f.l->code) - 1;
  int newline;
  if (pc == 0) {  /* may be first time? */
    ci->line = 1;
    ci->refi = 0;
    ci->lastpc = pc+1;  /* make sure it will call linehook */
  }
  newline = luaG_getline(lineinfo, pc, ci->line, &ci->refi);
  /* calls linehook when enters a new line or jumps back (loop) */
  if (newline != ci->line || pc <= ci->lastpc) {
    ci->line = newline;
    L->top = top;
    luaD_lineHook(L, base-2, newline, linehook);
  }
  ci->lastpc = pc;
}


static Closure *luaV_closure (lua_State *L, int nelems) {
  Closure *c = luaF_newclosure(L, nelems);
  L->top -= nelems;
  while (nelems--)
    c->upvalue[nelems] = *(L->top+nelems);
  clvalue(L->top) = c;
  ttype(L->top) = LUA_TFUNCTION;
  incr_top;
  return c;
}


void luaV_Cclosure (lua_State *L, lua_CFunction c, int nelems) {
  Closure *cl = luaV_closure(L, nelems);
  cl->f.c = c;
  cl->isC = 1;
}


void luaV_Lclosure (lua_State *L, Proto *l, int nelems) {
  Closure *cl = luaV_closure(L, nelems);
  cl->f.l = l;
  cl->isC = 0;
}


/*
** Function to index a table.
** Receives the table at `t' and the key at top.
*/
const TObject *luaV_gettable (lua_State *L, StkId t) {
  Closure *tm;
  int tg;
  if (ttype(t) == LUA_TTABLE &&  /* `t' is a table? */
      ((tg = hvalue(t)->htag) == LUA_TTABLE ||  /* with default tag? */
        luaT_gettm(L, tg, TM_GETTABLE) == NULL)) { /* or no TM? */
    /* do a primitive get */
    const TObject *h = luaH_get(L, hvalue(t), L->top-1);
    /* result is no nil or there is no `index' tag method? */
    if (ttype(h) != LUA_TNIL || ((tm=luaT_gettm(L, tg, TM_INDEX)) == NULL))
      return h;  /* return result */
    /* else call `index' tag method */
  }
  else {  /* try a `gettable' tag method */
    tm = luaT_gettmbyObj(L, t, TM_GETTABLE);
  }
  if (tm != NULL) {  /* is there a tag method? */
    luaD_checkstack(L, 2);
    *(L->top+1) = *(L->top-1);  /* key */
    *L->top = *t;  /* table */
    clvalue(L->top-1) = tm;  /* tag method */
    ttype(L->top-1) = LUA_TFUNCTION;
    L->top += 2;
    luaD_call(L, L->top - 3, 1);
    return L->top - 1;  /* call result */
  }
  else {  /* no tag method */
    luaG_typeerror(L, t, "index");
    return NULL;  /* to avoid warnings */
  }
}


/*
** Receives table at `t', key at `key' and value at top.
*/
void luaV_settable (lua_State *L, StkId t, StkId key) {
  int tg;
  if (ttype(t) == LUA_TTABLE &&  /* `t' is a table? */
      ((tg = hvalue(t)->htag) == LUA_TTABLE ||  /* with default tag? */
        luaT_gettm(L, tg, TM_SETTABLE) == NULL)) /* or no TM? */
    *luaH_set(L, hvalue(t), key) = *(L->top-1);  /* do a primitive set */
  else {  /* try a `settable' tag method */
    Closure *tm = luaT_gettmbyObj(L, t, TM_SETTABLE);
    if (tm != NULL) {
      luaD_checkstack(L, 3);
      *(L->top+2) = *(L->top-1);
      *(L->top+1) = *key;
      *(L->top) = *t;
      clvalue(L->top-1) = tm;
      ttype(L->top-1) = LUA_TFUNCTION;
      L->top += 3;
      luaD_call(L, L->top - 4, 0);  /* call `settable' tag method */
    }
    else  /* no tag method... */
      luaG_typeerror(L, t, "index");
  }
}


const TObject *luaV_getglobal (lua_State *L, TString *s) {
  const TObject *value = luaH_getstr(L->gt, s);
  Closure *tm = luaT_gettmbyObj(L, value, TM_GETGLOBAL);
  if (tm == NULL)  /* is there a tag method? */
    return value;  /* default behavior */
  else {  /* tag method */
    luaD_checkstack(L, 3);
    clvalue(L->top) = tm;
    ttype(L->top) = LUA_TFUNCTION;
    tsvalue(L->top+1) = s;  /* global name */
    ttype(L->top+1) = LUA_TSTRING;
    *(L->top+2) = *value;
    L->top += 3;
    luaD_call(L, L->top - 3, 1);
    return L->top - 1;
  }
}


void luaV_setglobal (lua_State *L, TString *s) {
  const TObject *oldvalue = luaH_getstr(L->gt, s);
  Closure *tm = luaT_gettmbyObj(L, oldvalue, TM_SETGLOBAL);
  if (tm == NULL) {  /* is there a tag method? */
    if (oldvalue != &luaO_nilobject) {
      /* cast to remove `const' is OK, because `oldvalue' != luaO_nilobject */
      *(TObject *)oldvalue = *(L->top - 1);
    }
    else {
      TObject key;
      ttype(&key) = LUA_TSTRING;
      tsvalue(&key) = s;
      *luaH_set(L, L->gt, &key) = *(L->top - 1);
    }
  }
  else {
    luaD_checkstack(L, 3);
    *(L->top+2) = *(L->top-1);  /* new value */
    *(L->top+1) = *oldvalue;
    ttype(L->top) = LUA_TSTRING;
    tsvalue(L->top) = s;
    clvalue(L->top-1) = tm;
    ttype(L->top-1) = LUA_TFUNCTION;
    L->top += 3;
    luaD_call(L, L->top - 4, 0);
  }
}


static int call_binTM (lua_State *L, StkId top, TMS event) {
  /* try first operand */
  Closure *tm = luaT_gettmbyObj(L, top-2, event);
  L->top = top;
  if (tm == NULL) {
    tm = luaT_gettmbyObj(L, top-1, event);  /* try second operand */
    if (tm == NULL) {
      tm = luaT_gettm(L, 0, event);  /* try a `global' method */
      if (tm == NULL)
        return 0;  /* error */
    }
  }
  lua_pushstring(L, luaT_eventname[event]);
  luaD_callTM(L, tm, 3, 1);
  return 1;
}


static void call_arith (lua_State *L, StkId top, TMS event) {
  if (!call_binTM(L, top, event))
    luaG_binerror(L, top-2, LUA_TNUMBER, "perform arithmetic on");
}


static int luaV_strcomp (const TString *ls, const TString *rs) {
  const char *l = ls->str;
  size_t ll = ls->len;
  const char *r = rs->str;
  size_t lr = rs->len;
  for (;;) {
    int temp = strcoll(l, r);
    if (temp != 0) return temp;
    else {  /* strings are equal up to a '\0' */
      size_t len = strlen(l);  /* index of first '\0' in both strings */
      if (len == ll)  /* l is finished? */
        return (len == lr) ? 0 : -1;  /* l is equal or smaller than r */
      else if (len == lr)  /* r is finished? */
        return 1;  /* l is greater than r (because l is not finished) */
      /* both strings longer than `len'; go on comparing (after the '\0') */
      len++;
      l += len; ll -= len; r += len; lr -= len;
    }
  }
}


int luaV_lessthan (lua_State *L, const TObject *l, const TObject *r, StkId top) {
  if (ttype(l) == LUA_TNUMBER && ttype(r) == LUA_TNUMBER)
    return (nvalue(l) < nvalue(r));
  else if (ttype(l) == LUA_TSTRING && ttype(r) == LUA_TSTRING)
    return (luaV_strcomp(tsvalue(l), tsvalue(r)) < 0);
  else {  /* call TM */
    luaD_checkstack(L, 2);
    *top++ = *l;
    *top++ = *r;
    if (!call_binTM(L, top, TM_LT))
      luaG_ordererror(L, top-2);
    L->top--;
    return (ttype(L->top) != LUA_TNIL);
  }
}


void luaV_strconc (lua_State *L, int total, StkId top) {
  do {
    int n = 2;  /* number of elements handled in this pass (at least 2) */
    if (tostring(L, top-2) || tostring(L, top-1)) {
      if (!call_binTM(L, top, TM_CONCAT))
        luaG_binerror(L, top-2, LUA_TSTRING, "concat");
    }
    else if (tsvalue(top-1)->len > 0) {  /* if len=0, do nothing */
      /* at least two string values; get as many as possible */
      lint32 tl = (lint32)tsvalue(top-1)->len + 
                  (lint32)tsvalue(top-2)->len;
      char *buffer;
      int i;
      while (n < total && !tostring(L, top-n-1)) {  /* collect total length */
        tl += tsvalue(top-n-1)->len;
        n++;
      }
      if (tl > MAX_SIZET) lua_error(L, "string size overflow");
      buffer = luaO_openspace(L, tl);
      tl = 0;
      for (i=n; i>0; i--) {  /* concat all strings */
        size_t l = tsvalue(top-i)->len;
        memcpy(buffer+tl, tsvalue(top-i)->str, l);
        tl += l;
      }
      tsvalue(top-n) = luaS_newlstr(L, buffer, tl);
    }
    total -= n-1;  /* got `n' strings to create 1 new */
    top -= n-1;
  } while (total > 1);  /* repeat until only 1 result left */
}


static void luaV_pack (lua_State *L, StkId firstelem) {
  int i;
  Hash *htab = luaH_new(L, 0);
  for (i=0; firstelem+i<L->top; i++)
    *luaH_setint(L, htab, i+1) = *(firstelem+i);
  /* store counter in field `n' */
  luaH_setstrnum(L, htab, luaS_new(L, "n"), i);
  L->top = firstelem;  /* remove elements from the stack */
  ttype(L->top) = LUA_TTABLE;
  hvalue(L->top) = htab;
  incr_top;
}


static void adjust_varargs (lua_State *L, StkId base, int nfixargs) {
  int nvararg = (L->top-base) - nfixargs;
  if (nvararg < 0)
    luaD_adjusttop(L, base, nfixargs);
  luaV_pack(L, base+nfixargs);
}



#define dojump(pc, i)	{ int d = GETARG_S(i); pc += d; }

/*
** Executes the given Lua function. Parameters are between [base,top).
** Returns n such that the the results are between [n,top).
*/
StkId luaV_execute (lua_State *L, const Closure *cl, StkId base) {
  const Proto *const tf = cl->f.l;
  StkId top;  /* keep top local, for performance */
  const Instruction *pc = tf->code;
  TString **const kstr = tf->kstr;
  const lua_Hook linehook = L->linehook;
  infovalue(base-1)->pc = &pc;
  luaD_checkstack(L, tf->maxstacksize+EXTRA_STACK);
  if (tf->is_vararg)  /* varargs? */
    adjust_varargs(L, base, tf->numparams);
  else
    luaD_adjusttop(L, base, tf->numparams);
  top = L->top;
  /* main loop of interpreter */
  for (;;) {
    const Instruction i = *pc++;
    if (linehook)
      traceexec(L, base, top, linehook);
    switch (GET_OPCODE(i)) {
      case OP_END: {
        L->top = top;
        return top;
      }
      case OP_RETURN: {
        L->top = top;
        return base+GETARG_U(i);
      }
      case OP_CALL: {
        int nres = GETARG_B(i);
        if (nres == MULT_RET) nres = LUA_MULTRET;
        L->top = top;
        luaD_call(L, base+GETARG_A(i), nres);
        top = L->top;
        break;
      }
      case OP_TAILCALL: {
        L->top = top;
        luaD_call(L, base+GETARG_A(i), LUA_MULTRET);
        return base+GETARG_B(i);
      }
      case OP_PUSHNIL: {
        int n = GETARG_U(i);
        LUA_ASSERT(n>0, "invalid argument");
        do {
          ttype(top++) = LUA_TNIL;
        } while (--n > 0);
        break;
      }
      case OP_POP: {
        top -= GETARG_U(i);
        break;
      }
      case OP_PUSHINT: {
        ttype(top) = LUA_TNUMBER;
        nvalue(top) = (Number)GETARG_S(i);
        top++;
        break;
      }
      case OP_PUSHSTRING: {
        ttype(top) = LUA_TSTRING;
        tsvalue(top) = kstr[GETARG_U(i)];
        top++;
        break;
      }
      case OP_PUSHNUM: {
        ttype(top) = LUA_TNUMBER;
        nvalue(top) = tf->knum[GETARG_U(i)];
        top++;
        break;
      }
      case OP_PUSHNEGNUM: {
        ttype(top) = LUA_TNUMBER;
        nvalue(top) = -tf->knum[GETARG_U(i)];
        top++;
        break;
      }
      case OP_PUSHUPVALUE: {
        *top++ = cl->upvalue[GETARG_U(i)];
        break;
      }
      case OP_GETLOCAL: {
        *top++ = *(base+GETARG_U(i));
        break;
      }
      case OP_GETGLOBAL: {
        L->top = top;
        *top = *luaV_getglobal(L, kstr[GETARG_U(i)]);
        top++;
        break;
      }
      case OP_GETTABLE: {
        L->top = top;
        top--;
        *(top-1) = *luaV_gettable(L, top-1);
        break;
      }
      case OP_GETDOTTED: {
        ttype(top) = LUA_TSTRING;
        tsvalue(top) = kstr[GETARG_U(i)];
        L->top = top+1;
        *(top-1) = *luaV_gettable(L, top-1);
        break;
      }
      case OP_GETINDEXED: {
        *top = *(base+GETARG_U(i));
        L->top = top+1;
        *(top-1) = *luaV_gettable(L, top-1);
        break;
      }
      case OP_PUSHSELF: {
        TObject receiver;
        receiver = *(top-1);
        ttype(top) = LUA_TSTRING;
        tsvalue(top++) = kstr[GETARG_U(i)];
        L->top = top;
        *(top-2) = *luaV_gettable(L, top-2);
        *(top-1) = receiver;
        break;
      }
      case OP_CREATETABLE: {
        L->top = top;
        luaC_checkGC(L);
        hvalue(top) = luaH_new(L, GETARG_U(i));
        ttype(top) = LUA_TTABLE;
        top++;
        break;
      }
      case OP_SETLOCAL: {
        *(base+GETARG_U(i)) = *(--top);
        break;
      }
      case OP_SETGLOBAL: {
        L->top = top;
        luaV_setglobal(L, kstr[GETARG_U(i)]);
        top--;
        break;
      }
      case OP_SETTABLE: {
        StkId t = top-GETARG_A(i);
        L->top = top;
        luaV_settable(L, t, t+1);
        top -= GETARG_B(i);  /* pop values */
        break;
      }
      case OP_SETLIST: {
        int aux = GETARG_A(i) * LFIELDS_PER_FLUSH;
        int n = GETARG_B(i);
        Hash *arr = hvalue(top-n-1);
        L->top = top-n;  /* final value of `top' (in case of errors) */
        for (; n; n--)
          *luaH_setint(L, arr, n+aux) = *(--top);
        break;
      }
      case OP_SETMAP: {
        int n = GETARG_U(i);
        StkId finaltop = top-2*n;
        Hash *arr = hvalue(finaltop-1);
        L->top = finaltop;  /* final value of `top' (in case of errors) */
        for (; n; n--) {
          top-=2;
          *luaH_set(L, arr, top) = *(top+1);
        }
        break;
      }
      case OP_ADD: {
        if (tonumber(top-2) || tonumber(top-1))
          call_arith(L, top, TM_ADD);
        else
          nvalue(top-2) += nvalue(top-1);
        top--;
        break;
      }
      case OP_ADDI: {
        if (tonumber(top-1)) {
          ttype(top) = LUA_TNUMBER;
          nvalue(top) = (Number)GETARG_S(i);
          call_arith(L, top+1, TM_ADD);
        }
        else
          nvalue(top-1) += (Number)GETARG_S(i);
        break;
      }
      case OP_SUB: {
        if (tonumber(top-2) || tonumber(top-1))
          call_arith(L, top, TM_SUB);
        else
          nvalue(top-2) -= nvalue(top-1);
        top--;
        break;
      }
      case OP_MULT: {
        if (tonumber(top-2) || tonumber(top-1))
          call_arith(L, top, TM_MUL);
        else
          nvalue(top-2) *= nvalue(top-1);
        top--;
        break;
      }
      case OP_DIV: {
        if (tonumber(top-2) || tonumber(top-1))
          call_arith(L, top, TM_DIV);
        else
          nvalue(top-2) /= nvalue(top-1);
        top--;
        break;
      }
      case OP_POW: {
        if (!call_binTM(L, top, TM_POW))
          lua_error(L, "undefined operation");
        top--;
        break;
      }
      case OP_CONCAT: {
        int n = GETARG_U(i);
        luaV_strconc(L, n, top);
        top -= n-1;
        L->top = top;
        luaC_checkGC(L);
        break;
      }
      case OP_MINUS: {
        if (tonumber(top-1)) {
          ttype(top) = LUA_TNIL;
          call_arith(L, top+1, TM_UNM);
        }
        else
          nvalue(top-1) = -nvalue(top-1);
        break;
      }
      case OP_NOT: {
        ttype(top-1) =
           (ttype(top-1) == LUA_TNIL) ? LUA_TNUMBER : LUA_TNIL;
        nvalue(top-1) = 1;
        break;
      }
      case OP_JMPNE: {
        top -= 2;
        if (!luaO_equalObj(top, top+1)) dojump(pc, i);
        break;
      }
      case OP_JMPEQ: {
        top -= 2;
        if (luaO_equalObj(top, top+1)) dojump(pc, i);
        break;
      }
      case OP_JMPLT: {
        top -= 2;
        if (luaV_lessthan(L, top, top+1, top+2)) dojump(pc, i);
        break;
      }
      case OP_JMPLE: {  /* a <= b  ===  !(b<a) */
        top -= 2;
        if (!luaV_lessthan(L, top+1, top, top+2)) dojump(pc, i);
        break;
      }
      case OP_JMPGT: {  /* a > b  ===  (b<a) */
        top -= 2;
        if (luaV_lessthan(L, top+1, top, top+2)) dojump(pc, i);
        break;
      }
      case OP_JMPGE: {  /* a >= b  ===  !(a<b) */
        top -= 2;
        if (!luaV_lessthan(L, top, top+1, top+2)) dojump(pc, i);
        break;
      }
      case OP_JMPT: {
        if (ttype(--top) != LUA_TNIL) dojump(pc, i);
        break;
      }
      case OP_JMPF: {
        if (ttype(--top) == LUA_TNIL) dojump(pc, i);
        break;
      }
      case OP_JMPONT: {
        if (ttype(top-1) == LUA_TNIL) top--;
        else dojump(pc, i);
        break;
      }
      case OP_JMPONF: {
        if (ttype(top-1) != LUA_TNIL) top--;
        else dojump(pc, i);
        break;
      }
      case OP_JMP: {
        dojump(pc, i);
        break;
      }
      case OP_PUSHNILJMP: {
        ttype(top++) = LUA_TNIL;
        pc++;
        break;
      }
      case OP_FORPREP: {
        if (tonumber(top-1))
          lua_error(L, "`for' step must be a number");
        if (tonumber(top-2))
          lua_error(L, "`for' limit must be a number");
        if (tonumber(top-3))
          lua_error(L, "`for' initial value must be a number");
        if (nvalue(top-1) > 0 ?
            nvalue(top-3) > nvalue(top-2) :
            nvalue(top-3) < nvalue(top-2)) {  /* `empty' loop? */
          top -= 3;  /* remove control variables */
          dojump(pc, i);  /* jump to loop end */
        }
        break;
      }
      case OP_FORLOOP: {
        LUA_ASSERT(ttype(top-1) == LUA_TNUMBER, "invalid step");
        LUA_ASSERT(ttype(top-2) == LUA_TNUMBER, "invalid limit");
        if (ttype(top-3) != LUA_TNUMBER)
          lua_error(L, "`for' index must be a number");
        nvalue(top-3) += nvalue(top-1);  /* increment index */
        if (nvalue(top-1) > 0 ?
            nvalue(top-3) > nvalue(top-2) :
            nvalue(top-3) < nvalue(top-2))
          top -= 3;  /* end loop: remove control variables */
        else
          dojump(pc, i);  /* repeat loop */
        break;
      }
      case OP_LFORPREP: {
        Node *node;
        if (ttype(top-1) != LUA_TTABLE)
          lua_error(L, "`for' table must be a table");
        node = luaH_next(L, hvalue(top-1), &luaO_nilobject);
        if (node == NULL) {  /* `empty' loop? */
          top--;  /* remove table */
          dojump(pc, i);  /* jump to loop end */
        }
        else {
          top += 2;  /* index,value */
          *(top-2) = *key(node);
          *(top-1) = *val(node);
        }
        break;
      }
      case OP_LFORLOOP: {
        Node *node;
        LUA_ASSERT(ttype(top-3) == LUA_TTABLE, "invalid table");
        node = luaH_next(L, hvalue(top-3), top-2);
        if (node == NULL)  /* end loop? */
          top -= 3;  /* remove table, key, and value */
        else {
          *(top-2) = *key(node);
          *(top-1) = *val(node);
          dojump(pc, i);  /* repeat loop */
        }
        break;
      }
      case OP_CLOSURE: {
        L->top = top;
        luaV_Lclosure(L, tf->kproto[GETARG_A(i)], GETARG_B(i));
        top = L->top;
        luaC_checkGC(L);
        break;
      }
    }
  }
}
/* resumed: mluxsys.c */
/* include: lzio.c */
/*
** $Id: lzio.c,v 1.13 2000/06/12 13:52:05 roberto Exp $
** a generic input stream interface
** See Copyright Notice in lua.h
*/



#include <stdio.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lzio.h - see lua-4.0/src/llex.h */



/* ----------------------------------------------------- memory buffers --- */

static int zmfilbuf (ZIO* z) {
  (void)z;  /* to avoid warnings */
  return EOZ;
}


ZIO* zmopen (ZIO* z, const char* b, size_t size, const char *name) {
  if (b==NULL) return NULL;
  z->n = size;
  z->p = (const unsigned char *)b;
  z->filbuf = zmfilbuf;
  z->u = NULL;
  z->name = name;
  return z;
}

/* ------------------------------------------------------------ strings --- */

ZIO* zsopen (ZIO* z, const char* s, const char *name) {
  if (s==NULL) return NULL;
  return zmopen(z, s, strlen(s), name);
}

/* -------------------------------------------------------------- FILEs --- */

static int zffilbuf (ZIO* z) {
  size_t n;
  if (feof((FILE *)z->u)) return EOZ;
  n = fread(z->buffer, 1, ZBSIZE, (FILE *)z->u);
  if (n==0) return EOZ;
  z->n = n-1;
  z->p = z->buffer;
  return *(z->p++);
}


ZIO* zFopen (ZIO* z, FILE* f, const char *name) {
  if (f==NULL) return NULL;
  z->n = 0;
  z->p = z->buffer;
  z->filbuf = zffilbuf;
  z->u = f;
  z->name = name;
  return z;
}


/* --------------------------------------------------------------- read --- */
size_t zread (ZIO *z, void *b, size_t n) {
  while (n) {
    size_t m;
    if (z->n == 0) {
      if (z->filbuf(z) == EOZ)
        return n;  /* return number of missing bytes */
      zungetc(z);  /* put result from `filbuf' in the buffer */
    }
    m = (n <= z->n) ? n : z->n;  /* min. between n and z->n */
    memcpy(b, z->p, m);
    z->n -= m;
    z->p += m;
    b = (char *)b + m;
    n -= m;
  }
  return 0;
}
/* resumed: mluxsys.c */

#ifndef MINIMAL
/* include: lauxlib.c */
/*
** $Id: lauxlib.c,v 1.43 2000/10/30 13:07:48 roberto Exp $
** Auxiliary functions for building Lua libraries
** See Copyright Notice in lua.h
*/


#include <stdarg.h>
#include <stdio.h>
#include <string.h>

/* This file uses only the official API of Lua.
** Any function declared here could be written as an application function.
** With care, these functions can be used by other libraries.
*/

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: luadebug.h - see mluxsys.c */



LUALIB_API int luaL_findstring (const char *name, const char *const list[]) {
  int i;
  for (i=0; list[i]; i++)
    if (strcmp(list[i], name) == 0)
      return i;
  return -1;  /* name not found */
}

LUALIB_API void luaL_argerror (lua_State *L, int narg, const char *extramsg) {
  lua_Debug ar;
  lua_getstack(L, 0, &ar);
  lua_getinfo(L, "n", &ar);
  if (ar.name == NULL)
    ar.name = "?";
  luaL_verror(L, "bad argument #%d to `%.50s' (%.100s)",
              narg, ar.name, extramsg);
}


static void type_error (lua_State *L, int narg, int t) {
  char buff[50];
  sprintf(buff, "%.8s expected, got %.8s", lua_typename(L, t),
                                           lua_typename(L, lua_type(L, narg)));
  luaL_argerror(L, narg, buff);
}


LUALIB_API void luaL_checkstack (lua_State *L, int space, const char *mes) {
  if (space > lua_stackspace(L))
    luaL_verror(L, "stack overflow (%.30s)", mes);
}


LUALIB_API void luaL_checktype(lua_State *L, int narg, int t) {
  if (lua_type(L, narg) != t)
    type_error(L, narg, t);
}


LUALIB_API void luaL_checkany (lua_State *L, int narg) {
  if (lua_type(L, narg) == LUA_TNONE)
    luaL_argerror(L, narg, "value expected");
}


LUALIB_API const char *luaL_check_lstr (lua_State *L, int narg, size_t *len) {
  const char *s = lua_tostring(L, narg);
  if (!s) type_error(L, narg, LUA_TSTRING);
  if (len) *len = lua_strlen(L, narg);
  return s;
}


LUALIB_API const char *luaL_opt_lstr (lua_State *L, int narg, const char *def, size_t *len) {
  if (lua_isnull(L, narg)) {
    if (len)
      *len = (def ? strlen(def) : 0);
    return def;
  }
  else return luaL_check_lstr(L, narg, len);
}


LUALIB_API double luaL_check_number (lua_State *L, int narg) {
  double d = lua_tonumber(L, narg);
  if (d == 0 && !lua_isnumber(L, narg))  /* avoid extra test when d is not 0 */
    type_error(L, narg, LUA_TNUMBER);
  return d;
}


LUALIB_API double luaL_opt_number (lua_State *L, int narg, double def) {
  if (lua_isnull(L, narg)) return def;
  else return luaL_check_number(L, narg);
}


LUALIB_API void luaL_openlib (lua_State *L, const struct luaL_reg *l, int n) {
  int i;
  for (i=0; i<n; i++)
    lua_register(L, l[i].name, l[i].func);
}


LUALIB_API void luaL_verror (lua_State *L, const char *fmt, ...) {
  char buff[500];
  va_list argp;
  va_start(argp, fmt);
  vsprintf(buff, fmt, argp);
  va_end(argp);
  lua_error(L, buff);
}


/*
** {======================================================
** Generic Buffer manipulation
** =======================================================
*/


#define buffempty(B)	((B)->p == (B)->buffer)
#define bufflen(B)	((B)->p - (B)->buffer)
#define bufffree(B)	((size_t)(LUAL_BUFFERSIZE - bufflen(B)))

#define LIMIT	(LUA_MINSTACK/2)


static int emptybuffer (luaL_Buffer *B) {
  size_t l = bufflen(B);
  if (l == 0) return 0;  /* put nothing on stack */
  else {
    lua_pushlstring(B->L, B->buffer, l);
    B->p = B->buffer;
    B->level++;
    return 1;
  }
}


static void adjuststack (luaL_Buffer *B) {
  if (B->level > 1) {
    lua_State *L = B->L;
    int toget = 1;  /* number of levels to concat */
    size_t toplen = lua_strlen(L, -1);
    do {
      size_t l = lua_strlen(L, -(toget+1));
      if (B->level - toget + 1 >= LIMIT || toplen > l) {
        toplen += l;
        toget++;
      }
      else break;
    } while (toget < B->level);
    if (toget >= 2) {
      lua_concat(L, toget);
      B->level = B->level - toget + 1;
    }
  }
}


LUALIB_API char *luaL_prepbuffer (luaL_Buffer *B) {
  if (emptybuffer(B))
    adjuststack(B);
  return B->buffer;
}


LUALIB_API void luaL_addlstring (luaL_Buffer *B, const char *s, size_t l) {
  while (l--)
    luaL_putchar(B, *s++);
}


LUALIB_API void luaL_addstring (luaL_Buffer *B, const char *s) {
  luaL_addlstring(B, s, strlen(s));
}


LUALIB_API void luaL_pushresult (luaL_Buffer *B) {
  emptybuffer(B);
  if (B->level == 0)
    lua_pushlstring(B->L, NULL, 0);
  else if (B->level > 1)
    lua_concat(B->L, B->level);
  B->level = 1;
}


LUALIB_API void luaL_addvalue (luaL_Buffer *B) {
  lua_State *L = B->L;
  size_t vl = lua_strlen(L, -1);
  if (vl <= bufffree(B)) {  /* fit into buffer? */
    memcpy(B->p, lua_tostring(L, -1), vl);  /* put it there */
    B->p += vl;
    lua_pop(L, 1);  /* remove from stack */
  }
  else {
    if (emptybuffer(B))
      lua_insert(L, -2);  /* put buffer before new value */
    B->level++;  /* add new value into B stack */
    adjuststack(B);
  }
}


LUALIB_API void luaL_buffinit (lua_State *L, luaL_Buffer *B) {
  B->L = L;
  B->p = B->buffer;
  B->level = 0;
}

/* }====================================================== */
/* resumed: mluxsys.c */
/* include: lbaselib.c */
/*
** $Id: lbaselib.c,v 1.17 2000/11/06 13:45:18 roberto Exp $
** Basic library
** See Copyright Notice in lua.h
*/



#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: luadebug.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */



/*
** If your system does not support `stderr', redefine this function, or
** redefine _ERRORMESSAGE so that it won't need _ALERT.
*/
static int luaB__ALERT (lua_State *L) {
  fputs(luaL_check_string(L, 1), stderr);
  return 0;
}


/*
** Basic implementation of _ERRORMESSAGE.
** The library `liolib' redefines _ERRORMESSAGE for better error information.
*/
static int luaB__ERRORMESSAGE (lua_State *L) {
  luaL_checktype(L, 1, LUA_TSTRING);
  lua_getglobal(L, LUA_ALERT);
  if (lua_isfunction(L, -1)) {  /* avoid error loop if _ALERT is not defined */
    lua_Debug ar;
    lua_pushstring(L, "error: ");
    lua_pushvalue(L, 1);
    if (lua_getstack(L, 1, &ar)) {
      lua_getinfo(L, "Sl", &ar);
      if (ar.source && ar.currentline > 0) {
        char buff[100];
        sprintf(buff, "\n  <%.70s: line %d>", ar.short_src, ar.currentline);
        lua_pushstring(L, buff);
        lua_concat(L, 2);
      }
    }
    lua_pushstring(L, "\n");
    lua_concat(L, 3);
    lua_rawcall(L, 1, 0);
  }
  return 0;
}


/*
** If your system does not support `stdout', you can just remove this function.
** If you need, you can define your own `print' function, following this
** model but changing `fputs' to put the strings at a proper place
** (a console window or a log file, for instance).
*/
static int luaB_print (lua_State *L) {
  int n = lua_gettop(L);  /* number of arguments */
  int i;
  lua_getglobal(L, "tostring");
  for (i=1; i<=n; i++) {
    const char *s;
    lua_pushvalue(L, -1);  /* function to be called */
    lua_pushvalue(L, i);   /* value to print */
    lua_rawcall(L, 1, 1);
    s = lua_tostring(L, -1);  /* get result */
    if (s == NULL)
      lua_error(L, "`tostring' must return a string to `print'");
    if (i>1) fputs("\t", stdout);
    fputs(s, stdout);
    lua_pop(L, 1);  /* pop result */
  }
  fputs("\n", stdout);
  return 0;
}


static int luaB_tonumber (lua_State *L) {
  int base = luaL_opt_int(L, 2, 10);
  if (base == 10) {  /* standard conversion */
    luaL_checkany(L, 1);
    if (lua_isnumber(L, 1)) {
      lua_pushnumber(L, lua_tonumber(L, 1));
      return 1;
    }
  }
  else {
    const char *s1 = luaL_check_string(L, 1);
    char *s2;
    unsigned long n;
    luaL_arg_check(L, 2 <= base && base <= 36, 2, "base out of range");
    n = strtoul(s1, &s2, base);
    if (s1 != s2) {  /* at least one valid digit? */
      while (isspace((unsigned char)*s2)) s2++;  /* skip trailing spaces */
      if (*s2 == '\0') {  /* no invalid trailing characters? */
        lua_pushnumber(L, n);
        return 1;
      }
    }
  }
  lua_pushnil(L);  /* else not a number */
  return 1;
}


static int luaB_error (lua_State *L) {
  lua_error(L, luaL_opt_string(L, 1, NULL));
  return 0;  /* to avoid warnings */
}

static int luaB_setglobal (lua_State *L) {
  luaL_checkany(L, 2);
  lua_setglobal(L, luaL_check_string(L, 1));
  return 0;
}

static int luaB_getglobal (lua_State *L) {
  lua_getglobal(L, luaL_check_string(L, 1));
  return 1;
}

static int luaB_tag (lua_State *L) {
  luaL_checkany(L, 1);
  lua_pushnumber(L, lua_tag(L, 1));
  return 1;
}

static int luaB_settag (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  lua_pushvalue(L, 1);  /* push table */
  lua_settag(L, luaL_check_int(L, 2));
  return 1;  /* return table */
}

static int luaB_newtag (lua_State *L) {
  lua_pushnumber(L, lua_newtag(L));
  return 1;
}

static int luaB_copytagmethods (lua_State *L) {
  lua_pushnumber(L, lua_copytagmethods(L, luaL_check_int(L, 1),
                                          luaL_check_int(L, 2)));
  return 1;
}

static int luaB_globals (lua_State *L) {
  lua_getglobals(L);  /* value to be returned */
  if (!lua_isnull(L, 1)) {
    luaL_checktype(L, 1, LUA_TTABLE);
    lua_pushvalue(L, 1);  /* new table of globals */
    lua_setglobals(L);
  }
  return 1;
}

static int luaB_rawget (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  luaL_checkany(L, 2);
  lua_rawget(L, -2);
  return 1;
}

static int luaB_rawset (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  luaL_checkany(L, 2);
  luaL_checkany(L, 3);
  lua_rawset(L, -3);
  return 1;
}

static int luaB_settagmethod (lua_State *L) {
  int tag = luaL_check_int(L, 1);
  const char *event = luaL_check_string(L, 2);
  luaL_arg_check(L, lua_isfunction(L, 3) || lua_isnil(L, 3), 3,
                 "function or nil expected");
  if (strcmp(event, "gc") == 0)
    lua_error(L, "deprecated use: cannot set the `gc' tag method from Lua");
  lua_gettagmethod(L, tag, event);
  lua_pushvalue(L, 3);
  lua_settagmethod(L, tag, event);
  return 1;
}


static int luaB_gettagmethod (lua_State *L) {
  int tag = luaL_check_int(L, 1);
  const char *event = luaL_check_string(L, 2);
  if (strcmp(event, "gc") == 0)
    lua_error(L, "deprecated use: cannot get the `gc' tag method from Lua");
  lua_gettagmethod(L, tag, event);
  return 1;
}


static int luaB_gcinfo (lua_State *L) {
  lua_pushnumber(L, lua_getgccount(L));
  lua_pushnumber(L, lua_getgcthreshold(L));
  return 2;
}


static int luaB_collectgarbage (lua_State *L) {
  lua_setgcthreshold(L, luaL_opt_int(L, 1, 0));
  return 0;
}


static int luaB_type (lua_State *L) {
  luaL_checkany(L, 1);
  lua_pushstring(L, lua_typename(L, lua_type(L, 1)));
  return 1;
}


static int luaB_next (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  lua_settop(L, 2);  /* create a 2nd argument if there isn't one */
  if (lua_next(L, 1))
    return 2;
  else {
    lua_pushnil(L);
    return 1;
  }
}


static int passresults (lua_State *L, int status, int oldtop) {
  static const char *const errornames[] =
    {"ok", "run-time error", "file error", "syntax error",
     "memory error", "error in error handling"};
  if (status == 0) {
    int nresults = lua_gettop(L) - oldtop;
    if (nresults > 0)
      return nresults;  /* results are already on the stack */
    else {
      lua_pushuserdata(L, NULL);  /* at least one result to signal no errors */
      return 1;
    }
  }
  else {  /* error */
    lua_pushnil(L);
    lua_pushstring(L, errornames[status]);  /* error code */
    return 2;
  }
}

static int luaB_dostring (lua_State *L) {
  int oldtop = lua_gettop(L);
  size_t l;
  const char *s = luaL_check_lstr(L, 1, &l);
#if 0 /* 03/02/2001 jcw - test disabled */
  if (*s == '\27')  /* binary files start with ESC... */
    lua_error(L, "`dostring' cannot run pre-compiled code");
#endif
  return passresults(L, lua_dobuffer(L, s, l, luaL_opt_string(L, 2, s)), oldtop);
}


static int luaB_dofile (lua_State *L) {
  int oldtop = lua_gettop(L);
  const char *fname = luaL_opt_string(L, 1, NULL);
  return passresults(L, lua_dofile(L, fname), oldtop);
}


static int luaB_call (lua_State *L) {
  int oldtop;
  const char *options = luaL_opt_string(L, 3, "");
  int err = 0;  /* index of old error method */
  int i, status;
  int n;
  luaL_checktype(L, 2, LUA_TTABLE);
  n = lua_getn(L, 2);
  if (!lua_isnull(L, 4)) {  /* set new error method */
    lua_getglobal(L, LUA_ERRORMESSAGE);
    err = lua_gettop(L);  /* get index */
    lua_pushvalue(L, 4);
    lua_setglobal(L, LUA_ERRORMESSAGE);
  }
  oldtop = lua_gettop(L);  /* top before function-call preparation */
  /* push function */
  lua_pushvalue(L, 1);
  luaL_checkstack(L, n, "too many arguments");
  for (i=0; i<n; i++)  /* push arg[1...n] */
    lua_rawgeti(L, 2, i+1);
  status = lua_call(L, n, LUA_MULTRET);
  if (err != 0) {  /* restore old error method */
    lua_pushvalue(L, err);
    lua_setglobal(L, LUA_ERRORMESSAGE);
  }
  if (status != 0) {  /* error in call? */
    if (strchr(options, 'x'))
      lua_pushnil(L);  /* return nil to signal the error */
    else
      lua_error(L, NULL);  /* propagate error without additional messages */
    return 1;
  }
  if (strchr(options, 'p'))  /* pack results? */
    lua_error(L, "deprecated option `p' in `call'");
  return lua_gettop(L) - oldtop;  /* results are already on the stack */
}


static int luaB_tostring (lua_State *L) {
  char buff[64];
  switch (lua_type(L, 1)) {
    case LUA_TNUMBER:
      lua_pushstring(L, lua_tostring(L, 1));
      return 1;
    case LUA_TSTRING:
      lua_pushvalue(L, 1);
      return 1;
    case LUA_TTABLE:
      sprintf(buff, "table: %p", lua_topointer(L, 1));
      break;
    case LUA_TFUNCTION:
      sprintf(buff, "function: %p", lua_topointer(L, 1));
      break;
    case LUA_TUSERDATA:
      sprintf(buff, "userdata(%d): %p", lua_tag(L, 1), lua_touserdata(L, 1));
      break;
    case LUA_TNIL:
      lua_pushstring(L, "nil");
      return 1;
    default:
      luaL_argerror(L, 1, "value expected");
  }
  lua_pushstring(L, buff);
  return 1;
}


static int luaB_foreachi (lua_State *L) {
  int n, i;
  luaL_checktype(L, 1, LUA_TTABLE);
  luaL_checktype(L, 2, LUA_TFUNCTION);
  n = lua_getn(L, 1);
  for (i=1; i<=n; i++) {
    lua_pushvalue(L, 2);  /* function */
    lua_pushnumber(L, i);  /* 1st argument */
    lua_rawgeti(L, 1, i);  /* 2nd argument */
    lua_rawcall(L, 2, 1);
    if (!lua_isnil(L, -1))
      return 1;
    lua_pop(L, 1);  /* remove nil result */
  }
  return 0;
}


static int luaB_foreach (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  luaL_checktype(L, 2, LUA_TFUNCTION);
  lua_pushnil(L);  /* first index */
  for (;;) {
    if (lua_next(L, 1) == 0)
      return 0;
    lua_pushvalue(L, 2);  /* function */
    lua_pushvalue(L, -3);  /* key */
    lua_pushvalue(L, -3);  /* value */
    lua_rawcall(L, 2, 1);
    if (!lua_isnil(L, -1))
      return 1;
    lua_pop(L, 2);  /* remove value and result */
  }
}


static int luaB_assert (lua_State *L) {
  luaL_checkany(L, 1);
  if (lua_isnil(L, 1))
    luaL_verror(L, "assertion failed!  %.90s", luaL_opt_string(L, 2, ""));
  return 0;
}


static int luaB_getn (lua_State *L) {
  luaL_checktype(L, 1, LUA_TTABLE);
  lua_pushnumber(L, lua_getn(L, 1));
  return 1;
}


static int luaB_tinsert (lua_State *L) {
  int v = lua_gettop(L);  /* last argument: to be inserted */
  int n, pos;
  luaL_checktype(L, 1, LUA_TTABLE);
  n = lua_getn(L, 1);
  if (v == 2)  /* called with only 2 arguments */
    pos = n+1;
  else
    pos = luaL_check_int(L, 2);  /* 2nd argument is the position */
  lua_pushstring(L, "n");
  lua_pushnumber(L, n+1);
  lua_rawset(L, 1);  /* t.n = n+1 */
  for (; n>=pos; n--) {
    lua_rawgeti(L, 1, n);
    lua_rawseti(L, 1, n+1);  /* t[n+1] = t[n] */
  }
  lua_pushvalue(L, v);
  lua_rawseti(L, 1, pos);  /* t[pos] = v */
  return 0;
}


static int luaB_tremove (lua_State *L) {
  int pos, n;
  luaL_checktype(L, 1, LUA_TTABLE);
  n = lua_getn(L, 1);
  pos = luaL_opt_int(L, 2, n);
  if (n <= 0) return 0;  /* table is "empty" */
  lua_rawgeti(L, 1, pos);  /* result = t[pos] */
  for ( ;pos<n; pos++) {
    lua_rawgeti(L, 1, pos+1);
    lua_rawseti(L, 1, pos);  /* a[pos] = a[pos+1] */
  }
  lua_pushstring(L, "n");
  lua_pushnumber(L, n-1);
  lua_rawset(L, 1);  /* t.n = n-1 */
  lua_pushnil(L);
  lua_rawseti(L, 1, n);  /* t[n] = nil */
  return 1;
}




/*
** {======================================================
** Quicksort
** (based on `Algorithms in MODULA-3', Robert Sedgewick;
**  Addison-Wesley, 1993.)
*/


static void set2 (lua_State *L, int i, int j) {
  lua_rawseti(L, 1, i);
  lua_rawseti(L, 1, j);
}

static int sort_comp (lua_State *L, int a, int b) {
  /* WARNING: the caller (auxsort) must ensure stack space */
  if (!lua_isnil(L, 2)) {  /* function? */
    int res;
    lua_pushvalue(L, 2);
    lua_pushvalue(L, a-1);  /* -1 to compensate function */
    lua_pushvalue(L, b-2);  /* -2 to compensate function and `a' */
    lua_rawcall(L, 2, 1);
    res = !lua_isnil(L, -1);
    lua_pop(L, 1);
    return res;
  }
  else  /* a < b? */
    return lua_lessthan(L, a, b);
}

static void auxsort (lua_State *L, int l, int u) {
  while (l < u) {  /* for tail recursion */
    int i, j;
    /* sort elements a[l], a[(l+u)/2] and a[u] */
    lua_rawgeti(L, 1, l);
    lua_rawgeti(L, 1, u);
    if (sort_comp(L, -1, -2))  /* a[u] < a[l]? */
      set2(L, l, u);  /* swap a[l] - a[u] */
    else
      lua_pop(L, 2);
    if (u-l == 1) break;  /* only 2 elements */
    i = (l+u)/2;
    lua_rawgeti(L, 1, i);
    lua_rawgeti(L, 1, l);
    if (sort_comp(L, -2, -1))  /* a[i]<a[l]? */
      set2(L, i, l);
    else {
      lua_pop(L, 1);  /* remove a[l] */
      lua_rawgeti(L, 1, u);
      if (sort_comp(L, -1, -2))  /* a[u]<a[i]? */
        set2(L, i, u);
      else
        lua_pop(L, 2);
    }
    if (u-l == 2) break;  /* only 3 elements */
    lua_rawgeti(L, 1, i);  /* Pivot */
    lua_pushvalue(L, -1);
    lua_rawgeti(L, 1, u-1);
    set2(L, i, u-1);
    /* a[l] <= P == a[u-1] <= a[u], only need to sort from l+1 to u-2 */
    i = l; j = u-1;
    for (;;) {  /* invariant: a[l..i] <= P <= a[j..u] */
      /* repeat ++i until a[i] >= P */
      while (lua_rawgeti(L, 1, ++i), sort_comp(L, -1, -2)) {
        if (i>u) lua_error(L, "invalid order function for sorting");
        lua_pop(L, 1);  /* remove a[i] */
      }
      /* repeat --j until a[j] <= P */
      while (lua_rawgeti(L, 1, --j), sort_comp(L, -3, -1)) {
        if (j<l) lua_error(L, "invalid order function for sorting");
        lua_pop(L, 1);  /* remove a[j] */
      }
      if (j<i) {
        lua_pop(L, 3);  /* pop pivot, a[i], a[j] */
        break;
      }
      set2(L, i, j);
    }
    lua_rawgeti(L, 1, u-1);
    lua_rawgeti(L, 1, i);
    set2(L, u-1, i);  /* swap pivot (a[u-1]) with a[i] */
    /* a[l..i-1] <= a[i] == P <= a[i+1..u] */
    /* adjust so that smaller "half" is in [j..i] and larger one in [l..u] */
    if (i-l < u-i) {
      j=l; i=i-1; l=i+2;
    }
    else {
      j=i+1; i=u; u=j-2;
    }
    auxsort(L, j, i);  /* call recursively the smaller one */
  }  /* repeat the routine for the larger one */
}

static int luaB_sort (lua_State *L) {
  int n;
  luaL_checktype(L, 1, LUA_TTABLE);
  n = lua_getn(L, 1);
  if (!lua_isnull(L, 2))  /* is there a 2nd argument? */
    luaL_checktype(L, 2, LUA_TFUNCTION);
  lua_settop(L, 2);  /* make sure there is two arguments */
  auxsort(L, 1, n);
  return 0;
}

/* }====================================================== */



/*
** {======================================================
** Deprecated functions to manipulate global environment.
** =======================================================
*/


#define num_deprecated	4

static const struct luaL_reg deprecated_names [num_deprecated] = {
  {"foreachvar", luaB_foreach},
  {"nextvar", luaB_next},
  {"rawgetglobal", luaB_rawget},
  {"rawsetglobal", luaB_rawset}
};


#ifdef LUA_DEPRECATEDFUNCS

/*
** call corresponding function inserting `globals' as first argument
*/
static int deprecated_func (lua_State *L) {
  lua_insert(L, 1);  /* upvalue is the function to be called */
  lua_getglobals(L);
  lua_insert(L, 2);  /* table of globals is 1o argument */
  lua_rawcall(L, lua_gettop(L)-1, LUA_MULTRET);
  return lua_gettop(L);  /* return all results */
}


static void deprecated_funcs (lua_State *L) {
  int i;
  for (i=0; i<num_deprecated; i++) {
    lua_pushcfunction(L, deprecated_names[i].func);
    lua_pushcclosure(L, deprecated_func, 1);
    lua_setglobal(L, deprecated_names[i].name);
  }
}


#else

/*
** gives an explicit error in any attempt to call a deprecated function
*/
static int deprecated_func (lua_State *L) {
  luaL_verror(L, "function `%.20s' is deprecated", lua_tostring(L, -1));
  return 0;  /* to avoid warnings */
}


static void deprecated_funcs (lua_State *L) {
  int i;
  for (i=0; i<num_deprecated; i++) {
    lua_pushstring(L, deprecated_names[i].name);
    lua_pushcclosure(L, deprecated_func, 1);
    lua_setglobal(L, deprecated_names[i].name);
  }
}

#endif

/* }====================================================== */

static const struct luaL_reg base_funcs[] = {
  {LUA_ALERT, luaB__ALERT},
  {LUA_ERRORMESSAGE, luaB__ERRORMESSAGE},
  {"call", luaB_call},
  {"collectgarbage", luaB_collectgarbage},
  {"copytagmethods", luaB_copytagmethods},
  {"dofile", luaB_dofile},
  {"dostring", luaB_dostring},
  {"error", luaB_error},
  {"foreach", luaB_foreach},
  {"foreachi", luaB_foreachi},
  {"gcinfo", luaB_gcinfo},
  {"getglobal", luaB_getglobal},
  {"gettagmethod", luaB_gettagmethod},
  {"globals", luaB_globals},
  {"newtag", luaB_newtag},
  {"next", luaB_next},
  {"print", luaB_print},
  {"rawget", luaB_rawget},
  {"rawset", luaB_rawset},
  {"rawgettable", luaB_rawget},  /* for compatibility */
  {"rawsettable", luaB_rawset},  /* for compatibility */
  {"setglobal", luaB_setglobal},
  {"settag", luaB_settag},
  {"settagmethod", luaB_settagmethod},
  {"tag", luaB_tag},
  {"tonumber", luaB_tonumber},
  {"tostring", luaB_tostring},
  {"type", luaB_type},
  {"assert", luaB_assert},
  {"getn", luaB_getn},
  {"sort", luaB_sort},
  {"tinsert", luaB_tinsert},
  {"tremove", luaB_tremove}
};



LUALIB_API void lua_baselibopen (lua_State *L) {
  luaL_openl(L, base_funcs);
  lua_pushstring(L, LUA_VERSION);
  lua_setglobal(L, "_VERSION");
  deprecated_funcs(L);
}

/* resumed: mluxsys.c */
/* include: ldblib.c */
/*
** $Id: ldblib.c,v 1.29 2000/11/06 17:58:38 roberto Exp $
** Interface from Lua to its debug API
** See Copyright Notice in lua.h
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: luadebug.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */



static void settabss (lua_State *L, const char *i, const char *v) {
  lua_pushstring(L, i);
  lua_pushstring(L, v);
  lua_settable(L, -3);
}


static void settabsi (lua_State *L, const char *i, int v) {
  lua_pushstring(L, i);
  lua_pushnumber(L, v);
  lua_settable(L, -3);
}


static int getinfo (lua_State *L) {
  lua_Debug ar;
  const char *options = luaL_opt_string(L, 2, "flnSu");
  char buff[20];
  if (lua_isnumber(L, 1)) {
    if (!lua_getstack(L, (int)lua_tonumber(L, 1), &ar)) {
      lua_pushnil(L);  /* level out of range */
      return 1;
    }
  }
  else if (lua_isfunction(L, 1)) {
    lua_pushvalue(L, 1);
    sprintf(buff, ">%.10s", options);
    options = buff;
  }
  else
    luaL_argerror(L, 1, "function or level expected");
  if (!lua_getinfo(L, options, &ar))
    luaL_argerror(L, 2, "invalid option");
  lua_newtable(L);
  for (; *options; options++) {
    switch (*options) {
      case 'S':
        settabss(L, "source", ar.source);
        if (ar.source)
          settabss(L, "short_src", ar.short_src);
        settabsi(L, "linedefined", ar.linedefined);
        settabss(L, "what", ar.what);
        break;
      case 'l':
        settabsi(L, "currentline", ar.currentline);
        break;
      case 'u':
        settabsi(L, "nups", ar.nups);
        break;
      case 'n':
        settabss(L, "name", ar.name);
        settabss(L, "namewhat", ar.namewhat);
        break;
      case 'f':
        lua_pushstring(L, "func");
        lua_pushvalue(L, -3);
        lua_settable(L, -3);
        break;
    }
  }
  return 1;  /* return table */
}
    

static int getlocal (lua_State *L) {
  lua_Debug ar;
  const char *name;
  if (!lua_getstack(L, luaL_check_int(L, 1), &ar))  /* level out of range? */
    luaL_argerror(L, 1, "level out of range");
  name = lua_getlocal(L, &ar, luaL_check_int(L, 2));
  if (name) {
    lua_pushstring(L, name);
    lua_pushvalue(L, -2);
    return 2;
  }
  else {
    lua_pushnil(L);
    return 1;
  }
}


static int setlocal (lua_State *L) {
  lua_Debug ar;
  if (!lua_getstack(L, luaL_check_int(L, 1), &ar))  /* level out of range? */
    luaL_argerror(L, 1, "level out of range");
  luaL_checkany(L, 3);
  lua_pushstring(L, lua_setlocal(L, &ar, luaL_check_int(L, 2)));
  return 1;
}



/* dummy variables (to define unique addresses) */
static char key1, key2;
#define KEY_CALLHOOK	(&key1)
#define KEY_LINEHOOK	(&key2)


static void hookf (lua_State *L, void *key) {
  lua_getregistry(L);
  lua_pushuserdata(L, key);
  lua_gettable(L, -2);
  if (lua_isfunction(L, -1)) {
    lua_pushvalue(L, 1);
    lua_rawcall(L, 1, 0);
  }
  else
    lua_pop(L, 1);  /* pop result from gettable */
  lua_pop(L, 1);  /* pop table */
}


static void callf (lua_State *L, lua_Debug *ar) {
  lua_pushstring(L, ar->event);
  hookf(L, KEY_CALLHOOK);
}


static void linef (lua_State *L, lua_Debug *ar) {
  lua_pushnumber(L, ar->currentline);
  hookf(L, KEY_LINEHOOK);
}


static void sethook (lua_State *L, void *key, lua_Hook hook,
                     lua_Hook (*sethookf)(lua_State * L, lua_Hook h)) {
  lua_settop(L, 1);
  if (lua_isnil(L, 1))
    (*sethookf)(L, NULL);
  else if (lua_isfunction(L, 1))
    (*sethookf)(L, hook);
  else
    luaL_argerror(L, 1, "function expected");
  lua_getregistry(L);
  lua_pushuserdata(L, key);
  lua_pushvalue(L, -1);  /* dup key */
  lua_gettable(L, -3);   /* get old value */
  lua_pushvalue(L, -2);  /* key (again) */
  lua_pushvalue(L, 1);
  lua_settable(L, -5);  /* set new value */
}


static int setcallhook (lua_State *L) {
  sethook(L, KEY_CALLHOOK, callf, lua_setcallhook);
  return 1;
}


static int setlinehook (lua_State *L) {
  sethook(L, KEY_LINEHOOK, linef, lua_setlinehook);
  return 1;
}


static const struct luaL_reg dblib[] = {
  {"getlocal", getlocal},
  {"getinfo", getinfo},
  {"setcallhook", setcallhook},
  {"setlinehook", setlinehook},
  {"setlocal", setlocal}
};


LUALIB_API void lua_dblibopen (lua_State *L) {
  luaL_openl(L, dblib);
}

/* resumed: mluxsys.c */
/* include: liolib.c */
/*
** $Id: liolib.c,v 1.91 2000/10/31 13:10:24 roberto Exp $
** Standard I/O (and system) library
** See Copyright Notice in lua.h
*/


#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: luadebug.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */


#ifndef OLD_ANSI
#include <errno.h>
#include <locale.h>
/*JCW can't be used in lux, because include conflicts with Windows build */
/*JCW #define realloc(b,s)    ((b) == NULL ? malloc(s) : (realloc)(b, s)) */
/*JCW #define free(b)         if (b) (free)(b) */
#else
/* no support for locale and for strerror: fake them */
#define setlocale(a,b)	((void)a, strcmp((b),"C")==0?"C":NULL)
#define LC_ALL		0
#define LC_COLLATE	0
#define LC_CTYPE	0
#define LC_MONETARY	0
#define LC_NUMERIC	0
#define LC_TIME		0
#define strerror(e)	"generic I/O error"
#define errno		(-1)
#endif



#ifdef POPEN
/* FILE *popen();
int pclose(); */
#define CLOSEFILE(L, f)    ((pclose(f) == -1) ? fclose(f) : 0)
#else
/* no support for popen */
#define popen(x,y) NULL  /* that is, popen always fails */
#define CLOSEFILE(L, f)    (fclose(f))
#endif


#define INFILE	0
#define OUTFILE 1

typedef struct IOCtrl {
  int ref[2];  /* ref for strings _INPUT/_OUTPUT */
  int iotag;    /* tag for file handles */
  int closedtag;  /* tag for closed handles */
} IOCtrl;



static const char *const filenames[] = {"_INPUT", "_OUTPUT"};


static int pushresult (lua_State *L, int i) {
  if (i) {
    lua_pushuserdata(L, NULL);
    return 1;
  }
  else {
    lua_pushnil(L);
    lua_pushstring(L, strerror(errno));
    lua_pushnumber(L, errno);
    return 3;;
  }
}


/*
** {======================================================
** FILE Operations
** =======================================================
*/


static FILE *gethandle (lua_State *L, IOCtrl *ctrl, int f) {
  void *p = lua_touserdata(L, f);
  if (p != NULL) {  /* is `f' a userdata ? */
    int ftag = lua_tag(L, f);
    if (ftag == ctrl->iotag)  /* does it have the correct tag? */
      return (FILE *)p;
    else if (ftag == ctrl->closedtag)
      lua_error(L, "cannot access a closed file");
    /* else go through */
  }
  return NULL;
}


static FILE *getnonullfile (lua_State *L, IOCtrl *ctrl, int arg) {
  FILE *f = gethandle(L, ctrl, arg);
  luaL_arg_check(L, f, arg, "invalid file handle");
  return f;
}


static FILE *getfilebyref (lua_State *L, IOCtrl *ctrl, int inout) {
  FILE *f;
  lua_getglobals(L);
  lua_getref(L, ctrl->ref[inout]);
  lua_rawget(L, -2);
  f = gethandle(L, ctrl, -1);
  if (f == NULL)
    luaL_verror(L, "global variable `%.10s' is not a file handle",
                filenames[inout]);
  return f;
}


static void setfilebyname (lua_State *L, IOCtrl *ctrl, FILE *f,
                           const char *name) {
  lua_pushusertag(L, f, ctrl->iotag);
  lua_setglobal(L, name);
}


#define setfile(L,ctrl,f,inout)	(setfilebyname(L,ctrl,f,filenames[inout]))


static int setreturn (lua_State *L, IOCtrl *ctrl, FILE *f, int inout) {
  if (f == NULL)
    return pushresult(L, 0);
  else {
    setfile(L, ctrl, f, inout);
    lua_pushusertag(L, f, ctrl->iotag);
    return 1;
  }
}


static int closefile (lua_State *L, IOCtrl *ctrl, FILE *f) {
  if (f == stdin || f == stdout || f == stderr)
    return 1;
  else {
    lua_pushusertag(L, f, ctrl->iotag);
    lua_settag(L, ctrl->closedtag);
    return (CLOSEFILE(L, f) == 0);
  }
}


static int io_close (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  lua_pop(L, 1);  /* remove upvalue */
  return pushresult(L, closefile(L, ctrl, getnonullfile(L, ctrl, 1)));
}


static int file_collect (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *f = getnonullfile(L, ctrl, 1);
  if (f != stdin && f != stdout && f != stderr)
    CLOSEFILE(L, f);
  return 0;
}


static int io_open (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *f;
  lua_pop(L, 1);  /* remove upvalue */
  f = fopen(luaL_check_string(L, 1), luaL_check_string(L, 2));
  if (f) {
    lua_pushusertag(L, f, ctrl->iotag);
    return 1;
  }
  else
    return pushresult(L, 0);
}



static int io_fromto (lua_State *L, int inout, const char *mode) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *current;
  lua_pop(L, 1);  /* remove upvalue */
  if (lua_isnull(L, 1)) {
    closefile(L, ctrl, getfilebyref(L, ctrl, inout));
    current = (inout == 0) ? stdin : stdout;    
  }
  else if (lua_tag(L, 1) == ctrl->iotag)  /* deprecated option */
    current = (FILE *)lua_touserdata(L, 1);
  else {
    const char *s = luaL_check_string(L, 1);
    current = (*s == '|') ? popen(s+1, mode) : fopen(s, mode);
  }
  return setreturn(L, ctrl, current, inout);
}


static int io_readfrom (lua_State *L) {
  return io_fromto(L, INFILE, "r");
}


static int io_writeto (lua_State *L) {
  return io_fromto(L, OUTFILE, "w");
}


static int io_appendto (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *current;
  lua_pop(L, 1);  /* remove upvalue */
  current = fopen(luaL_check_string(L, 1), "a");
  return setreturn(L, ctrl, current, OUTFILE);
}



/*
** {======================================================
** READ
** =======================================================
*/



#ifdef LUA_COMPAT_READPATTERN

/*
** We cannot lookahead without need, because this can lock stdin.
** This flag signals when we need to read a next char.
*/
#define NEED_OTHER (EOF-1)  /* just some flag different from EOF */


static int read_pattern (lua_State *L, FILE *f, const char *p) {
  int inskip = 0;  /* {skip} level */
  int c = NEED_OTHER;
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  while (*p != '\0') {
    switch (*p) {
      case '{':
        inskip++;
        p++;
        continue;
      case '}':
        if (!inskip) lua_error(L, "unbalanced braces in read pattern");
        inskip--;
        p++;
        continue;
      default: {
        const char *ep = luaI_classend(L, p);  /* get what is next */
        int m;  /* match result */
        if (c == NEED_OTHER) c = getc(f);
        m = (c==EOF) ? 0 : luaI_singlematch(c, p, ep);
        if (m) {
          if (!inskip) luaL_putchar(&b, c);
          c = NEED_OTHER;
        }
        switch (*ep) {
          case '+':  /* repetition (1 or more) */
            if (!m) goto break_while;  /* pattern fails? */
            /* else go through */
          case '*':  /* repetition (0 or more) */
            while (m) {  /* reads the same item until it fails */
              c = getc(f);
              m = (c==EOF) ? 0 : luaI_singlematch(c, p, ep);
              if (m && !inskip) luaL_putchar(&b, c);
            }
            /* go through to continue reading the pattern */
          case '?':  /* optional */
            p = ep+1;  /* continues reading the pattern */
            continue;
          default:
            if (!m) goto break_while;  /* pattern fails? */
            p = ep;  /* else continues reading the pattern */
        }
      }
    }
  } break_while:
  if (c != NEED_OTHER) ungetc(c, f);
  luaL_pushresult(&b);  /* close buffer */
  return (*p == '\0');
}

#else

#define read_pattern(L, f, p) (lua_error(L, "read patterns are deprecated"), 0)

#endif


static int read_number (lua_State *L, FILE *f) {
  double d;
  if (fscanf(f, "%lf", &d) == 1) {
    lua_pushnumber(L, d);
    return 1;
  }
  else return 0;  /* read fails */
}


static int read_word (lua_State *L, FILE *f) {
  int c;
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  do { c = fgetc(f); } while (isspace(c));  /* skip spaces */
  while (c != EOF && !isspace(c)) {
    luaL_putchar(&b, c);
    c = fgetc(f);
  }
  ungetc(c, f);
  luaL_pushresult(&b);  /* close buffer */
  return (lua_strlen(L, -1) > 0);
}


static int read_line (lua_State *L, FILE *f) {
  int n = 0;
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  for (;;) {
    char *p = luaL_prepbuffer(&b);
    if (!fgets(p, LUAL_BUFFERSIZE, f))  /* read fails? */
      break;
    n = strlen(p);
    if (p[n-1] != '\n')
      luaL_addsize(&b, n); 
    else {
      luaL_addsize(&b, n-1);  /* do not add the `\n' */
      break;
    }
  }
  luaL_pushresult(&b);  /* close buffer */
  return (n > 0);  /* read something? */
}


static void read_file (lua_State *L, FILE *f) {
  size_t len = 0;
  size_t size = BUFSIZ;
  char *buffer = NULL;
  for (;;) {
    char *newbuffer = (char *)realloc(buffer, size);
    if (newbuffer == NULL) {
      free(buffer);
      lua_error(L, "not enough memory to read a file");
    }
    buffer = newbuffer;
    len += fread(buffer+len, sizeof(char), size-len, f);
    if (len < size) break;  /* did not read all it could */
    size *= 2;
  }
  lua_pushlstring(L, buffer, len);
  free(buffer);
}


static int read_chars (lua_State *L, FILE *f, size_t n) {
  char *buffer;
  size_t n1;
  char statbuff[BUFSIZ];
  if (n <= BUFSIZ)
    buffer = statbuff;
  else {
    buffer = (char  *)malloc(n);
    if (buffer == NULL)
      lua_error(L, "not enough memory to read a file");
  }
  n1 = fread(buffer, sizeof(char), n, f);
  lua_pushlstring(L, buffer, n1);
  if (buffer != statbuff) free(buffer);
  return (n1 > 0 || n == 0);
}


static int io_read (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  int lastarg = lua_gettop(L) - 1;
  int firstarg = 1;
  FILE *f = gethandle(L, ctrl, firstarg);
  int n;
  if (f) firstarg++;
  else f = getfilebyref(L, ctrl, INFILE);  /* get _INPUT */
  lua_pop(L, 1);
  if (firstarg > lastarg) {  /* no arguments? */
    lua_settop(L, 0);  /* erase upvalue and other eventual garbage */
    firstarg = lastarg = 1;  /* correct indices */
    lua_pushstring(L, "*l");  /* push default argument */
  }
  else  /* ensure stack space for all results and for auxlib's buffer */
    luaL_checkstack(L, lastarg-firstarg+1+LUA_MINSTACK, "too many arguments");
  for (n = firstarg; n<=lastarg; n++) {
    int success;
    if (lua_isnumber(L, n))
      success = read_chars(L, f, (size_t)lua_tonumber(L, n));
    else {
      const char *p = luaL_check_string(L, n);
      if (p[0] != '*')
        success = read_pattern(L, f, p);  /* deprecated! */
      else {
        switch (p[1]) {
          case 'n':  /* number */
            if (!read_number(L, f)) goto endloop;  /* read fails */
            continue;  /* number is already pushed; avoid the "pushstring" */
          case 'l':  /* line */
            success = read_line(L, f);
            break;
          case 'a':  /* file */
            read_file(L, f);
            success = 1; /* always success */
            break;
          case 'w':  /* word */
            success = read_word(L, f);
            break;
          default:
            luaL_argerror(L, n, "invalid format");
            success = 0;  /* to avoid warnings */
        }
      }
    }
    if (!success) {
      lua_pop(L, 1);  /* remove last result */
      break;  /* read fails */
    }
  } endloop:
  return n - firstarg;
}

/* }====================================================== */


static int io_write (lua_State *L) {
  int lastarg = lua_gettop(L) - 1;
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  int arg = 1;
  int status = 1;
  FILE *f = gethandle(L, ctrl, arg);
  if (f) arg++;
  else f = getfilebyref(L, ctrl, OUTFILE);  /* get _OUTPUT */
  for (; arg <=  lastarg; arg++) {
    if (lua_type(L, arg) == LUA_TNUMBER) {  /* LUA_NUMBER */
      /* optimization: could be done exactly as for strings */
      status = status && fprintf(f, "%.16g", lua_tonumber(L, arg)) > 0;
    }
    else {
      size_t l;
      const char *s = luaL_check_lstr(L, arg, &l);
      status = status && (fwrite(s, sizeof(char), l, f) == l);
    }
  }
  pushresult(L, status);
  return 1;
}


static int io_seek (lua_State *L) {
  static const int mode[] = {SEEK_SET, SEEK_CUR, SEEK_END};
  static const char *const modenames[] = {"set", "cur", "end", NULL};
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *f;
  int op;
  long offset;
  lua_pop(L, 1);  /* remove upvalue */
  f = getnonullfile(L, ctrl, 1);
  op = luaL_findstring(luaL_opt_string(L, 2, "cur"), modenames);
  offset = luaL_opt_long(L, 3, 0);
  luaL_arg_check(L, op != -1, 2, "invalid mode");
  op = fseek(f, offset, mode[op]);
  if (op)
    return pushresult(L, 0);  /* error */
  else {
    lua_pushnumber(L, ftell(f));
    return 1;
  }
}


static int io_flush (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_touserdata(L, -1);
  FILE *f;
  lua_pop(L, 1);  /* remove upvalue */
  f = gethandle(L, ctrl, 1);
  luaL_arg_check(L, f || lua_isnull(L, 1), 1, "invalid file handle");
  return pushresult(L, fflush(f) == 0);
}

/* }====================================================== */


/*
** {======================================================
** Other O.S. Operations
** =======================================================
*/

static int io_execute (lua_State *L) {
  lua_pushnumber(L, system(luaL_check_string(L, 1)));
  return 1;
}


static int io_remove (lua_State *L) {
  return pushresult(L, remove(luaL_check_string(L, 1)) == 0);
}


static int io_rename (lua_State *L) {
  return pushresult(L, rename(luaL_check_string(L, 1),
                    luaL_check_string(L, 2)) == 0);
}


static int io_tmpname (lua_State *L) {
  lua_pushstring(L, tmpnam(NULL));
  return 1;
}



static int io_getenv (lua_State *L) {
  lua_pushstring(L, getenv(luaL_check_string(L, 1)));  /* if NULL push nil */
  return 1;
}


static int io_clock (lua_State *L) {
  lua_pushnumber(L, ((double)clock())/CLOCKS_PER_SEC);
  return 1;
}


static int io_date (lua_State *L) {
  char b[256];
  const char *s = luaL_opt_string(L, 1, "%c");
  struct tm *stm;
  time_t t;
/*JCW 17/02/2001 - extended to accept optional seconds as 2nd arg */
  if (!lua_isnil(L,2)) t = luaL_check_long(L, 2); else
/* end of mods, note that the time() call is now part of an else! */
  time(&t); stm = localtime(&t);
  stm = localtime(&t);
  if (strftime(b, sizeof(b), s, stm))
    lua_pushstring(L, b);
  else
    lua_error(L, "invalid `date' format");
  return 1;
}


static int setloc (lua_State *L) {
  static const int cat[] = {LC_ALL, LC_COLLATE, LC_CTYPE, LC_MONETARY,
                      LC_NUMERIC, LC_TIME};
  static const char *const catnames[] = {"all", "collate", "ctype", "monetary",
     "numeric", "time", NULL};
  int op = luaL_findstring(luaL_opt_string(L, 2, "all"), catnames);
  luaL_arg_check(L, op != -1, 2, "invalid option");
  lua_pushstring(L, setlocale(cat[op], luaL_check_string(L, 1)));
  return 1;
}


static int io_exit (lua_State *L) {
  exit(luaL_opt_int(L, 1, EXIT_SUCCESS));
  return 0;  /* to avoid warnings */
}

/* }====================================================== */



static int io_debug (lua_State *L) {
  for (;;) {
    char buffer[250];
    fprintf(stderr, "lua_debug> ");
    if (fgets(buffer, sizeof(buffer), stdin) == 0 ||
        strcmp(buffer, "cont\n") == 0)
      return 0;
    lua_dostring(L, buffer);
    lua_settop(L, 0);  /* remove eventual returns */
  }
}


#define LEVELS1	12	/* size of the first part of the stack */
#define LEVELS2	10	/* size of the second part of the stack */

static int errorfb (lua_State *L) {
  int level = 1;  /* skip level 0 (it's this function) */
  int firstpart = 1;  /* still before eventual `...' */
  lua_Debug ar;
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  luaL_addstring(&b, "error: ");
  luaL_addstring(&b, luaL_check_string(L, 1));
  luaL_addstring(&b, "\n");
  while (lua_getstack(L, level++, &ar)) {
    char buff[120];  /* enough to fit following `sprintf's */
    if (level == 2)
      luaL_addstring(&b, "stack traceback:\n");
    else if (level > LEVELS1 && firstpart) {
      /* no more than `LEVELS2' more levels? */
      if (!lua_getstack(L, level+LEVELS2, &ar))
        level--;  /* keep going */
      else {
        luaL_addstring(&b, "       ...\n");  /* too many levels */
        while (lua_getstack(L, level+LEVELS2, &ar))  /* find last levels */
          level++;
      }
      firstpart = 0;
      continue;
    }
    sprintf(buff, "%4d:  ", level-1);
    luaL_addstring(&b, buff);
    lua_getinfo(L, "Snl", &ar);
    switch (*ar.namewhat) {
      case 'g':  case 'l':  /* global, local */
        sprintf(buff, "function `%.50s'", ar.name);
        break;
      case 'f':  /* field */
        sprintf(buff, "method `%.50s'", ar.name);
        break;
      case 't':  /* tag method */
        sprintf(buff, "`%.50s' tag method", ar.name);
        break;
      default: {
        if (*ar.what == 'm')  /* main? */
          sprintf(buff, "main of %.70s", ar.short_src);
        else if (*ar.what == 'C')  /* C function? */
          sprintf(buff, "%.70s", ar.short_src);
        else
          sprintf(buff, "function <%d:%.70s>", ar.linedefined, ar.short_src);
        ar.source = NULL;  /* do not print source again */
      }
    }
    luaL_addstring(&b, buff);
    if (ar.currentline > 0) {
      sprintf(buff, " at line %d", ar.currentline);
      luaL_addstring(&b, buff);
    }
    if (ar.source) {
      sprintf(buff, " [%.70s]", ar.short_src);
      luaL_addstring(&b, buff);
    }
    luaL_addstring(&b, "\n");
  }
  luaL_pushresult(&b);
  lua_getglobal(L, LUA_ALERT);
  if (lua_isfunction(L, -1)) {  /* avoid loop if _ALERT is not defined */
    lua_pushvalue(L, -2);  /* error message */
    lua_rawcall(L, 1, 0);
  }
  return 0;
}



static const struct luaL_reg iolib[] = {
  {LUA_ERRORMESSAGE, errorfb},
  {"clock",     io_clock},
  {"date",     io_date},
  {"debug",    io_debug},
  {"execute",  io_execute},
  {"exit",     io_exit},
  {"getenv",   io_getenv},
  {"remove",   io_remove},
  {"rename",   io_rename},
  {"setlocale", setloc},
  {"tmpname",   io_tmpname}
};


static const struct luaL_reg iolibtag[] = {
  {"appendto", io_appendto},
  {"closefile",   io_close},
  {"flush",     io_flush},
  {"openfile",   io_open},
  {"read",     io_read},
  {"readfrom", io_readfrom},
  {"seek",     io_seek},
  {"write",    io_write},
  {"writeto",  io_writeto}
};


static void openwithcontrol (lua_State *L) {
  IOCtrl *ctrl = (IOCtrl *)lua_newuserdata(L, sizeof(IOCtrl));
  unsigned int i;
  ctrl->iotag = lua_newtag(L);
  ctrl->closedtag = lua_newtag(L);
  for (i=0; i<sizeof(iolibtag)/sizeof(iolibtag[0]); i++) {
    /* put `ctrl' as upvalue for these functions */
    lua_pushvalue(L, -1);
    lua_pushcclosure(L, iolibtag[i].func, 1);
    lua_setglobal(L, iolibtag[i].name);
  }
  /* create references to variable names */
  lua_pushstring(L, filenames[INFILE]);
  ctrl->ref[INFILE] = lua_ref(L, 1);
  lua_pushstring(L, filenames[OUTFILE]);
  ctrl->ref[OUTFILE] = lua_ref(L, 1);
  /* predefined file handles */
  setfile(L, ctrl, stdin, INFILE);
  setfile(L, ctrl, stdout, OUTFILE);
  setfilebyname(L, ctrl, stdin, "_STDIN");
  setfilebyname(L, ctrl, stdout, "_STDOUT");
  setfilebyname(L, ctrl, stderr, "_STDERR");
  /* close files when collected */
  lua_pushcclosure(L, file_collect, 1);  /* pops `ctrl' from stack */
  lua_settagmethod(L, ctrl->iotag, "gc");
}


LUALIB_API void lua_iolibopen (lua_State *L) {
  luaL_openl(L, iolib);
  openwithcontrol(L);
}

/* resumed: mluxsys.c */
/* include: lmathlib.c */
/*
** $Id: lmathlib.c,v 1.32 2000/10/31 13:10:24 roberto Exp $
** Standard mathematical library
** See Copyright Notice in lua.h
*/


#include <stdlib.h>
#include <math.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */


#undef PI
#define PI (3.14159265358979323846)
#define RADIANS_PER_DEGREE (PI/180.0)



/*
** If you want Lua to operate in radians (instead of degrees),
** define RADIANS
*/
#ifdef RADIANS
#define FROMRAD(a)	(a)
#define TORAD(a)	(a)
#else
#define FROMRAD(a)	((a)/RADIANS_PER_DEGREE)
#define TORAD(a)	((a)*RADIANS_PER_DEGREE)
#endif


static int math_abs (lua_State *L) {
  lua_pushnumber(L, fabs(luaL_check_number(L, 1)));
  return 1;
}

static int math_sin (lua_State *L) {
  lua_pushnumber(L, sin(TORAD(luaL_check_number(L, 1))));
  return 1;
}

static int math_cos (lua_State *L) {
  lua_pushnumber(L, cos(TORAD(luaL_check_number(L, 1))));
  return 1;
}

static int math_tan (lua_State *L) {
  lua_pushnumber(L, tan(TORAD(luaL_check_number(L, 1))));
  return 1;
}

static int math_asin (lua_State *L) {
  lua_pushnumber(L, FROMRAD(asin(luaL_check_number(L, 1))));
  return 1;
}

static int math_acos (lua_State *L) {
  lua_pushnumber(L, FROMRAD(acos(luaL_check_number(L, 1))));
  return 1;
}

static int math_atan (lua_State *L) {
  lua_pushnumber(L, FROMRAD(atan(luaL_check_number(L, 1))));
  return 1;
}

static int math_atan2 (lua_State *L) {
  lua_pushnumber(L, FROMRAD(atan2(luaL_check_number(L, 1), luaL_check_number(L, 2))));
  return 1;
}

static int math_ceil (lua_State *L) {
  lua_pushnumber(L, ceil(luaL_check_number(L, 1)));
  return 1;
}

static int math_floor (lua_State *L) {
  lua_pushnumber(L, floor(luaL_check_number(L, 1)));
  return 1;
}

static int math_mod (lua_State *L) {
  lua_pushnumber(L, fmod(luaL_check_number(L, 1), luaL_check_number(L, 2)));
  return 1;
}

static int math_sqrt (lua_State *L) {
  lua_pushnumber(L, sqrt(luaL_check_number(L, 1)));
  return 1;
}

static int math_pow (lua_State *L) {
  lua_pushnumber(L, pow(luaL_check_number(L, 1), luaL_check_number(L, 2)));
  return 1;
}

static int math_log (lua_State *L) {
  lua_pushnumber(L, log(luaL_check_number(L, 1)));
  return 1;
}

static int math_log10 (lua_State *L) {
  lua_pushnumber(L, log10(luaL_check_number(L, 1)));
  return 1;
}

static int math_exp (lua_State *L) {
  lua_pushnumber(L, exp(luaL_check_number(L, 1)));
  return 1;
}

static int math_deg (lua_State *L) {
  lua_pushnumber(L, luaL_check_number(L, 1)/RADIANS_PER_DEGREE);
  return 1;
}

static int math_rad (lua_State *L) {
  lua_pushnumber(L, luaL_check_number(L, 1)*RADIANS_PER_DEGREE);
  return 1;
}

static int math_frexp (lua_State *L) {
  int e;
  lua_pushnumber(L, frexp(luaL_check_number(L, 1), &e));
  lua_pushnumber(L, e);
  return 2;
}

static int math_ldexp (lua_State *L) {
  lua_pushnumber(L, ldexp(luaL_check_number(L, 1), luaL_check_int(L, 2)));
  return 1;
}



static int math_min (lua_State *L) {
  int n = lua_gettop(L);  /* number of arguments */
  double dmin = luaL_check_number(L, 1);
  int i;
  for (i=2; i<=n; i++) {
    double d = luaL_check_number(L, i);
    if (d < dmin)
      dmin = d;
  }
  lua_pushnumber(L, dmin);
  return 1;
}


static int math_max (lua_State *L) {
  int n = lua_gettop(L);  /* number of arguments */
  double dmax = luaL_check_number(L, 1);
  int i;
  for (i=2; i<=n; i++) {
    double d = luaL_check_number(L, i);
    if (d > dmax)
      dmax = d;
  }
  lua_pushnumber(L, dmax);
  return 1;
}


static int math_random (lua_State *L) {
  /* the '%' avoids the (rare) case of r==1, and is needed also because on
     some systems (SunOS!) "rand()" may return a value larger than RAND_MAX */
  double r = (double)(rand()%RAND_MAX) / (double)RAND_MAX;
  switch (lua_gettop(L)) {  /* check number of arguments */
    case 0: {  /* no arguments */
      lua_pushnumber(L, r);  /* Number between 0 and 1 */
      break;
    }
    case 1: {  /* only upper limit */
      int u = luaL_check_int(L, 1);
      luaL_arg_check(L, 1<=u, 1, "interval is empty");
      lua_pushnumber(L, (int)(r*u)+1);  /* integer between 1 and `u' */
      break;
    }
    case 2: {  /* lower and upper limits */
      int l = luaL_check_int(L, 1);
      int u = luaL_check_int(L, 2);
      luaL_arg_check(L, l<=u, 2, "interval is empty");
      lua_pushnumber(L, (int)(r*(u-l+1))+l);  /* integer between `l' and `u' */
      break;
    }
    default: lua_error(L, "wrong number of arguments");
  }
  return 1;
}


static int math_randomseed (lua_State *L) {
  srand(luaL_check_int(L, 1));
  return 0;
}


static const struct luaL_reg mathlib[] = {
{"abs",   math_abs},
{"sin",   math_sin},
{"cos",   math_cos},
{"tan",   math_tan},
{"asin",  math_asin},
{"acos",  math_acos},
{"atan",  math_atan},
{"atan2", math_atan2},
{"ceil",  math_ceil},
{"floor", math_floor},
{"mod",   math_mod},
{"frexp", math_frexp},
{"ldexp", math_ldexp},
{"sqrt",  math_sqrt},
{"min",   math_min},
{"max",   math_max},
{"log",   math_log},
{"log10", math_log10},
{"exp",   math_exp},
{"deg",   math_deg},
{"rad",   math_rad},
{"random",     math_random},
{"randomseed", math_randomseed}
};

/*
** Open math library
*/
LUALIB_API void lua_mathlibopen (lua_State *L) {
  luaL_openl(L, mathlib);
  lua_pushcfunction(L, math_pow);
  lua_settagmethod(L, LUA_TNUMBER, "pow");
  lua_pushnumber(L, PI);
  lua_setglobal(L, "PI");
}

/* resumed: mluxsys.c */
/* include: lstrlib.c */
/*
** $Id: lstrlib.c,v 1.56 2000/10/27 16:15:53 roberto Exp $
** Standard library for string operations and pattern-matching
** See Copyright Notice in lua.h
*/


#include <ctype.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* skipped: lua.h - see mluxsys.c */

/* skipped: lauxlib.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */



static int str_len (lua_State *L) {
  size_t l;
  luaL_check_lstr(L, 1, &l);
  lua_pushnumber(L, l);
  return 1;
}


static long posrelat (long pos, size_t len) {
  /* relative string position: negative means back from end */
  return (pos>=0) ? pos : (long)len+pos+1;
}


static int str_sub (lua_State *L) {
  size_t l;
  const char *s = luaL_check_lstr(L, 1, &l);
  long start = posrelat(luaL_check_long(L, 2), l);
  long end = posrelat(luaL_opt_long(L, 3, -1), l);
  if (start < 1) start = 1;
  if (end > (long)l) end = l;
  if (start <= end)
    lua_pushlstring(L, s+start-1, end-start+1);
  else lua_pushstring(L, "");
  return 1;
}


static int str_lower (lua_State *L) {
  size_t l;
  size_t i;
  luaL_Buffer b;
  const char *s = luaL_check_lstr(L, 1, &l);
  luaL_buffinit(L, &b);
  for (i=0; i<l; i++)
    luaL_putchar(&b, tolower((unsigned char)(s[i])));
  luaL_pushresult(&b);
  return 1;
}


static int str_upper (lua_State *L) {
  size_t l;
  size_t i;
  luaL_Buffer b;
  const char *s = luaL_check_lstr(L, 1, &l);
  luaL_buffinit(L, &b);
  for (i=0; i<l; i++)
    luaL_putchar(&b, toupper((unsigned char)(s[i])));
  luaL_pushresult(&b);
  return 1;
}

static int str_rep (lua_State *L) {
  size_t l;
  luaL_Buffer b;
  const char *s = luaL_check_lstr(L, 1, &l);
  int n = luaL_check_int(L, 2);
  luaL_buffinit(L, &b);
  while (n-- > 0)
    luaL_addlstring(&b, s, l);
  luaL_pushresult(&b);
  return 1;
}


static int str_byte (lua_State *L) {
  size_t l;
  const char *s = luaL_check_lstr(L, 1, &l);
  long pos = posrelat(luaL_opt_long(L, 2, 1), l);
  luaL_arg_check(L, 0<pos && (size_t)pos<=l, 2,  "out of range");
  lua_pushnumber(L, (unsigned char)s[pos-1]);
  return 1;
}


static int str_char (lua_State *L) {
  int n = lua_gettop(L);  /* number of arguments */
  int i;
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  for (i=1; i<=n; i++) {
    int c = luaL_check_int(L, i);
    luaL_arg_check(L, (unsigned char)c == c, i, "invalid value");
    luaL_putchar(&b, (unsigned char)c);
  }
  luaL_pushresult(&b);
  return 1;
}



/*
** {======================================================
** PATTERN MATCHING
** =======================================================
*/

#ifndef MAX_CAPTURES
#define MAX_CAPTURES 32  /* arbitrary limit */
#endif


struct Capture {
  const char *src_end;  /* end ('\0') of source string */
  int level;  /* total number of captures (finished or unfinished) */
  struct {
    const char *init;
    long len;  /* -1 signals unfinished capture */
  } capture[MAX_CAPTURES];
};


#define ESC		'%'
#define SPECIALS	"^$*+?.([%-"


static int check_capture (lua_State *L, int l, struct Capture *cap) {
  l -= '1';
  if (!(0 <= l && l < cap->level && cap->capture[l].len != -1))
    lua_error(L, "invalid capture index");
  return l;
}


static int capture_to_close (lua_State *L, struct Capture *cap) {
  int level = cap->level;
  for (level--; level>=0; level--)
    if (cap->capture[level].len == -1) return level;
  lua_error(L, "invalid pattern capture");
  return 0;  /* to avoid warnings */
}


const char *luaI_classend (lua_State *L, const char *p) {
  switch (*p++) {
    case ESC:
      if (*p == '\0') lua_error(L, "malformed pattern (ends with `%')");
      return p+1;
    case '[':
      if (*p == '^') p++;
      do {  /* look for a ']' */
        if (*p == '\0') lua_error(L, "malformed pattern (missing `]')");
        if (*(p++) == ESC && *p != '\0') p++;  /* skip escapes (e.g. '%]') */
      } while (*p != ']');
      return p+1;
    default:
      return p;
  }
}


static int match_class (int c, int cl) {
  int res;
  switch (tolower(cl)) {
    case 'a' : res = isalpha(c); break;
    case 'c' : res = iscntrl(c); break;
    case 'd' : res = isdigit(c); break;
    case 'l' : res = islower(c); break;
    case 'p' : res = ispunct(c); break;
    case 's' : res = isspace(c); break;
    case 'u' : res = isupper(c); break;
    case 'w' : res = isalnum(c); break;
    case 'x' : res = isxdigit(c); break;
    case 'z' : res = (c == '\0'); break;
    default: return (cl == c);
  }
  return (islower(cl) ? res : !res);
}



static int matchbracketclass (int c, const char *p, const char *endclass) {
  int sig = 1;
  if (*(p+1) == '^') {
    sig = 0;
    p++;  /* skip the '^' */
  }
  while (++p < endclass) {
    if (*p == ESC) {
      p++;
      if (match_class(c, (unsigned char)*p))
        return sig;
    }
    else if ((*(p+1) == '-') && (p+2 < endclass)) {
      p+=2;
      if ((int)(unsigned char)*(p-2) <= c && c <= (int)(unsigned char)*p)
        return sig;
    }
    else if ((int)(unsigned char)*p == c) return sig;
  }
  return !sig;
}



int luaI_singlematch (int c, const char *p, const char *ep) {
  switch (*p) {
    case '.':  /* matches any char */
      return 1;
    case ESC:
      return match_class(c, (unsigned char)*(p+1));
    case '[':
      return matchbracketclass(c, p, ep-1);
    default:
      return ((unsigned char)*p == c);
  }
}


static const char *match (lua_State *L, const char *s, const char *p,
                          struct Capture *cap);


static const char *matchbalance (lua_State *L, const char *s, const char *p,
                                 struct Capture *cap) {
  if (*p == 0 || *(p+1) == 0)
    lua_error(L, "unbalanced pattern");
  if (*s != *p) return NULL;
  else {
    int b = *p;
    int e = *(p+1);
    int cont = 1;
    while (++s < cap->src_end) {
      if (*s == e) {
        if (--cont == 0) return s+1;
      }
      else if (*s == b) cont++;
    }
  }
  return NULL;  /* string ends out of balance */
}


static const char *max_expand (lua_State *L, const char *s, const char *p,
                               const char *ep, struct Capture *cap) {
  long i = 0;  /* counts maximum expand for item */
  while ((s+i)<cap->src_end && luaI_singlematch((unsigned char)*(s+i), p, ep))
    i++;
  /* keeps trying to match with the maximum repetitions */
  while (i>=0) {
    const char *res = match(L, (s+i), ep+1, cap);
    if (res) return res;
    i--;  /* else didn't match; reduce 1 repetition to try again */
  }
  return NULL;
}


static const char *min_expand (lua_State *L, const char *s, const char *p,
                               const char *ep, struct Capture *cap) {
  for (;;) {
    const char *res = match(L, s, ep+1, cap);
    if (res != NULL)
      return res;
    else if (s<cap->src_end && luaI_singlematch((unsigned char)*s, p, ep))
      s++;  /* try with one more repetition */
    else return NULL;
  }
}


static const char *start_capture (lua_State *L, const char *s, const char *p,
                                  struct Capture *cap) {
  const char *res;
  int level = cap->level;
  if (level >= MAX_CAPTURES) lua_error(L, "too many captures");
  cap->capture[level].init = s;
  cap->capture[level].len = -1;
  cap->level = level+1;
  if ((res=match(L, s, p+1, cap)) == NULL)  /* match failed? */
    cap->level--;  /* undo capture */
  return res;
}


static const char *end_capture (lua_State *L, const char *s, const char *p,
                                struct Capture *cap) {
  int l = capture_to_close(L, cap);
  const char *res;
  cap->capture[l].len = s - cap->capture[l].init;  /* close capture */
  if ((res = match(L, s, p+1, cap)) == NULL)  /* match failed? */
    cap->capture[l].len = -1;  /* undo capture */
  return res;
}


static const char *match_capture (lua_State *L, const char *s, int level,
                                  struct Capture *cap) {
  int l = check_capture(L, level, cap);
  size_t len = cap->capture[l].len;
  if ((size_t)(cap->src_end-s) >= len &&
      memcmp(cap->capture[l].init, s, len) == 0)
    return s+len;
  else return NULL;
}


static const char *match (lua_State *L, const char *s, const char *p,
                          struct Capture *cap) {
  init: /* using goto's to optimize tail recursion */
  switch (*p) {
    case '(':  /* start capture */
      return start_capture(L, s, p, cap);
    case ')':  /* end capture */
      return end_capture(L, s, p, cap);
    case ESC:  /* may be %[0-9] or %b */
      if (isdigit((unsigned char)(*(p+1)))) {  /* capture? */
        s = match_capture(L, s, *(p+1), cap);
        if (s == NULL) return NULL;
        p+=2; goto init;  /* else return match(L, s, p+2, cap) */
      }
      else if (*(p+1) == 'b') {  /* balanced string? */
        s = matchbalance(L, s, p+2, cap);
        if (s == NULL) return NULL;
        p+=4; goto init;  /* else return match(L, s, p+4, cap); */
      }
      else goto dflt;  /* case default */
    case '\0':  /* end of pattern */
      return s;  /* match succeeded */
    case '$':
      if (*(p+1) == '\0')  /* is the '$' the last char in pattern? */
        return (s == cap->src_end) ? s : NULL;  /* check end of string */
      else goto dflt;
    default: dflt: {  /* it is a pattern item */
      const char *ep = luaI_classend(L, p);  /* points to what is next */
      int m = s<cap->src_end && luaI_singlematch((unsigned char)*s, p, ep);
      switch (*ep) {
        case '?': {  /* optional */
          const char *res;
          if (m && ((res=match(L, s+1, ep+1, cap)) != NULL))
            return res;
          p=ep+1; goto init;  /* else return match(L, s, ep+1, cap); */
        }
        case '*':  /* 0 or more repetitions */
          return max_expand(L, s, p, ep, cap);
        case '+':  /* 1 or more repetitions */
          return (m ? max_expand(L, s+1, p, ep, cap) : NULL);
        case '-':  /* 0 or more repetitions (minimum) */
          return min_expand(L, s, p, ep, cap);
        default:
          if (!m) return NULL;
          s++; p=ep; goto init;  /* else return match(L, s+1, ep, cap); */
      }
    }
  }
}



static const char *lmemfind (const char *s1, size_t l1,
                             const char *s2, size_t l2) {
  if (l2 == 0) return s1;  /* empty strings are everywhere */
  else if (l2 > l1) return NULL;  /* avoids a negative `l1' */
  else {
    const char *init;  /* to search for a `*s2' inside `s1' */
    l2--;  /* 1st char will be checked by `memchr' */
    l1 = l1-l2;  /* `s2' cannot be found after that */
    while (l1 > 0 && (init = (const char *)memchr(s1, *s2, l1)) != NULL) {
      init++;   /* 1st char is already checked */
      if (memcmp(init, s2+1, l2) == 0)
        return init-1;
      else {  /* correct `l1' and `s1' to try again */
        l1 -= init-s1;
        s1 = init;
      }
    }
    return NULL;  /* not found */
  }
}


static int push_captures (lua_State *L, struct Capture *cap) {
  int i;
  luaL_checkstack(L, cap->level, "too many captures");
  for (i=0; i<cap->level; i++) {
    int l = cap->capture[i].len;
    if (l == -1) lua_error(L, "unfinished capture");
    lua_pushlstring(L, cap->capture[i].init, l);
  }
  return cap->level;  /* number of strings pushed */
}


static int str_find (lua_State *L) {
  size_t l1, l2;
  const char *s = luaL_check_lstr(L, 1, &l1);
  const char *p = luaL_check_lstr(L, 2, &l2);
  long init = posrelat(luaL_opt_long(L, 3, 1), l1) - 1;
  struct Capture cap;
  luaL_arg_check(L, 0 <= init && (size_t)init <= l1, 3, "out of range");
  if (lua_gettop(L) > 3 ||  /* extra argument? */
      strpbrk(p, SPECIALS) == NULL) {  /* or no special characters? */
    const char *s2 = lmemfind(s+init, l1-init, p, l2);
    if (s2) {
      lua_pushnumber(L, s2-s+1);
      lua_pushnumber(L, s2-s+l2);
      return 2;
    }
  }
  else {
    int anchor = (*p == '^') ? (p++, 1) : 0;
    const char *s1=s+init;
    cap.src_end = s+l1;
    do {
      const char *res;
      cap.level = 0;
      if ((res=match(L, s1, p, &cap)) != NULL) {
        lua_pushnumber(L, s1-s+1);  /* start */
        lua_pushnumber(L, res-s);   /* end */
        return push_captures(L, &cap) + 2;
      }
    } while (s1++<cap.src_end && !anchor);
  }
  lua_pushnil(L);  /* not found */
  return 1;
}


static void add_s (lua_State *L, luaL_Buffer *b, struct Capture *cap) {
  if (lua_isstring(L, 3)) {
    const char *news = lua_tostring(L, 3);
    size_t l = lua_strlen(L, 3);
    size_t i;
    for (i=0; i<l; i++) {
      if (news[i] != ESC)
        luaL_putchar(b, news[i]);
      else {
        i++;  /* skip ESC */
        if (!isdigit((unsigned char)news[i]))
          luaL_putchar(b, news[i]);
        else {
          int level = check_capture(L, news[i], cap);
          luaL_addlstring(b, cap->capture[level].init, cap->capture[level].len);
        }
      }
    }
  }
  else {  /* is a function */
    int n;
    lua_pushvalue(L, 3);
    n = push_captures(L, cap);
    lua_rawcall(L, n, 1);
    if (lua_isstring(L, -1))
      luaL_addvalue(b);  /* add return to accumulated result */
    else
      lua_pop(L, 1);  /* function result is not a string: pop it */
  }
}


static int str_gsub (lua_State *L) {
  size_t srcl;
  const char *src = luaL_check_lstr(L, 1, &srcl);
  const char *p = luaL_check_string(L, 2);
  int max_s = luaL_opt_int(L, 4, srcl+1);
  int anchor = (*p == '^') ? (p++, 1) : 0;
  int n = 0;
  struct Capture cap;
  luaL_Buffer b;
  luaL_arg_check(L,
    lua_gettop(L) >= 3 && (lua_isstring(L, 3) || lua_isfunction(L, 3)),
    3, "string or function expected");
  luaL_buffinit(L, &b);
  cap.src_end = src+srcl;
  while (n < max_s) {
    const char *e;
    cap.level = 0;
    e = match(L, src, p, &cap);
    if (e) {
      n++;
      add_s(L, &b, &cap);
    }
    if (e && e>src) /* non empty match? */
      src = e;  /* skip it */
    else if (src < cap.src_end)
      luaL_putchar(&b, *src++);
    else break;
    if (anchor) break;
  }
  luaL_addlstring(&b, src, cap.src_end-src);
  luaL_pushresult(&b);
  lua_pushnumber(L, n);  /* number of substitutions */
  return 2;
}

/* }====================================================== */


static void luaI_addquoted (lua_State *L, luaL_Buffer *b, int arg) {
  size_t l;
  const char *s = luaL_check_lstr(L, arg, &l);
  luaL_putchar(b, '"');
  while (l--) {
    switch (*s) {
      case '"':  case '\\':  case '\n':
        luaL_putchar(b, '\\');
        luaL_putchar(b, *s);
        break;
      case '\0': luaL_addlstring(b, "\\000", 4); break;
      default: luaL_putchar(b, *s);
    }
    s++;
  }
  luaL_putchar(b, '"');
}

/* maximum size of each formatted item (> len(format('%99.99f', -1e308))) */
#define MAX_ITEM	512
/* maximum size of each format specification (such as '%-099.99d') */
#define MAX_FORMAT	20

static int str_format (lua_State *L) {
  int arg = 1;
  const char *strfrmt = luaL_check_string(L, arg);
  luaL_Buffer b;
  luaL_buffinit(L, &b);
  while (*strfrmt) {
    if (*strfrmt != '%')
      luaL_putchar(&b, *strfrmt++);
    else if (*++strfrmt == '%')
      luaL_putchar(&b, *strfrmt++);  /* %% */
    else { /* format item */
      struct Capture cap;
      char form[MAX_FORMAT];  /* to store the format ('%...') */
      char buff[MAX_ITEM];  /* to store the formatted item */
      const char *initf = strfrmt;
      form[0] = '%';
      if (isdigit((unsigned char)*initf) && *(initf+1) == '$') {
        arg = *initf - '0';
        initf += 2;  /* skip the 'n$' */
      }
      arg++;
      cap.src_end = strfrmt+strlen(strfrmt)+1;
      cap.level = 0;
      strfrmt = match(L, initf, "[-+ #0]*(%d*)%.?(%d*)", &cap);
      if (cap.capture[0].len > 2 || cap.capture[1].len > 2 ||  /* < 100? */
          strfrmt-initf > MAX_FORMAT-2)
        lua_error(L, "invalid format (width or precision too long)");
      strncpy(form+1, initf, strfrmt-initf+1); /* +1 to include conversion */
      form[strfrmt-initf+2] = 0;
      switch (*strfrmt++) {
        case 'c':  case 'd':  case 'i':
          sprintf(buff, form, luaL_check_int(L, arg));
          break;
        case 'o':  case 'u':  case 'x':  case 'X':
          sprintf(buff, form, (unsigned int)luaL_check_number(L, arg));
          break;
        case 'e':  case 'E': case 'f': case 'g': case 'G':
          sprintf(buff, form, luaL_check_number(L, arg));
          break;
        case 'q':
          luaI_addquoted(L, &b, arg);
          continue;  /* skip the "addsize" at the end */
        case 's': {
          size_t l;
          const char *s = luaL_check_lstr(L, arg, &l);
          if (cap.capture[1].len == 0 && l >= 100) {
            /* no precision and string is too long to be formatted;
               keep original string */
            lua_pushvalue(L, arg);
            luaL_addvalue(&b);
            continue;  /* skip the "addsize" at the end */
          }
          else {
            sprintf(buff, form, s);
            break;
          }
        }
        default:  /* also treat cases 'pnLlh' */
          lua_error(L, "invalid option in `format'");
      }
      luaL_addlstring(&b, buff, strlen(buff));
    }
  }
  luaL_pushresult(&b);
  return 1;
}


static const struct luaL_reg strlib[] = {
{"strlen", str_len},
{"strsub", str_sub},
{"strlower", str_lower},
{"strupper", str_upper},
{"strchar", str_char},
{"strrep", str_rep},
{"ascii", str_byte},  /* for compatibility with 3.0 and earlier */
{"strbyte", str_byte},
{"format", str_format},
{"strfind", str_find},
{"gsub", str_gsub}
};


/*
** Open string library
*/
LUALIB_API void lua_strlibopen (lua_State *L) {
  luaL_openl(L, strlib);
}
/* resumed: mluxsys.c */
/* custom libs: */
/*#include "lbitlib.c"*/
/*#include "luasocket.c"*/
/* include: luxlib.c */
/* Lux extensions to Lua
 * 02/02/2001 jcw@equi4.com
 */
/* skipped: lua.h - see mluxsys.c */
/* skipped: lualib.h - see mluxsys.c */
/* skipped: lauxlib.h - see mluxsys.c */

#ifdef WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <io.h>
#include <fcntl.h>
#include <sys/stat.h>
#else
#ifndef macintosh
#include <sys/types.h>
#include <sys/mman.h>
#endif
#endif

#ifdef NOCOMP
/* include: zlibd.h */
/* zlibd.h - generated from zlib113/zlib.h by onesrc
 * paths: zlib113/
 * Sun Feb 18 14:52:43 PST 2001
 */

/* zlib.h -- interface of the 'zlib' general purpose compression library
  version 1.1.3, July 9th, 1998

  Copyright (C) 1995-1998 Jean-loup Gailly and Mark Adler

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be
     misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.

  Jean-loup Gailly        Mark Adler
  jloup@gzip.org          madler@alumni.caltech.edu


  The data format used by the zlib library is described by RFCs (Request for
  Comments) 1950 to 1952 in the files ftp://ds.internic.net/rfc/rfc1950.txt
  (zlib format), rfc1951.txt (deflate format) and rfc1952.txt (gzip format).
*/

#ifndef _ZLIB_H
#define _ZLIB_H

/* include: zconf.h */
/* zconf.h -- configuration of the zlib compression library
 * Copyright (C) 1995-1998 Jean-loup Gailly.
 * For conditions of distribution and use, see copyright notice in zlib.h 
 */

/* @(#) $Id$ */

#ifndef _ZCONF_H
#define _ZCONF_H

/*
 * If you *really* need a unique prefix for all types and library functions,
 * compile with -DZ_PREFIX. The "standard" zlib should be compiled without it.
 */
#ifdef Z_PREFIX
#  define deflateInit_	z_deflateInit_
#  define deflate	z_deflate
#  define deflateEnd	z_deflateEnd
#  define inflateInit_ 	z_inflateInit_
#  define inflate	z_inflate
#  define inflateEnd	z_inflateEnd
#  define deflateInit2_	z_deflateInit2_
#  define deflateSetDictionary z_deflateSetDictionary
#  define deflateCopy	z_deflateCopy
#  define deflateReset	z_deflateReset
#  define deflateParams	z_deflateParams
#  define inflateInit2_	z_inflateInit2_
#  define inflateSetDictionary z_inflateSetDictionary
#  define inflateSync	z_inflateSync
#  define inflateSyncPoint z_inflateSyncPoint
#  define inflateReset	z_inflateReset
#  define compress	z_compress
#  define compress2	z_compress2
#  define uncompress	z_uncompress
#  define adler32	z_adler32
#  define crc32		z_crc32
#  define get_crc_table z_get_crc_table

#  define Byte		z_Byte
#  define uInt		z_uInt
#  define uLong		z_uLong
#  define Bytef	        z_Bytef
#  define charf		z_charf
#  define intf		z_intf
#  define uIntf		z_uIntf
#  define uLongf	z_uLongf
#  define voidpf	z_voidpf
#  define voidp		z_voidp
#endif

#if (defined(_WIN32) || defined(__WIN32__)) && !defined(WIN32)
#  define WIN32
#endif
#if defined(__GNUC__) || defined(WIN32) || defined(__386__) || defined(i386)
#  ifndef __32BIT__
#    define __32BIT__
#  endif
#endif
#if defined(__MSDOS__) && !defined(MSDOS)
#  define MSDOS
#endif

/*
 * Compile with -DMAXSEG_64K if the alloc function cannot allocate more
 * than 64k bytes at a time (needed on systems with 16-bit int).
 */
#if defined(MSDOS) && !defined(__32BIT__)
#  define MAXSEG_64K
#endif
#ifdef MSDOS
#  define UNALIGNED_OK
#endif

#if (defined(MSDOS) || defined(_WINDOWS) || defined(WIN32))  && !defined(STDC)
#  define STDC
#endif
#if defined(__STDC__) || defined(__cplusplus) || defined(__OS2__)
#  ifndef STDC
#    define STDC
#  endif
#endif

#ifndef STDC
#  ifndef const /* cannot use !defined(STDC) && !defined(const) on Mac */
#    define const
#  endif
#endif

/* Some Mac compilers merge all .h files incorrectly: */
#if defined(__MWERKS__) || defined(applec) ||defined(THINK_C) ||defined(__SC__)
#  define NO_DUMMY_DECL
#endif

/* Old Borland C incorrectly complains about missing returns: */
#if defined(__BORLANDC__) && (__BORLANDC__ < 0x500)
#  define NEED_DUMMY_RETURN
#endif


/* Maximum value for memLevel in deflateInit2 */
#ifndef MAX_MEM_LEVEL
#  ifdef MAXSEG_64K
#    define MAX_MEM_LEVEL 8
#  else
#    define MAX_MEM_LEVEL 9
#  endif
#endif

/* Maximum value for windowBits in deflateInit2 and inflateInit2.
 * WARNING: reducing MAX_WBITS makes minigzip unable to extract .gz files
 * created by gzip. (Files created by minigzip can still be extracted by
 * gzip.)
 */
#ifndef MAX_WBITS
#  define MAX_WBITS   15 /* 32K LZ77 window */
#endif

/* The memory requirements for deflate are (in bytes):
            (1 << (windowBits+2)) +  (1 << (memLevel+9))
 that is: 128K for windowBits=15  +  128K for memLevel = 8  (default values)
 plus a few kilobytes for small objects. For example, if you want to reduce
 the default memory requirements from 256K to 128K, compile with
     make CFLAGS="-O -DMAX_WBITS=14 -DMAX_MEM_LEVEL=7"
 Of course this will generally degrade compression (there's no free lunch).

   The memory requirements for inflate are (in bytes) 1 << windowBits
 that is, 32K for windowBits=15 (default value) plus a few kilobytes
 for small objects.
*/

                        /* Type declarations */

#ifndef OF /* function prototypes */
#  ifdef STDC
#    define OF(args)  args
#  else
#    define OF(args)  ()
#  endif
#endif

/* The following definitions for FAR are needed only for MSDOS mixed
 * model programming (small or medium model with some far allocations).
 * This was tested only with MSC; for other MSDOS compilers you may have
 * to define NO_MEMCPY in zutil.h.  If you don't need the mixed model,
 * just define FAR to be empty.
 */
#if (defined(M_I86SM) || defined(M_I86MM)) && !defined(__32BIT__)
   /* MSC small or medium model */
#  define SMALL_MEDIUM
#  ifdef _MSC_VER
#    define FAR _far
#  else
#    define FAR far
#  endif
#endif
#if defined(__BORLANDC__) && (defined(__SMALL__) || defined(__MEDIUM__))
#  ifndef __32BIT__
#    define SMALL_MEDIUM
#    define FAR _far
#  endif
#endif

/* Compile with -DZLIB_DLL for Windows DLL support */
#if defined(ZLIB_DLL)
#  if defined(_WINDOWS) || defined(WINDOWS)
#    ifdef FAR
#      undef FAR
#    endif
#    include <windows.h>
#    define ZEXPORT  WINAPI
#    ifdef WIN32
#      define ZEXPORTVA  WINAPIV
#    else
#      define ZEXPORTVA  FAR _cdecl _export
#    endif
#  endif
#  if defined (__BORLANDC__)
#    if (__BORLANDC__ >= 0x0500) && defined (WIN32)
#      include <windows.h>
#      define ZEXPORT __declspec(dllexport) WINAPI
#      define ZEXPORTRVA __declspec(dllexport) WINAPIV
#    else
#      if defined (_Windows) && defined (__DLL__)
#        define ZEXPORT _export
#        define ZEXPORTVA _export
#      endif
#    endif
#  endif
#endif

#if defined (__BEOS__)
#  if defined (ZLIB_DLL)
#    define ZEXTERN extern __declspec(dllexport)
#  else
#    define ZEXTERN extern __declspec(dllimport)
#  endif
#endif

#ifndef ZEXPORT
#  define ZEXPORT
#endif
#ifndef ZEXPORTVA
#  define ZEXPORTVA
#endif
#ifndef ZEXTERN
#  define ZEXTERN extern
#endif

#ifndef FAR
#   define FAR
#endif

#if !defined(MACOS) && !defined(TARGET_OS_MAC)
typedef unsigned char  Byte;  /* 8 bits */
#endif
typedef unsigned int   uInt;  /* 16 bits or more */
typedef unsigned long  uLong; /* 32 bits or more */

#ifdef SMALL_MEDIUM
   /* Borland C/C++ and some old MSC versions ignore FAR inside typedef */
#  define Bytef Byte FAR
#else
   typedef Byte  FAR Bytef;
#endif
typedef char  FAR charf;
typedef int   FAR intf;
typedef uInt  FAR uIntf;
typedef uLong FAR uLongf;

#ifdef STDC
   typedef void FAR *voidpf;
   typedef void     *voidp;
#else
   typedef Byte FAR *voidpf;
   typedef Byte     *voidp;
#endif

#ifdef HAVE_UNISTD_H
#  include <sys/types.h> /* for off_t */
#  include <unistd.h>    /* for SEEK_* and off_t */
#  define z_off_t  off_t
#endif
#ifndef SEEK_SET
#  define SEEK_SET        0       /* Seek from beginning of file.  */
#  define SEEK_CUR        1       /* Seek from current position.  */
#  define SEEK_END        2       /* Set file pointer to EOF plus "offset" */
#endif
#ifndef z_off_t
#  define  z_off_t long
#endif

/* MVS linker does not support external names larger than 8 bytes */
#if defined(__MVS__)
#   pragma map(deflateInit_,"DEIN")
#   pragma map(deflateInit2_,"DEIN2")
#   pragma map(deflateEnd,"DEEND")
#   pragma map(inflateInit_,"ININ")
#   pragma map(inflateInit2_,"ININ2")
#   pragma map(inflateEnd,"INEND")
#   pragma map(inflateSync,"INSY")
#   pragma map(inflateSetDictionary,"INSEDI")
#   pragma map(inflate_blocks,"INBL")
#   pragma map(inflate_blocks_new,"INBLNE")
#   pragma map(inflate_blocks_free,"INBLFR")
#   pragma map(inflate_blocks_reset,"INBLRE")
#   pragma map(inflate_codes_free,"INCOFR")
#   pragma map(inflate_codes,"INCO")
#   pragma map(inflate_fast,"INFA")
#   pragma map(inflate_flush,"INFLU")
#   pragma map(inflate_mask,"INMA")
#   pragma map(inflate_set_dictionary,"INSEDI2")
#   pragma map(inflate_copyright,"INCOPY")
#   pragma map(inflate_trees_bits,"INTRBI")
#   pragma map(inflate_trees_dynamic,"INTRDY")
#   pragma map(inflate_trees_fixed,"INTRFI")
#   pragma map(inflate_trees_free,"INTRFR")
#endif

#endif /* _ZCONF_H */
/* resumed: zlib113/zlib.h */

#ifdef __cplusplus
extern "C" {
#endif

#define ZLIB_VERSION "1.1.3"

/* 
     The 'zlib' compression library provides in-memory compression and
  decompression functions, including integrity checks of the uncompressed
  data.  This version of the library supports only one compression method
  (deflation) but other algorithms will be added later and will have the same
  stream interface.

     Compression can be done in a single step if the buffers are large
  enough (for example if an input file is mmap'ed), or can be done by
  repeated calls of the compression function.  In the latter case, the
  application must provide more input and/or consume the output
  (providing more output space) before each call.

     The library also supports reading and writing files in gzip (.gz) format
  with an interface similar to that of stdio.

     The library does not install any signal handler. The decoder checks
  the consistency of the compressed data, so the library should never
  crash even in case of corrupted input.
*/

typedef voidpf (*alloc_func) OF((voidpf opaque, uInt items, uInt size));
typedef void   (*free_func)  OF((voidpf opaque, voidpf address));

struct internal_state;

typedef struct z_stream_s {
    Bytef    *next_in;  /* next input byte */
    uInt     avail_in;  /* number of bytes available at next_in */
    uLong    total_in;  /* total nb of input bytes read so far */

    Bytef    *next_out; /* next output byte should be put there */
    uInt     avail_out; /* remaining free space at next_out */
    uLong    total_out; /* total nb of bytes output so far */

    char     *msg;      /* last error message, NULL if no error */
    struct internal_state FAR *state; /* not visible by applications */

    alloc_func zalloc;  /* used to allocate the internal state */
    free_func  zfree;   /* used to free the internal state */
    voidpf     opaque;  /* private data object passed to zalloc and zfree */

    int     data_type;  /* best guess about the data type: ascii or binary */
    uLong   adler;      /* adler32 value of the uncompressed data */
    uLong   reserved;   /* reserved for future use */
} z_stream;

typedef z_stream FAR *z_streamp;

/*
   The application must update next_in and avail_in when avail_in has
   dropped to zero. It must update next_out and avail_out when avail_out
   has dropped to zero. The application must initialize zalloc, zfree and
   opaque before calling the init function. All other fields are set by the
   compression library and must not be updated by the application.

   The opaque value provided by the application will be passed as the first
   parameter for calls of zalloc and zfree. This can be useful for custom
   memory management. The compression library attaches no meaning to the
   opaque value.

   zalloc must return Z_NULL if there is not enough memory for the object.
   If zlib is used in a multi-threaded application, zalloc and zfree must be
   thread safe.

   On 16-bit systems, the functions zalloc and zfree must be able to allocate
   exactly 65536 bytes, but will not be required to allocate more than this
   if the symbol MAXSEG_64K is defined (see zconf.h). WARNING: On MSDOS,
   pointers returned by zalloc for objects of exactly 65536 bytes *must*
   have their offset normalized to zero. The default allocation function
   provided by this library ensures this (see zutil.c). To reduce memory
   requirements and avoid any allocation of 64K objects, at the expense of
   compression ratio, compile the library with -DMAX_WBITS=14 (see zconf.h).

   The fields total_in and total_out can be used for statistics or
   progress reports. After compression, total_in holds the total size of
   the uncompressed data and may be saved for use in the decompressor
   (particularly if the decompressor wants to decompress everything in
   a single step).
*/

                        /* constants */

#define Z_NO_FLUSH      0
#define Z_PARTIAL_FLUSH 1 /* will be removed, use Z_SYNC_FLUSH instead */
#define Z_SYNC_FLUSH    2
#define Z_FULL_FLUSH    3
#define Z_FINISH        4
/* Allowed flush values; see deflate() below for details */

#define Z_OK            0
#define Z_STREAM_END    1
#define Z_NEED_DICT     2
#define Z_ERRNO        (-1)
#define Z_STREAM_ERROR (-2)
#define Z_DATA_ERROR   (-3)
#define Z_MEM_ERROR    (-4)
#define Z_BUF_ERROR    (-5)
#define Z_VERSION_ERROR (-6)
/* Return codes for the compression/decompression functions. Negative
 * values are errors, positive values are used for special but normal events.
 */

#define Z_NO_COMPRESSION         0
#define Z_BEST_SPEED             1
#define Z_BEST_COMPRESSION       9
#define Z_DEFAULT_COMPRESSION  (-1)
/* compression levels */

#define Z_FILTERED            1
#define Z_HUFFMAN_ONLY        2
#define Z_DEFAULT_STRATEGY    0
/* compression strategy; see deflateInit2() below for details */

#define Z_BINARY   0
#define Z_ASCII    1
#define Z_UNKNOWN  2
/* Possible values of the data_type field */

#define Z_DEFLATED   8
/* The deflate compression method (the only one supported in this version) */

#define Z_NULL  0  /* for initializing zalloc, zfree, opaque */

#define zlib_version zlibVersion()
/* for compatibility with versions < 1.0.2 */

                        /* basic functions */

ZEXTERN const char * ZEXPORT zlibVersion OF((void));
/* The application can compare zlibVersion and ZLIB_VERSION for consistency.
   If the first character differs, the library code actually used is
   not compatible with the zlib.h header file used by the application.
   This check is automatically made by deflateInit and inflateInit.
 */

/* 
ZEXTERN int ZEXPORT deflateInit OF((z_streamp strm, int level));

     Initializes the internal stream state for compression. The fields
   zalloc, zfree and opaque must be initialized before by the caller.
   If zalloc and zfree are set to Z_NULL, deflateInit updates them to
   use default allocation functions.

     The compression level must be Z_DEFAULT_COMPRESSION, or between 0 and 9:
   1 gives best speed, 9 gives best compression, 0 gives no compression at
   all (the input data is simply copied a block at a time).
   Z_DEFAULT_COMPRESSION requests a default compromise between speed and
   compression (currently equivalent to level 6).

     deflateInit returns Z_OK if success, Z_MEM_ERROR if there was not
   enough memory, Z_STREAM_ERROR if level is not a valid compression level,
   Z_VERSION_ERROR if the zlib library version (zlib_version) is incompatible
   with the version assumed by the caller (ZLIB_VERSION).
   msg is set to null if there is no error message.  deflateInit does not
   perform any compression: this will be done by deflate().
*/


ZEXTERN int ZEXPORT deflate OF((z_streamp strm, int flush));
/*
    deflate compresses as much data as possible, and stops when the input
  buffer becomes empty or the output buffer becomes full. It may introduce some
  output latency (reading input without producing any output) except when
  forced to flush.

    The detailed semantics are as follows. deflate performs one or both of the
  following actions:

  - Compress more input starting at next_in and update next_in and avail_in
    accordingly. If not all input can be processed (because there is not
    enough room in the output buffer), next_in and avail_in are updated and
    processing will resume at this point for the next call of deflate().

  - Provide more output starting at next_out and update next_out and avail_out
    accordingly. This action is forced if the parameter flush is non zero.
    Forcing flush frequently degrades the compression ratio, so this parameter
    should be set only when necessary (in interactive applications).
    Some output may be provided even if flush is not set.

  Before the call of deflate(), the application should ensure that at least
  one of the actions is possible, by providing more input and/or consuming
  more output, and updating avail_in or avail_out accordingly; avail_out
  should never be zero before the call. The application can consume the
  compressed output when it wants, for example when the output buffer is full
  (avail_out == 0), or after each call of deflate(). If deflate returns Z_OK
  and with zero avail_out, it must be called again after making room in the
  output buffer because there might be more output pending.

    If the parameter flush is set to Z_SYNC_FLUSH, all pending output is
  flushed to the output buffer and the output is aligned on a byte boundary, so
  that the decompressor can get all input data available so far. (In particular
  avail_in is zero after the call if enough output space has been provided
  before the call.)  Flushing may degrade compression for some compression
  algorithms and so it should be used only when necessary.

    If flush is set to Z_FULL_FLUSH, all output is flushed as with
  Z_SYNC_FLUSH, and the compression state is reset so that decompression can
  restart from this point if previous compressed data has been damaged or if
  random access is desired. Using Z_FULL_FLUSH too often can seriously degrade
  the compression.

    If deflate returns with avail_out == 0, this function must be called again
  with the same value of the flush parameter and more output space (updated
  avail_out), until the flush is complete (deflate returns with non-zero
  avail_out).

    If the parameter flush is set to Z_FINISH, pending input is processed,
  pending output is flushed and deflate returns with Z_STREAM_END if there
  was enough output space; if deflate returns with Z_OK, this function must be
  called again with Z_FINISH and more output space (updated avail_out) but no
  more input data, until it returns with Z_STREAM_END or an error. After
  deflate has returned Z_STREAM_END, the only possible operations on the
  stream are deflateReset or deflateEnd.
  
    Z_FINISH can be used immediately after deflateInit if all the compression
  is to be done in a single step. In this case, avail_out must be at least
  0.1% larger than avail_in plus 12 bytes.  If deflate does not return
  Z_STREAM_END, then it must be called again as described above.

    deflate() sets strm->adler to the adler32 checksum of all input read
  so far (that is, total_in bytes).

    deflate() may update data_type if it can make a good guess about
  the input data type (Z_ASCII or Z_BINARY). In doubt, the data is considered
  binary. This field is only for information purposes and does not affect
  the compression algorithm in any manner.

    deflate() returns Z_OK if some progress has been made (more input
  processed or more output produced), Z_STREAM_END if all input has been
  consumed and all output has been produced (only when flush is set to
  Z_FINISH), Z_STREAM_ERROR if the stream state was inconsistent (for example
  if next_in or next_out was NULL), Z_BUF_ERROR if no progress is possible
  (for example avail_in or avail_out was zero).
*/


ZEXTERN int ZEXPORT deflateEnd OF((z_streamp strm));
/*
     All dynamically allocated data structures for this stream are freed.
   This function discards any unprocessed input and does not flush any
   pending output.

     deflateEnd returns Z_OK if success, Z_STREAM_ERROR if the
   stream state was inconsistent, Z_DATA_ERROR if the stream was freed
   prematurely (some input or output was discarded). In the error case,
   msg may be set but then points to a static string (which must not be
   deallocated).
*/


/* 
ZEXTERN int ZEXPORT inflateInit OF((z_streamp strm));

     Initializes the internal stream state for decompression. The fields
   next_in, avail_in, zalloc, zfree and opaque must be initialized before by
   the caller. If next_in is not Z_NULL and avail_in is large enough (the exact
   value depends on the compression method), inflateInit determines the
   compression method from the zlib header and allocates all data structures
   accordingly; otherwise the allocation will be deferred to the first call of
   inflate.  If zalloc and zfree are set to Z_NULL, inflateInit updates them to
   use default allocation functions.

     inflateInit returns Z_OK if success, Z_MEM_ERROR if there was not enough
   memory, Z_VERSION_ERROR if the zlib library version is incompatible with the
   version assumed by the caller.  msg is set to null if there is no error
   message. inflateInit does not perform any decompression apart from reading
   the zlib header if present: this will be done by inflate().  (So next_in and
   avail_in may be modified, but next_out and avail_out are unchanged.)
*/


ZEXTERN int ZEXPORT inflate OF((z_streamp strm, int flush));
/*
    inflate decompresses as much data as possible, and stops when the input
  buffer becomes empty or the output buffer becomes full. It may some
  introduce some output latency (reading input without producing any output)
  except when forced to flush.

  The detailed semantics are as follows. inflate performs one or both of the
  following actions:

  - Decompress more input starting at next_in and update next_in and avail_in
    accordingly. If not all input can be processed (because there is not
    enough room in the output buffer), next_in is updated and processing
    will resume at this point for the next call of inflate().

  - Provide more output starting at next_out and update next_out and avail_out
    accordingly.  inflate() provides as much output as possible, until there
    is no more input data or no more space in the output buffer (see below
    about the flush parameter).

  Before the call of inflate(), the application should ensure that at least
  one of the actions is possible, by providing more input and/or consuming
  more output, and updating the next_* and avail_* values accordingly.
  The application can consume the uncompressed output when it wants, for
  example when the output buffer is full (avail_out == 0), or after each
  call of inflate(). If inflate returns Z_OK and with zero avail_out, it
  must be called again after making room in the output buffer because there
  might be more output pending.

    If the parameter flush is set to Z_SYNC_FLUSH, inflate flushes as much
  output as possible to the output buffer. The flushing behavior of inflate is
  not specified for values of the flush parameter other than Z_SYNC_FLUSH
  and Z_FINISH, but the current implementation actually flushes as much output
  as possible anyway.

    inflate() should normally be called until it returns Z_STREAM_END or an
  error. However if all decompression is to be performed in a single step
  (a single call of inflate), the parameter flush should be set to
  Z_FINISH. In this case all pending input is processed and all pending
  output is flushed; avail_out must be large enough to hold all the
  uncompressed data. (The size of the uncompressed data may have been saved
  by the compressor for this purpose.) The next operation on this stream must
  be inflateEnd to deallocate the decompression state. The use of Z_FINISH
  is never required, but can be used to inform inflate that a faster routine
  may be used for the single inflate() call.

     If a preset dictionary is needed at this point (see inflateSetDictionary
  below), inflate sets strm-adler to the adler32 checksum of the
  dictionary chosen by the compressor and returns Z_NEED_DICT; otherwise 
  it sets strm->adler to the adler32 checksum of all output produced
  so far (that is, total_out bytes) and returns Z_OK, Z_STREAM_END or
  an error code as described below. At the end of the stream, inflate()
  checks that its computed adler32 checksum is equal to that saved by the
  compressor and returns Z_STREAM_END only if the checksum is correct.

    inflate() returns Z_OK if some progress has been made (more input processed
  or more output produced), Z_STREAM_END if the end of the compressed data has
  been reached and all uncompressed output has been produced, Z_NEED_DICT if a
  preset dictionary is needed at this point, Z_DATA_ERROR if the input data was
  corrupted (input stream not conforming to the zlib format or incorrect
  adler32 checksum), Z_STREAM_ERROR if the stream structure was inconsistent
  (for example if next_in or next_out was NULL), Z_MEM_ERROR if there was not
  enough memory, Z_BUF_ERROR if no progress is possible or if there was not
  enough room in the output buffer when Z_FINISH is used. In the Z_DATA_ERROR
  case, the application may then call inflateSync to look for a good
  compression block.
*/


ZEXTERN int ZEXPORT inflateEnd OF((z_streamp strm));
/*
     All dynamically allocated data structures for this stream are freed.
   This function discards any unprocessed input and does not flush any
   pending output.

     inflateEnd returns Z_OK if success, Z_STREAM_ERROR if the stream state
   was inconsistent. In the error case, msg may be set but then points to a
   static string (which must not be deallocated).
*/

                        /* Advanced functions */

/*
    The following functions are needed only in some special applications.
*/

/*   
ZEXTERN int ZEXPORT deflateInit2 OF((z_streamp strm,
                                     int  level,
                                     int  method,
                                     int  windowBits,
                                     int  memLevel,
                                     int  strategy));

     This is another version of deflateInit with more compression options. The
   fields next_in, zalloc, zfree and opaque must be initialized before by
   the caller.

     The method parameter is the compression method. It must be Z_DEFLATED in
   this version of the library.

     The windowBits parameter is the base two logarithm of the window size
   (the size of the history buffer).  It should be in the range 8..15 for this
   version of the library. Larger values of this parameter result in better
   compression at the expense of memory usage. The default value is 15 if
   deflateInit is used instead.

     The memLevel parameter specifies how much memory should be allocated
   for the internal compression state. memLevel=1 uses minimum memory but
   is slow and reduces compression ratio; memLevel=9 uses maximum memory
   for optimal speed. The default value is 8. See zconf.h for total memory
   usage as a function of windowBits and memLevel.

     The strategy parameter is used to tune the compression algorithm. Use the
   value Z_DEFAULT_STRATEGY for normal data, Z_FILTERED for data produced by a
   filter (or predictor), or Z_HUFFMAN_ONLY to force Huffman encoding only (no
   string match).  Filtered data consists mostly of small values with a
   somewhat random distribution. In this case, the compression algorithm is
   tuned to compress them better. The effect of Z_FILTERED is to force more
   Huffman coding and less string matching; it is somewhat intermediate
   between Z_DEFAULT and Z_HUFFMAN_ONLY. The strategy parameter only affects
   the compression ratio but not the correctness of the compressed output even
   if it is not set appropriately.

      deflateInit2 returns Z_OK if success, Z_MEM_ERROR if there was not enough
   memory, Z_STREAM_ERROR if a parameter is invalid (such as an invalid
   method). msg is set to null if there is no error message.  deflateInit2 does
   not perform any compression: this will be done by deflate().
*/
                            
ZEXTERN int ZEXPORT deflateSetDictionary OF((z_streamp strm,
                                             const Bytef *dictionary,
                                             uInt  dictLength));
/*
     Initializes the compression dictionary from the given byte sequence
   without producing any compressed output. This function must be called
   immediately after deflateInit, deflateInit2 or deflateReset, before any
   call of deflate. The compressor and decompressor must use exactly the same
   dictionary (see inflateSetDictionary).

     The dictionary should consist of strings (byte sequences) that are likely
   to be encountered later in the data to be compressed, with the most commonly
   used strings preferably put towards the end of the dictionary. Using a
   dictionary is most useful when the data to be compressed is short and can be
   predicted with good accuracy; the data can then be compressed better than
   with the default empty dictionary.

     Depending on the size of the compression data structures selected by
   deflateInit or deflateInit2, a part of the dictionary may in effect be
   discarded, for example if the dictionary is larger than the window size in
   deflate or deflate2. Thus the strings most likely to be useful should be
   put at the end of the dictionary, not at the front.

     Upon return of this function, strm->adler is set to the Adler32 value
   of the dictionary; the decompressor may later use this value to determine
   which dictionary has been used by the compressor. (The Adler32 value
   applies to the whole dictionary even if only a subset of the dictionary is
   actually used by the compressor.)

     deflateSetDictionary returns Z_OK if success, or Z_STREAM_ERROR if a
   parameter is invalid (such as NULL dictionary) or the stream state is
   inconsistent (for example if deflate has already been called for this stream
   or if the compression method is bsort). deflateSetDictionary does not
   perform any compression: this will be done by deflate().
*/

ZEXTERN int ZEXPORT deflateCopy OF((z_streamp dest,
                                    z_streamp source));
/*
     Sets the destination stream as a complete copy of the source stream.

     This function can be useful when several compression strategies will be
   tried, for example when there are several ways of pre-processing the input
   data with a filter. The streams that will be discarded should then be freed
   by calling deflateEnd.  Note that deflateCopy duplicates the internal
   compression state which can be quite large, so this strategy is slow and
   can consume lots of memory.

     deflateCopy returns Z_OK if success, Z_MEM_ERROR if there was not
   enough memory, Z_STREAM_ERROR if the source stream state was inconsistent
   (such as zalloc being NULL). msg is left unchanged in both source and
   destination.
*/

ZEXTERN int ZEXPORT deflateReset OF((z_streamp strm));
/*
     This function is equivalent to deflateEnd followed by deflateInit,
   but does not free and reallocate all the internal compression state.
   The stream will keep the same compression level and any other attributes
   that may have been set by deflateInit2.

      deflateReset returns Z_OK if success, or Z_STREAM_ERROR if the source
   stream state was inconsistent (such as zalloc or state being NULL).
*/

ZEXTERN int ZEXPORT deflateParams OF((z_streamp strm,
				      int level,
				      int strategy));
/*
     Dynamically update the compression level and compression strategy.  The
   interpretation of level and strategy is as in deflateInit2.  This can be
   used to switch between compression and straight copy of the input data, or
   to switch to a different kind of input data requiring a different
   strategy. If the compression level is changed, the input available so far
   is compressed with the old level (and may be flushed); the new level will
   take effect only at the next call of deflate().

     Before the call of deflateParams, the stream state must be set as for
   a call of deflate(), since the currently available input may have to
   be compressed and flushed. In particular, strm->avail_out must be non-zero.

     deflateParams returns Z_OK if success, Z_STREAM_ERROR if the source
   stream state was inconsistent or if a parameter was invalid, Z_BUF_ERROR
   if strm->avail_out was zero.
*/

/*   
ZEXTERN int ZEXPORT inflateInit2 OF((z_streamp strm,
                                     int  windowBits));

     This is another version of inflateInit with an extra parameter. The
   fields next_in, avail_in, zalloc, zfree and opaque must be initialized
   before by the caller.

     The windowBits parameter is the base two logarithm of the maximum window
   size (the size of the history buffer).  It should be in the range 8..15 for
   this version of the library. The default value is 15 if inflateInit is used
   instead. If a compressed stream with a larger window size is given as
   input, inflate() will return with the error code Z_DATA_ERROR instead of
   trying to allocate a larger window.

      inflateInit2 returns Z_OK if success, Z_MEM_ERROR if there was not enough
   memory, Z_STREAM_ERROR if a parameter is invalid (such as a negative
   memLevel). msg is set to null if there is no error message.  inflateInit2
   does not perform any decompression apart from reading the zlib header if
   present: this will be done by inflate(). (So next_in and avail_in may be
   modified, but next_out and avail_out are unchanged.)
*/

ZEXTERN int ZEXPORT inflateSetDictionary OF((z_streamp strm,
                                             const Bytef *dictionary,
                                             uInt  dictLength));
/*
     Initializes the decompression dictionary from the given uncompressed byte
   sequence. This function must be called immediately after a call of inflate
   if this call returned Z_NEED_DICT. The dictionary chosen by the compressor
   can be determined from the Adler32 value returned by this call of
   inflate. The compressor and decompressor must use exactly the same
   dictionary (see deflateSetDictionary).

     inflateSetDictionary returns Z_OK if success, Z_STREAM_ERROR if a
   parameter is invalid (such as NULL dictionary) or the stream state is
   inconsistent, Z_DATA_ERROR if the given dictionary doesn't match the
   expected one (incorrect Adler32 value). inflateSetDictionary does not
   perform any decompression: this will be done by subsequent calls of
   inflate().
*/

ZEXTERN int ZEXPORT inflateSync OF((z_streamp strm));
/* 
    Skips invalid compressed data until a full flush point (see above the
  description of deflate with Z_FULL_FLUSH) can be found, or until all
  available input is skipped. No output is provided.

    inflateSync returns Z_OK if a full flush point has been found, Z_BUF_ERROR
  if no more input was provided, Z_DATA_ERROR if no flush point has been found,
  or Z_STREAM_ERROR if the stream structure was inconsistent. In the success
  case, the application may save the current current value of total_in which
  indicates where valid compressed data was found. In the error case, the
  application may repeatedly call inflateSync, providing more input each time,
  until success or end of the input data.
*/

ZEXTERN int ZEXPORT inflateReset OF((z_streamp strm));
/*
     This function is equivalent to inflateEnd followed by inflateInit,
   but does not free and reallocate all the internal decompression state.
   The stream will keep attributes that may have been set by inflateInit2.

      inflateReset returns Z_OK if success, or Z_STREAM_ERROR if the source
   stream state was inconsistent (such as zalloc or state being NULL).
*/


                        /* utility functions */

/*
     The following utility functions are implemented on top of the
   basic stream-oriented functions. To simplify the interface, some
   default options are assumed (compression level and memory usage,
   standard memory allocation functions). The source code of these
   utility functions can easily be modified if you need special options.
*/

ZEXTERN int ZEXPORT compress OF((Bytef *dest,   uLongf *destLen,
                                 const Bytef *source, uLong sourceLen));
/*
     Compresses the source buffer into the destination buffer.  sourceLen is
   the byte length of the source buffer. Upon entry, destLen is the total
   size of the destination buffer, which must be at least 0.1% larger than
   sourceLen plus 12 bytes. Upon exit, destLen is the actual size of the
   compressed buffer.
     This function can be used to compress a whole file at once if the
   input file is mmap'ed.
     compress returns Z_OK if success, Z_MEM_ERROR if there was not
   enough memory, Z_BUF_ERROR if there was not enough room in the output
   buffer.
*/

ZEXTERN int ZEXPORT compress2 OF((Bytef *dest,   uLongf *destLen,
                                  const Bytef *source, uLong sourceLen,
                                  int level));
/*
     Compresses the source buffer into the destination buffer. The level
   parameter has the same meaning as in deflateInit.  sourceLen is the byte
   length of the source buffer. Upon entry, destLen is the total size of the
   destination buffer, which must be at least 0.1% larger than sourceLen plus
   12 bytes. Upon exit, destLen is the actual size of the compressed buffer.

     compress2 returns Z_OK if success, Z_MEM_ERROR if there was not enough
   memory, Z_BUF_ERROR if there was not enough room in the output buffer,
   Z_STREAM_ERROR if the level parameter is invalid.
*/

ZEXTERN int ZEXPORT uncompress OF((Bytef *dest,   uLongf *destLen,
                                   const Bytef *source, uLong sourceLen));
/*
     Decompresses the source buffer into the destination buffer.  sourceLen is
   the byte length of the source buffer. Upon entry, destLen is the total
   size of the destination buffer, which must be large enough to hold the
   entire uncompressed data. (The size of the uncompressed data must have
   been saved previously by the compressor and transmitted to the decompressor
   by some mechanism outside the scope of this compression library.)
   Upon exit, destLen is the actual size of the compressed buffer.
     This function can be used to decompress a whole file at once if the
   input file is mmap'ed.

     uncompress returns Z_OK if success, Z_MEM_ERROR if there was not
   enough memory, Z_BUF_ERROR if there was not enough room in the output
   buffer, or Z_DATA_ERROR if the input data was corrupted.
*/


typedef voidp gzFile;

ZEXTERN gzFile ZEXPORT gzopen  OF((const char *path, const char *mode));
/*
     Opens a gzip (.gz) file for reading or writing. The mode parameter
   is as in fopen ("rb" or "wb") but can also include a compression level
   ("wb9") or a strategy: 'f' for filtered data as in "wb6f", 'h' for
   Huffman only compression as in "wb1h". (See the description
   of deflateInit2 for more information about the strategy parameter.)

     gzopen can be used to read a file which is not in gzip format; in this
   case gzread will directly read from the file without decompression.

     gzopen returns NULL if the file could not be opened or if there was
   insufficient memory to allocate the (de)compression state; errno
   can be checked to distinguish the two cases (if errno is zero, the
   zlib error is Z_MEM_ERROR).  */

ZEXTERN gzFile ZEXPORT gzdopen  OF((int fd, const char *mode));
/*
     gzdopen() associates a gzFile with the file descriptor fd.  File
   descriptors are obtained from calls like open, dup, creat, pipe or
   fileno (in the file has been previously opened with fopen).
   The mode parameter is as in gzopen.
     The next call of gzclose on the returned gzFile will also close the
   file descriptor fd, just like fclose(fdopen(fd), mode) closes the file
   descriptor fd. If you want to keep fd open, use gzdopen(dup(fd), mode).
     gzdopen returns NULL if there was insufficient memory to allocate
   the (de)compression state.
*/

ZEXTERN int ZEXPORT gzsetparams OF((gzFile file, int level, int strategy));
/*
     Dynamically update the compression level or strategy. See the description
   of deflateInit2 for the meaning of these parameters.
     gzsetparams returns Z_OK if success, or Z_STREAM_ERROR if the file was not
   opened for writing.
*/

ZEXTERN int ZEXPORT    gzread  OF((gzFile file, voidp buf, unsigned len));
/*
     Reads the given number of uncompressed bytes from the compressed file.
   If the input file was not in gzip format, gzread copies the given number
   of bytes into the buffer.
     gzread returns the number of uncompressed bytes actually read (0 for
   end of file, -1 for error). */

ZEXTERN int ZEXPORT    gzwrite OF((gzFile file, 
				   const voidp buf, unsigned len));
/*
     Writes the given number of uncompressed bytes into the compressed file.
   gzwrite returns the number of uncompressed bytes actually written
   (0 in case of error).
*/

ZEXTERN int ZEXPORTVA   gzprintf OF((gzFile file, const char *format, ...));
/*
     Converts, formats, and writes the args to the compressed file under
   control of the format string, as in fprintf. gzprintf returns the number of
   uncompressed bytes actually written (0 in case of error).
*/

ZEXTERN int ZEXPORT gzputs OF((gzFile file, const char *s));
/*
      Writes the given null-terminated string to the compressed file, excluding
   the terminating null character.
      gzputs returns the number of characters written, or -1 in case of error.
*/

ZEXTERN char * ZEXPORT gzgets OF((gzFile file, char *buf, int len));
/*
      Reads bytes from the compressed file until len-1 characters are read, or
   a newline character is read and transferred to buf, or an end-of-file
   condition is encountered.  The string is then terminated with a null
   character.
      gzgets returns buf, or Z_NULL in case of error.
*/

ZEXTERN int ZEXPORT    gzputc OF((gzFile file, int c));
/*
      Writes c, converted to an unsigned char, into the compressed file.
   gzputc returns the value that was written, or -1 in case of error.
*/

ZEXTERN int ZEXPORT    gzgetc OF((gzFile file));
/*
      Reads one byte from the compressed file. gzgetc returns this byte
   or -1 in case of end of file or error.
*/

ZEXTERN int ZEXPORT    gzflush OF((gzFile file, int flush));
/*
     Flushes all pending output into the compressed file. The parameter
   flush is as in the deflate() function. The return value is the zlib
   error number (see function gzerror below). gzflush returns Z_OK if
   the flush parameter is Z_FINISH and all output could be flushed.
     gzflush should be called only when strictly necessary because it can
   degrade compression.
*/

ZEXTERN z_off_t ZEXPORT    gzseek OF((gzFile file,
				      z_off_t offset, int whence));
/* 
      Sets the starting position for the next gzread or gzwrite on the
   given compressed file. The offset represents a number of bytes in the
   uncompressed data stream. The whence parameter is defined as in lseek(2);
   the value SEEK_END is not supported.
     If the file is opened for reading, this function is emulated but can be
   extremely slow. If the file is opened for writing, only forward seeks are
   supported; gzseek then compresses a sequence of zeroes up to the new
   starting position.

      gzseek returns the resulting offset location as measured in bytes from
   the beginning of the uncompressed stream, or -1 in case of error, in
   particular if the file is opened for writing and the new starting position
   would be before the current position.
*/

ZEXTERN int ZEXPORT    gzrewind OF((gzFile file));
/*
     Rewinds the given file. This function is supported only for reading.

   gzrewind(file) is equivalent to (int)gzseek(file, 0L, SEEK_SET)
*/

ZEXTERN z_off_t ZEXPORT    gztell OF((gzFile file));
/*
     Returns the starting position for the next gzread or gzwrite on the
   given compressed file. This position represents a number of bytes in the
   uncompressed data stream.

   gztell(file) is equivalent to gzseek(file, 0L, SEEK_CUR)
*/

ZEXTERN int ZEXPORT gzeof OF((gzFile file));
/*
     Returns 1 when EOF has previously been detected reading the given
   input stream, otherwise zero.
*/

ZEXTERN int ZEXPORT    gzclose OF((gzFile file));
/*
     Flushes all pending output if necessary, closes the compressed file
   and deallocates all the (de)compression state. The return value is the zlib
   error number (see function gzerror below).
*/

ZEXTERN const char * ZEXPORT gzerror OF((gzFile file, int *errnum));
/*
     Returns the error message for the last error which occurred on the
   given compressed file. errnum is set to zlib error number. If an
   error occurred in the file system and not in the compression library,
   errnum is set to Z_ERRNO and the application may consult errno
   to get the exact error code.
*/

                        /* checksum functions */

/*
     These functions are not related to compression but are exported
   anyway because they might be useful in applications using the
   compression library.
*/

ZEXTERN uLong ZEXPORT adler32 OF((uLong adler, const Bytef *buf, uInt len));

/*
     Update a running Adler-32 checksum with the bytes buf[0..len-1] and
   return the updated checksum. If buf is NULL, this function returns
   the required initial value for the checksum.
   An Adler-32 checksum is almost as reliable as a CRC32 but can be computed
   much faster. Usage example:

     uLong adler = adler32(0L, Z_NULL, 0);

     while (read_buffer(buffer, length) != EOF) {
       adler = adler32(adler, buffer, length);
     }
     if (adler != original_adler) error();
*/

ZEXTERN uLong ZEXPORT crc32   OF((uLong crc, const Bytef *buf, uInt len));
/*
     Update a running crc with the bytes buf[0..len-1] and return the updated
   crc. If buf is NULL, this function returns the required initial value
   for the crc. Pre- and post-conditioning (one's complement) is performed
   within this function so it shouldn't be done by the application.
   Usage example:

     uLong crc = crc32(0L, Z_NULL, 0);

     while (read_buffer(buffer, length) != EOF) {
       crc = crc32(crc, buffer, length);
     }
     if (crc != original_crc) error();
*/


                        /* various hacks, don't look :) */

/* deflateInit and inflateInit are macros to allow checking the zlib version
 * and the compiler's view of z_stream:
 */
ZEXTERN int ZEXPORT deflateInit_ OF((z_streamp strm, int level,
                                     const char *version, int stream_size));
ZEXTERN int ZEXPORT inflateInit_ OF((z_streamp strm,
                                     const char *version, int stream_size));
ZEXTERN int ZEXPORT deflateInit2_ OF((z_streamp strm, int  level, int  method,
                                      int windowBits, int memLevel,
                                      int strategy, const char *version,
                                      int stream_size));
ZEXTERN int ZEXPORT inflateInit2_ OF((z_streamp strm, int  windowBits,
                                      const char *version, int stream_size));
#define deflateInit(strm, level) \
        deflateInit_((strm), (level),       ZLIB_VERSION, sizeof(z_stream))
#define inflateInit(strm) \
        inflateInit_((strm),                ZLIB_VERSION, sizeof(z_stream))
#define deflateInit2(strm, level, method, windowBits, memLevel, strategy) \
        deflateInit2_((strm),(level),(method),(windowBits),(memLevel),\
                      (strategy),           ZLIB_VERSION, sizeof(z_stream))
#define inflateInit2(strm, windowBits) \
        inflateInit2_((strm), (windowBits), ZLIB_VERSION, sizeof(z_stream))


#if !defined(_Z_UTIL_H) && !defined(NO_DUMMY_DECL)
//JCW    struct internal_state {int dummy;}; /* hack for buggy compilers */
#endif

ZEXTERN const char   * ZEXPORT zError           OF((int err));
ZEXTERN int            ZEXPORT inflateSyncPoint OF((z_streamp z));
ZEXTERN const uLongf * ZEXPORT get_crc_table    OF((void));

#ifdef __cplusplus
}
#endif

#endif /* _ZLIB_H */
/* resumed: ./luxlib.c */
#else
#include <zlib.h>
#endif

#ifdef WIN32
typedef __int64 I64;
#else
typedef long long I64;
#endif

/* prototype */
LUALIB_API void luxlib_open(lua_State *L);
/* TODO: get rid of static ints, use closures instead */
static int luxmemtag;
/* lux_Type - type of memory chunks */
enum { lux_raw, lux_heap, lux_str, lux_file };
/* lux_Mem - userdata for each memmap */
typedef struct {
  char *ptr;
  size_t len;
  int type;
  union { FILE* fp; int ref; } u;
} lux_Mem;

/* lux_memhandle - type-safe conversion of userdata to lux_Mem ptr */
static lux_Mem* lux_memhandle(lua_State *L, int f) {
  void *p = lua_touserdata(L, f);
  if (p == NULL || lua_tag(L, f) != luxmemtag)
    lua_error(L, "wrong type - mem map expected");
  return p;
}
/* lux_mmclose - close memmap, cleaning up as appropriate */
static int lux_mmclose(lua_State *L) {
  lux_Mem *m = (lux_Mem*) lux_memhandle(L, -1);
  switch (m->type) {
    case lux_heap: free(m->ptr); break;
    case lux_str: lua_unref(L, m->u.ref); break;
    case lux_file:
#if defined(macintosh)
      break;
#elif defined(WIN32)
      UnmapViewOfFile(m->ptr); fclose(m->u.fp); break;
#else
      munmap(m->ptr, m->len); fclose(m->u.fp); break;
#endif
  }
  m->type = lux_raw;
  m->ptr = 0;
  m->len = 0;
  return 0;
}
/* lux_newmem - create a new memmap, as userdata structure */
static lux_Mem *lux_newmem(lua_State *L, int t, char *p, size_t n) {
  lux_Mem *m = (lux_Mem*) lua_newuserdata(L, sizeof (lux_Mem));
  lua_settag(L, luxmemtag);
  m->type = t;
  m->ptr = p;
  m->len = n;
  return m; /* also leaves new userdata on stack */
}
/* lux_mmraw - create a memmap from raw memory (dangerous) */
static int lux_mmraw(lua_State *L) {
  void* ptr = (void*) luaL_check_long(L, 1);
  size_t len = luaL_check_long(L, 2);
  (void) lux_newmem(L, lux_raw, ptr, len);
  return 1;
}
/* lux_mmheap - create a memmap from an allocated chunk of memory */
static int lux_mmheap(lua_State *L) {
  size_t len = luaL_check_long(L, 1);
  (void) lux_newmem(L, lux_heap, malloc(len), len);
  return 1;
}
/* lux_mmstr - create a memmap from a Lua string (shares memory) */
static int lux_mmstr(lua_State *L) {
  size_t len;
  char *ptr = (char*) luaL_check_lstr(L, -1, &len);
  int ref = lua_ref(L, 1);
  lux_Mem *m = lux_newmem(L, lux_str, ptr, len);
  m->u.ref = ref;
  return 1;
}
/* lux_mmfile - create a memmap from a file, specified by name */
static int lux_mmfile(lua_State *L) {
  char *ptr;
  size_t len;
  lux_Mem *m;
  FILE *fp = fopen(luaL_check_string(L, 1), "rb");
  if (fp == NULL) lua_error(L, "cannot open file");
  fseek(fp, 0, SEEK_END);
  len = ftell(fp);
#if defined(macintosh)
  ptr = malloc(len);
  fseek(fp, 0, SEEK_SET);
  if (ptr != NULL) fread(ptr, len, 1, fp); //XXX error handling
  fclose(fp);
  fp = NULL;
#elif defined(WIN32)
  {
    HANDLE h = CreateFileMapping((HANDLE) _get_osfhandle(_fileno(fp)),
					0, PAGE_READONLY, 0, len, 0);
    ptr = h ? MapViewOfFile(h, FILE_MAP_READ, 0, 0, len) : NULL;
  }
#else
  ptr = mmap(0, len, PROT_READ, MAP_PRIVATE, fileno(fp), 0);
#endif
  if (ptr == NULL) {
    fclose(fp);
    lua_error(L, "cannot map file");
  }
  m = lux_newmem(L, lux_file, ptr, len);
  m->u.fp = fp;
  return 1;
}
/* lux_mminfo - return type, address, and length of this memmap */
static int lux_mminfo(lua_State *L) {
  lux_Mem *m = lux_memhandle(L, 1);
  if (m->len <= 0) return 0;
  lua_pushnumber(L, (long) m->ptr);
  lua_pushnumber(L, m->len);
  lua_pushnumber(L, m->type);
  return 3;
}
/* lux_mmsub - return a sub-string copy made from this memmap */
static int lux_mmsub(lua_State *L) {
  lux_Mem *m = lux_memhandle(L, 1);
  int i = luaL_opt_int(L, 2, 1);
  int j = luaL_opt_int(L, 3, -1);
  /* note: the following code also converts to 0-based [i..j) */
  i += i < 0 ? m->len : -1;
  if (j < 0) j += m->len + 1;
  /* if (i < 0 || j > m->len || i > j) return 0; */
  if (i < 0) i = 0;
  if (j > (int) m->len) j = m->len;
  if (i > j) i = j;
  lua_pushlstring(L, m->ptr + i, j - i);
  return 1;
}
/* lux_zadler32 - calculate the Adler-32 checksum of specified memmap */
static int lux_zadler32(lua_State *L) {
  lux_Mem *m = lux_memhandle(L, 1);
  long s = luaL_opt_long(L, 2, adler32(0,0,0));
  lua_pushnumber(L, adler32(s, (const Bytef*) m->ptr, m->len));
  return 1;
}
/* lux_zcrc32 - calculate the CRC-32 checksum of specified memmap */
static int lux_zcrc32(lua_State *L) {
  lux_Mem *m = lux_memhandle(L, 1);
  long s = luaL_opt_long(L, 2, crc32(0,0,0));
  lua_pushnumber(L, crc32(s, (const Bytef*) m->ptr, m->len));
  return 1;
}
#ifndef NOCOMP
/* lux_zcomp - perform zlib compression on specified memmap */
static int lux_zcomp(lua_State *L) {
  int err;
  z_stream zs;
  Bytef *buffer;
  lux_Mem *m = lux_memhandle(L, 1);
  int wbits = luaL_opt_int(L, 2, 0) < 0 ? -MAX_WBITS : MAX_WBITS;
  int level = luaL_opt_int(L, 3, Z_DEFAULT_COMPRESSION);
  zs.avail_in = m->len;
  zs.next_in = m->ptr;
  zs.avail_out = m->len + m->len / 1000 + 12;
  zs.next_out = buffer = malloc(zs.avail_out);
  zs.zalloc = 0;
  zs.zfree = 0;
  zs.opaque = 0;
  err = deflateInit2(&zs, level, Z_DEFLATED, wbits,
      			MAX_MEM_LEVEL, Z_DEFAULT_STRATEGY);
  if (err == Z_OK) {
    err = deflate(&zs, Z_FINISH);
    if (err != Z_STREAM_END) {
      deflateEnd(&zs);
      if (err == Z_OK) err = Z_BUF_ERROR;
    } else
      err = deflateEnd(&zs);
  }
  if (err != Z_OK) {
    free(buffer);
    lua_error(L, zError(err));
  }
  (void) lux_newmem(L, lux_heap,
			realloc(buffer, zs.total_out), zs.total_out);
  return 1;
}
#endif
/* lux_zdecomp - perform zlib decompression on specified memmap */
static int lux_zdecomp(lua_State *L) {
  int err;
  z_stream zs;
  Bytef *buffer;
  lux_Mem *m = lux_memhandle(L, 1);
  int wbits = luaL_opt_int(L, 2, 0) < 0 ? -MAX_WBITS : MAX_WBITS;
  int bufsize = luaL_opt_int(L, 3, 16*1024);
  for (;;) {
    zs.zalloc = 0;
    zs.zfree = 0;
    zs.avail_in = m->len + 1; /* +1 is required by zlib */
    zs.next_in = (Bytef*) m->ptr;
    zs.avail_out = bufsize;
    zs.next_out = buffer = malloc(bufsize);
    err = inflateInit2(&zs, wbits);
    if (err == Z_OK) {
      err = inflate(&zs, Z_FINISH);
      if (err != Z_STREAM_END) {
	inflateEnd(&zs);
	if (err == Z_OK) err = Z_BUF_ERROR;
      } else
	err = inflateEnd(&zs);
    }
    if (err == Z_OK) break;
    free(buffer);
    if (err != Z_BUF_ERROR) lua_error(L, zError(err));
    bufsize *= 2;
  }
  (void) lux_newmem(L, lux_heap,
			realloc(buffer, zs.total_out), zs.total_out);
  return 1;
}
/* logical operations, modeled after bitlib by Reuben Thomas */
#define LCN(a) ((I64) luaL_check_number(L,a))
static int lux_imod(lua_State *L) {
  lua_pushnumber(L, (double) (LCN(1) % LCN(2)));
  return 1;
}
static int lux_band(lua_State *L) {
  lua_pushnumber(L, (double) (LCN(1) & LCN(2)));
  return 1;
}
static int lux_bor(lua_State *L) {
  lua_pushnumber(L, (double) (LCN(1) | LCN(2)));
  return 1;
}
static int lux_bxor(lua_State *L) {
  lua_pushnumber(L, (double) (LCN(1) ^ LCN(2)));
  return 1;
}
static int lux_lshift(lua_State *L) {
  /* this operation can cause roundoff errors */
  lua_pushnumber(L, (double) (LCN(1) << luaL_check_int(L, 2)));
  return 1;
}
static int lux_rshift(lua_State *L) { /* differs from bitlib! */
  lua_pushnumber(L, (double) (LCN(1) >> luaL_check_int(L, 2)));
  return 1;
}
#undef LCN
/* lux_luxlibvers - get at the library build date and version number */
static int lux_luxlibvers(lua_State *L) {
  lua_pushstring(L, __DATE__);
  lua_pushnumber(L, 11);
  return 2;
}
/* luxlib - functions defined in this extension */
static struct luaL_reg luxlib[] = {
  {"mmraw", lux_mmraw},
  {"mmheap", lux_mmheap},
  {"mmstr", lux_mmstr},
  {"mmfile", lux_mmfile},
  {"mmclose", lux_mmclose},
  {"mminfo", lux_mminfo},
  {"mmsub", lux_mmsub},
  {"zadler32", lux_zadler32},
  {"zcrc32", lux_zcrc32},
#ifndef NOCOMP
  {"zcomp", lux_zcomp},
#endif
  {"zdecomp", lux_zdecomp},
  {"imod", lux_imod},
  {"band", lux_band},
  {"bor", lux_bor},
  {"bxor", lux_bxor},
  {"lshift", lux_lshift},
  {"rshift", lux_rshift},
  {"luxlibvers", lux_luxlibvers},
};
/* luxlib_open - the one and only public entry point */
void luxlib_open(lua_State *L) {
  luxmemtag = lua_newtag(L);
  lua_pushcfunction(L, lux_mmclose);
  lua_settagmethod(L, luxmemtag, "gc");
  luaL_openl(L, luxlib);
}
/* resumed: mluxsys.c */
#ifndef WIN32
/*#include "lposlib.c"*/
#endif
#ifndef WIN32
#define DLFCN
#endif
#ifndef NODYN
/* include: dynlib.c */
/* Support for dynamic loading of Lua extensions
 * 17/02/2001 jcw@equi4.com
 */

#if defined (macintosh)
  #define qMac  1
#elif defined (WIN32)
  #define qWin  1
#elif defined (unix) || defined (__unix__) || defined (__GNUC__)
  #define qUnix 1
#endif

#if qMac
  #include <CodeFragments.h>
#elif qWin
  #define WIN32_LEAN_AND_MEAN
  #include <windows.h>
#elif qUnix
  #include <dlfcn.h>
#endif

static int dynopen(lua_State *L)
{
  void* h = 0;
  const char *name = luaL_check_string(L, 1);
#if qMac
  CFragConnectionID connID;
  FSSpec fileSpec;
  OSErr err;
  Str255 errName;
  Str255 packageName;
  Ptr dummy;
/* MacOS: */
  /*err = PBMakeFSSpecSync(HParmBlkPtr paramBlock);*/
/* Tcl: */
  /*err = FSpLocationFromPath(strlen(name), name, &fileSpec);*/
/* Metrowerks: */
  err = __path2fss(name, &fileSpec);
  if (err != noErr)
    return 0;
  c2pstr(strcpy((char*) packageName, name));
  err = GetDiskFragment(&fileSpec, 0, 0, packageName,
			kLoadCFrag, &connID, &dummy, errName);
  if (err != noErr) {
    lua_pushnil(L);
    lua_pushnumber(L, err);
    lua_pushstring(L, p2cstr(errName));
    return 3;
  }
  h = connID;
#elif qWin
  h = LoadLibrary(name);
  /* h = LoadLibraryEx(name, 0, LOAD_WITH_ALTERED_SEARCH_PATH); */
  if (h == 0) {
    lua_pushnil(L);
    lua_pushnumber(L, GetLastError());
    return 2;
  }
#elif qUnix
  h = dlopen(name, RTLD_NOW | RTLD_GLOBAL);
  if (h == 0) {
    lua_pushnil(L);
    lua_pushstring(L, dlerror());
    return 2;
  }
#endif
  lua_pushuserdata(L, h);
  return 1;
}

static int dyncall(lua_State *L)
{
  void *h, *handle = lua_touserdata(L, 1);
  const char *symbol = luaL_check_string(L, 2);
  if (handle == NULL)
    return 0;
#if qMac
  CFragSymbolClass symClass;
  OSErr err;
  Str255 symbolName;
  Ptr proc;
  
  c2pstr(strcpy((char*) symbolName, symbol));
  err = FindSymbol(handle, symbolName, &proc, &symClass);
  if (err == noErr)
    h = proc;
#elif qWin
  h = GetProcAddress((HINSTANCE) handle, symbol);
#elif qUnix
  h = dlsym(handle, symbol);
#endif
  if (h == 0)
    return 0;
  return ((lua_CFunction) h)(L);
}

static int dynclose(lua_State *L)
{
  void *handle = lua_touserdata(L, 1);
  if (handle != NULL) {
#if qMac
    CloseConnection(handle);
#elif qWin
    FreeLibrary((HINSTANCE) handle);
#elif qUnix
    dlclose(handle);
#endif
  }
  return 0;
}

static struct luaL_reg dynlib[] = {
  {"dynopen", dynopen},
  {"dyncall", dyncall},
  {"dynclose", dynclose},
};

extern void dynlib_open(lua_State *L);

void dynlib_open(lua_State *L)
{
  luaL_openl(L, dynlib);
}
/* resumed: mluxsys.c */
#endif
#endif

extern lua_State *luxsys_open();

lua_State *luxsys_open() {
  lua_State* L = lua_open(0);
#ifndef MINIMAL
  lua_baselibopen(L);
  lua_iolibopen(L);
  lua_strlibopen(L);
  lua_mathlibopen(L);
  lua_dblibopen(L);
  /*lua_bitlibopen(L);*/
  /*lua_socketlibopen(L);*/
  luxlib_open(L);
#ifndef WIN32
  /*lua_poslibopen(L);*/
#endif
#ifndef NODYN
  dynlib_open(L);
#endif
#endif
/* include: preload.c */

{ /* begin embedded code */
  static unsigned char B1[] = { /* luac */ 27,76,117,97,64,1,4,4,4,32,6,9,8,
    18,230,91,161,176,185,178,65,8,0,0,0,61,40,110,111,110,101,41,0,0,0,0,0,
    0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,4,0,0,0,108,117,120,0,6,0,0,0,
    108,101,73,110,116,0,10,0,0,0,108,101,83,116,114,67,117,116,115,0,8,0,0,
    0,122,105,112,105,116,101,109,0,8,0,0,0,122,105,112,115,99,97,110,0,8,0,
    0,0,90,105,112,79,112,101,110,0,9,0,0,0,90,105,112,70,101,116,99,104,0,8,
    0,0,0,90,105,112,66,111,111,116,0,11,0,0,0,108,117,120,108,105,98,118,101,
    114,115,0,9,0,0,0,95,86,69,82,83,73,79,78,0,13,0,0,0,32,45,32,108,117,120,
    108,105,98,32,48,46,0,3,0,0,0,44,32,0,0,0,0,0,7,0,0,0,8,0,0,0,61,40,110,
    111,110,101,41,0,7,0,0,0,1,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,7,0,0,
    0,115,116,114,108,101,110,0,8,0,0,0,115,116,114,98,121,116,101,0,0,0,0,0,
    0,0,0,0,20,0,0,0,198,255,255,127,12,0,0,0,11,0,0,0,66,0,1,0,6,0,0,128,134,
    255,255,127,108,2,0,128,75,0,0,0,198,63,0,128,26,0,0,0,76,0,0,0,11,0,0,0,
    139,0,0,0,66,0,3,0,23,0,0,0,82,0,0,0,109,253,255,127,75,0,0,0,129,0,0,0,
    0,0,0,0,8,0,0,0,61,40,110,111,110,101,41,0,13,0,0,0,1,0,0,0,1,16,0,0,0,0,
    0,0,0,0,0,0,0,5,0,0,0,5,0,0,0,103,101,116,110,0,8,0,0,0,116,105,110,115,
    101,114,116,0,4,0,0,0,108,117,120,0,6,0,0,0,108,101,73,110,116,0,7,0,0,0,
    115,116,114,115,117,98,0,0,0,0,0,0,0,0,0,32,0,0,0,6,0,0,128,17,0,0,0,6,0,
    0,128,12,0,0,0,75,0,0,0,66,128,2,0,6,0,0,128,44,5,0,128,76,0,0,0,203,0,0,
    0,140,0,0,0,206,0,0,0,12,1,0,0,11,0,0,0,139,0,0,0,139,0,0,0,75,0,0,0,15,
    1,0,0,23,0,0,0,152,255,255,127,194,63,5,0,194,191,4,0,2,128,3,0,139,0,0,
    0,75,0,0,0,15,1,0,0,23,0,0,0,146,0,0,0,173,250,255,127,203,0,0,0,1,1,0,0,
    0,0,0,0,8,0,0,0,61,40,110,111,110,101,41,0,22,0,0,0,2,0,0,0,0,21,0,0,0,0,
    0,0,0,0,0,0,0,9,0,0,0,4,0,0,0,108,117,120,0,10,0,0,0,108,101,83,116,114,
    67,117,116,115,0,6,0,0,0,109,109,115,117,98,0,4,0,0,0,99,115,122,0,3,0,0,
    0,115,122,0,4,0,0,0,105,110,111,0,5,0,0,0,110,97,109,101,0,4,0,0,0,111,102,
    102,0,4,0,0,0,100,97,116,0,0,0,0,0,0,0,0,0,93,0,0,0,12,0,0,0,78,0,0,0,140,
    0,0,0,11,0,0,0,75,0,0,0,75,0,0,0,24,11,0,128,66,128,1,0,198,0,0,128,70,0,
    0,128,70,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,198,0,0,128,
    198,0,0,128,198,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,70,0,
    0,128,198,0,0,128,198,0,0,128,66,0,1,0,209,0,0,0,199,0,0,0,139,0,0,0,6,2,
    0,128,13,0,0,0,7,1,0,0,139,0,0,0,70,2,0,128,13,0,0,0,71,1,0,0,139,0,0,0,
    6,4,0,128,13,0,0,0,214,0,0,0,203,0,0,0,135,1,0,0,140,0,0,0,11,0,0,0,75,0,
    0,0,88,11,0,128,75,0,0,0,24,11,0,128,139,0,0,0,134,2,0,128,13,0,0,0,23,0,
    0,0,66,0,3,0,212,128,1,0,203,0,0,0,199,1,0,0,75,0,0,0,88,11,0,128,139,0,
    0,0,134,2,0,128,13,0,0,0,23,0,0,0,139,0,0,0,198,2,0,128,13,0,0,0,23,0,0,
    0,139,0,0,0,6,3,0,128,13,0,0,0,23,0,0,0,212,128,1,0,203,0,0,0,7,2,0,0,203,
    0,0,0,78,1,0,0,88,11,0,128,139,0,0,0,134,2,0,128,13,0,0,0,23,0,0,0,139,0,
    0,0,198,2,0,128,13,0,0,0,23,0,0,0,139,0,0,0,6,3,0,128,13,0,0,0,23,0,0,0,
    216,253,255,127,212,128,1,0,203,0,0,0,1,1,0,0,0,0,0,0,8,0,0,0,61,40,110,
    111,110,101,41,0,32,0,0,0,2,0,0,0,0,15,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,7,0,
    0,0,109,109,105,110,102,111,0,4,0,0,0,108,117,120,0,10,0,0,0,108,101,83,
    116,114,67,117,116,115,0,6,0,0,0,109,109,115,117,98,0,8,0,0,0,122,105,112,
    105,116,101,109,0,5,0,0,0,110,97,109,101,0,4,0,0,0,111,102,102,0,1,0,0,0,
    0,0,0,64,45,21,152,65,0,0,0,0,72,0,0,0,12,0,0,0,11,0,0,0,130,0,1,0,75,0,
    0,0,102,0,0,128,203,0,0,0,82,0,0,0,75,0,0,0,70,5,0,128,37,0,0,128,1,1,0,
    0,76,0,0,0,142,0,0,0,204,0,0,0,11,0,0,0,75,0,0,0,152,250,255,127,75,0,0,
    0,66,128,2,0,198,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,70,0,0,128,198,
    0,0,128,198,0,0,128,70,0,0,128,66,0,2,0,11,1,0,0,6,0,0,128,13,0,0,0,8,0,
    0,0,33,0,0,128,65,1,0,0,75,0,0,0,152,250,255,127,11,1,0,0,70,1,0,128,13,
    0,0,0,25,0,0,0,75,1,0,0,11,1,0,0,134,1,0,128,13,0,0,0,25,0,0,0,17,0,0,0,
    6,0,0,128,11,1,0,0,198,0,0,128,13,0,0,0,6,0,0,128,172,3,0,128,76,0,0,0,14,
    1,0,0,11,0,0,0,75,1,0,0,66,128,5,0,203,1,0,0,203,2,0,0,78,1,0,0,75,1,0,0,
    212,128,1,0,203,2,0,0,142,1,0,0,82,1,0,0,69,0,0,0,45,252,255,127,203,1,0,
    0,139,1,0,0,152,255,255,127,1,2,0,0,0,0,0,0,8,0,0,0,61,40,110,111,110,101,
    41,0,50,0,0,0,1,0,0,0,0,11,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,7,0,0,0,109,109,
    102,105,108,101,0,4,0,0,0,108,117,120,0,8,0,0,0,122,105,112,115,99,97,110,
    0,4,0,0,0,109,97,112,0,4,0,0,0,116,111,99,0,5,0,0,0,98,97,115,101,0,0,0,
    0,0,0,0,0,0,19,0,0,0,12,0,0,0,11,0,0,0,66,128,0,0,76,0,0,0,142,0,0,0,75,
    0,0,0,130,0,1,0,139,0,0,0,39,2,0,128,209,0,0,0,199,0,0,0,75,0,0,0,7,1,0,
    0,139,0,0,0,71,1,0,0,203,0,0,0,214,0,0,0,1,1,0,0,0,0,0,0,8,0,0,0,61,40,110,
    111,110,101,41,0,56,0,0,0,2,0,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,11,0,0,0,4,
    0,0,0,116,111,99,0,4,0,0,0,108,117,120,0,8,0,0,0,122,105,112,105,116,101,
    109,0,4,0,0,0,109,97,112,0,6,0,0,0,109,109,115,117,98,0,5,0,0,0,98,97,115,
    101,0,4,0,0,0,100,97,116,0,4,0,0,0,99,115,122,0,3,0,0,0,115,122,0,8,0,0,
    0,122,100,101,99,111,109,112,0,6,0,0,0,109,109,115,116,114,0,0,0,0,0,0,0,
    0,0,50,0,0,0,11,0,0,0,14,0,0,0,79,0,0,0,38,0,0,128,129,0,0,0,76,0,0,0,142,
    0,0,0,11,0,0,0,206,0,0,0,11,0,0,0,14,0,0,0,79,0,0,0,66,0,1,0,12,1,0,0,11,
    0,0,0,206,0,0,0,11,0,0,0,78,1,0,0,139,0,0,0,142,1,0,0,23,0,0,0,24,0,0,128,
    11,0,0,0,78,1,0,0,139,0,0,0,142,1,0,0,23,0,0,0,139,0,0,0,206,1,0,0,23,0,
    0,0,66,128,1,0,139,0,0,0,206,1,0,0,139,0,0,0,14,2,0,0,161,2,0,128,12,1,0,
    0,76,2,0,0,140,2,0,0,203,0,0,0,66,0,3,0,134,255,255,127,139,0,0,0,14,2,0,
    0,194,191,2,0,66,0,2,0,210,0,0,0,203,0,0,0,1,1,0,0,0,0,0,0,8,0,0,0,61,40,
    110,111,110,101,41,0,65,0,0,0,1,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,
    4,0,0,0,108,117,120,0,4,0,0,0,122,105,112,0,8,0,0,0,90,105,112,79,112,101,
    110,0,9,0,0,0,90,105,112,70,101,116,99,104,0,9,0,0,0,98,111,111,116,46,108,
    117,120,0,9,0,0,0,100,111,115,116,114,105,110,103,0,10,0,0,0,47,98,111,111,
    116,46,108,117,120,0,0,0,0,0,0,0,0,0,26,0,0,0,12,0,0,0,71,0,0,0,12,0,0,0,
    142,0,0,0,11,0,0,0,66,128,1,0,212,128,1,0,12,0,0,0,78,0,0,0,167,3,0,128,
    12,0,0,0,206,0,0,0,12,0,0,0,78,0,0,0,7,1,0,0,66,128,0,0,75,0,0,0,103,1,0,
    128,76,1,0,0,75,0,0,0,11,0,0,0,135,1,0,0,157,0,0,0,131,0,1,0,69,0,0,0,0,
    0,0,0,43,0,0,0,17,0,0,0,19,0,0,0,12,0,0,0,71,0,0,0,48,0,0,0,212,128,1,0,
    12,0,0,0,135,0,0,0,48,128,0,0,212,128,1,0,12,0,0,0,199,0,0,0,48,0,1,0,212,
    128,1,0,12,0,0,0,7,1,0,0,48,128,1,0,212,128,1,0,12,0,0,0,71,1,0,0,48,0,2,
    0,212,128,1,0,12,0,0,0,135,1,0,0,48,128,2,0,212,128,1,0,12,0,0,0,199,1,0,
    0,48,0,3,0,212,128,1,0,12,2,0,0,103,2,0,128,12,2,0,0,130,0,0,0,76,2,0,0,
    135,2,0,0,75,0,0,0,199,2,0,0,11,0,0,0,93,1,0,0,83,2,0,0,133,0,0,0,0,0,0,
    0, };
  lua_dobuffer(L,(const char*)B1,2448,"luac");
} /* end of embedded code */

/* resumed: mluxsys.c */
  return L;
}
