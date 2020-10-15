/* Lux as a Perl extension */

#include "luxsys.h"
#define bool int
#include <EXTERN.h>
#include <perl.h>
#include <XSUB.h>

static lua_State *g_lux; /* XXX static for now */

XS(XS_perlux_eval) {
  dXSARGS;
  if (items != 1)
    croak("Usage: perlux::eval(string)");
  {
    STRLEN len;
    const char *ptr = SvPV(ST(0), len);
    lua_dobuffer(g_lux, ptr, len, NULL);
  }
  XSRETURN_EMPTY;
}

#ifdef WIN32
__declspec(dllexport)
#endif
XS(boot_perlux) {
  dXSARGS;
  char *file = __FILE__;
  XS_VERSION_BOOTCHECK;
  (void) items; /* unused */
  g_lux = luxsys_open();
  newXS("perlux::eval", XS_perlux_eval, file);
  XSRETURN_YES;
}
