/* Lux as a Ruby extension */

#include "luxsys.h"
#include <ruby.h>

static lua_State *g_lux; /*XXX static for now */

static VALUE cRubylux;

static VALUE
Rubylux_eval(VALUE obj, VALUE arg) {
  Check_Type(arg, T_STRING);
  lua_dobuffer(g_lux, RSTRING(arg)->ptr, RSTRING(arg)->len, NULL);
  return Qnil;
}

#ifdef WIN32
__declspec(dllexport)
#endif
void Init_rubylux() {
  cRubylux = rb_define_module("Rubylux");
  g_lux = luxsys_open();
  rb_define_module_function(cRubylux, "eval", Rubylux_eval, 1);
}
