/* Lux as a Tcl extension */

#include "luxsys.h"
#define USE_TCL_STUBS 1
#include <tcl.h>

/* TODO: get rid of static ints, use closures instead */
static int tcluxtag;

static int
TcluxCallback(lua_State *L) {
  Tcl_Obj *list = lua_touserdata(L, -2);
  Tcl_Interp* ip = lua_touserdata(L, -1);
  int i, n = lua_gettop(L) - 2, refs = 0, refvec[10];
  if (list == NULL || lua_tag(L, -2) != tcluxtag || ip == NULL)
    lua_error(L, "TcluxCallback not called with proper args");
  list = Tcl_DuplicateObj(list);
  Tcl_IncrRefCount(list);
  for (i = 1; i <= n; ++i) {
    Tcl_Obj* elem;
    if (lua_isnil(L, i)) {
      elem = Tcl_NewObj();
    } else if (lua_isnumber(L, i)) {
      double d = lua_tonumber(L, i);
      long l = (long) d;
      elem = l == d ? Tcl_NewLongObj(l) : Tcl_NewDoubleObj(d);
    } else if (lua_isstring(L, i)) {
      int len = lua_strlen(L, i);
      const char* ptr = lua_tostring(L, i);
      elem = Tcl_NewByteArrayObj((unsigned char*) ptr, len);
    } else {
      lua_pushvalue(L, i);
      refvec[refs] = lua_ref(L, 0);
      elem = Tcl_NewIntObj(refvec[refs++]);
    }
    Tcl_ListObjAppendElement(ip, list, elem);
  }
  i = Tcl_EvalObjEx(ip, list, TCL_EVAL_DIRECT);
  while (--refs >= 0)
    lua_unref(L, refvec[refs]);
  Tcl_DecrRefCount(list);
  if (i != TCL_OK)
    lua_error(L, Tcl_GetStringResult(ip));
  return 0;
}

static int
TcluxCmd(ClientData cd_, Tcl_Interp* ip_, int oc_, Tcl_Obj*CONST ov_[]) {
  int v, i, len;
  char *ptr, *fmt;
  double d;
  lua_State *L = (void*) cd_;
  if (oc_ < 2) {
    Tcl_WrongNumArgs(ip_, oc_, ov_, "fmt ?args ...?");
    return TCL_ERROR;
  }
  fmt = Tcl_GetStringFromObj(ov_[1], &len);
  if (oc_ != 2 + len) {
    Tcl_SetResult(ip_, "arg count mismatch", TCL_STATIC);
    return TCL_ERROR;
  }
  for (i = 2; *fmt; ++i)
    switch (*fmt++) {
      case 'i':
	if (Tcl_GetIntFromObj(ip_, ov_[i], &v) != TCL_OK)
	  return TCL_ERROR;
	lua_pushnumber(L, v);
	break;
      case 'd':
	if (Tcl_GetDoubleFromObj(ip_, ov_[i], &d) != TCL_OK)
	  return TCL_ERROR;
	lua_pushnumber(L, d);
	break;
      case 'r':
	if (Tcl_GetIntFromObj(ip_, ov_[i], &v) != TCL_OK)
	  return TCL_ERROR;
	if (lua_getref(L, v) == 0)
	  lua_pushnil(L);
	break;
      case 'b':
	ptr = (void*) Tcl_GetByteArrayFromObj(ov_[i], &len);
	lua_pushlstring(L, ptr, len);
	break;
      case 's':
	ptr = Tcl_GetStringFromObj(ov_[i], &len);
	lua_pushlstring(L, ptr, len);
	break;
      case 'g':
	ptr = Tcl_GetStringFromObj(ov_[i], NULL);
	lua_getglobal(L, ptr);
	break;
      case 'p':
	lua_pushuserdata(L, ov_[i]);
	break;
      case 'c':
	if (Tcl_ListObjLength(ip_, ov_[i], &v) != TCL_OK)
	  return TCL_ERROR;
	lua_pushusertag(L, ov_[i], tcluxtag);
	lua_pushuserdata(L, ip_);
	lua_pushcclosure(L, TcluxCallback, 2);
	Tcl_IncrRefCount(ov_[i]);
	break;
      default:
	Tcl_SetResult(ip_, "unknown format specifier", TCL_STATIC);
	return TCL_ERROR;
    }
  v = lua_call(L, oc_ - 3, 0);
  if (v != 0) {
    Tcl_SetObjResult(ip_, Tcl_NewIntObj(v));
    return TCL_ERROR;
  }
  return TCL_OK;
}

static void
TcluxDelProc(ClientData cd_) {
  lua_close((void*) cd_);
}

static int
TcluxDecref(lua_State *L) {
  Tcl_Obj *p = lua_touserdata(L, -1);
  if (p == NULL || lua_tag(L, -1) != tcluxtag)
    lua_error(L, "bad call to TcluxDecref");
  Tcl_DecrRefCount(p);
  return 0;
}

DLLEXPORT int
Tclux_Init(Tcl_Interp* ip_) {
  lua_State *L;
#ifdef Tcl_CreateCommand
  if (!Tcl_InitStubs(ip_, "8.1", 0)) return TCL_ERROR;
#endif
  L = luxsys_open();
  if (L == NULL) return TCL_ERROR;
  tcluxtag = lua_newtag(L);
  lua_pushcfunction(L, TcluxDecref);
  lua_settagmethod(L, tcluxtag, "gc");
  Tcl_CreateObjCommand(ip_, "tclux", TcluxCmd, (void*) L, TcluxDelProc);
  return Tcl_PkgProvide(ip_, "tclux", "0.1");
}
