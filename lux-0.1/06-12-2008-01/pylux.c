/* Lux as a Python extension */

#include "luxsys.h"
#include <Python.h>

/* TODO: get rid of static data, use closures instead */
static int pyluxtag;
static lua_State *g_lux;
#define L g_lux

static int
PyluxCallback(lua_State *L) {
  PyObject *tuple, *result;
  PyObject* func = lua_touserdata(L, -1);
  int i, n = lua_gettop(L) - 1, refs = 0, refvec[10];
  if (func == NULL || !PyCallable_Check(func))
    lua_error(L, "PyluxCallback not called with proper args");
  tuple = PyTuple_New(n);
  if (tuple == NULL)
    lua_error(L, "cannot create tuple");
  for (i = 1; i <= n; ++i) {
    PyObject* elem;
    if (lua_isnil(L, i)) {
      elem = Py_None;
      Py_INCREF(elem);
    } else if (lua_isnumber(L, i)) {
      double d = lua_tonumber(L, i);
      long l = (long) d;
      elem = l == d ? PyInt_FromLong(l) : PyFloat_FromDouble(d);
    } else if (lua_isstring(L, i)) {
      elem = PyString_FromStringAndSize(lua_tostring(L, i),
					    lua_strlen(L, i));
    } else {
      lua_pushvalue(L, i);
      refvec[refs] = lua_ref(L, 0);
      elem = PyInt_FromLong(refvec[refs++]);
    }
    PyTuple_SET_ITEM(tuple, i - 1, elem);
  }
  result = PyObject_CallObject(func, tuple);
  while (--refs >= 0)
    lua_unref(L, refvec[refs]);
  Py_DECREF(tuple);
  if (result == 0)
    lua_error(L, "callback failed");
  Py_DECREF(result);
  return 0;
}

static PyObject*
Pylux_eval(PyObject *self, PyObject *args) {
  const char* s;
  int i, n = PyTuple_GET_SIZE(args);
  PyObject* o = PyTuple_GetItem(args, 0);

  if (n > 0 && (o == 0 || !PyString_Check(o))) {
    PyErr_BadArgument();
    return 0;
  }
  if (PyString_GET_SIZE(o) != n - 1) {
    PyErr_SetNone(PyExc_IndexError);
    return 0;
  }
  s = PyString_AS_STRING(o);
  for (i = 1; i < n; ++i) {
    PyObject* v = PyTuple_GetItem(args, i);
    switch (*s++)
    {
      /* case 'i': case 'd': case 's': */
      case 'v':
	if (PyInt_Check(v))
	  lua_pushnumber(L, PyInt_AS_LONG(v));
	else if (PyFloat_Check(v))
	  lua_pushnumber(L, PyFloat_AS_DOUBLE(v));
	else if (PyString_Check(v))
	  lua_pushlstring(L, PyString_AS_STRING(v),
	      			PyString_GET_SIZE(v));
	else {
	  PyErr_SetNone(PyExc_TypeError);
	  return 0;
	}
	break;
      case 'r':
	if (PyInt_Check(v)) {
	  if (lua_getref(L, PyInt_AS_LONG(v)))
	    lua_pushnil(L);
	} else {
	  PyErr_SetNone(PyExc_TypeError);
	  return 0;
	}
	break;
      case 'g':
	if (PyString_Check(v))
	  lua_getglobal(L, PyString_AS_STRING(v));
	else {
	  PyErr_SetNone(PyExc_TypeError);
	  return 0;
	}
	break;
      case 'p':
	lua_pushusertag(L, v, LUA_ANYTAG);
	break;
      case 'c':
	if (!PyCallable_Check(v)) {
	  PyErr_SetNone(PyExc_TypeError);
	  return 0;
	}
	lua_pushusertag(L, v, pyluxtag);
	lua_pushcclosure(L, PyluxCallback, 1);
	Py_INCREF(v);
	break;
      default:
	PyErr_BadArgument();
	return 0;
    }
  }
  i = lua_call(L, n - 2, 0);
  if (i != 0) {
    PyErr_SetNone(PyExc_RuntimeError);
    return 0;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static int
PyluxDecref(lua_State *L) {
  PyObject *p = lua_touserdata(L, -1);
  if (p == NULL || lua_tag(L, -1) != pyluxtag)
    lua_error(L, "bad call to PyluxDecref");
  Py_DECREF(p);
  return 0;
}

static PyMethodDef pylux_methods[] = {
  {"eval", Pylux_eval, METH_VARARGS},
  {0, 0, 0}
};

#ifdef WIN32
__declspec(dllexport)
#endif
void initpylux() {
  L = luxsys_open();
  pyluxtag = lua_newtag(L);
  lua_pushcfunction(L, PyluxDecref);
  lua_settagmethod(L, pyluxtag, "gc");
  Py_InitModule("pylux", pylux_methods);
}
