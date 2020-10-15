/* lux.c - generated from mlux.c by onesrc
 * paths: boot.c
 * Wed Feb 21 21:39:37 PST 2001
 */

/* Standalone Lux, with some extension code tied in */

#include "luxsys.h"

#if defined(WIN32)

#define WINDOWS_MEAN_AND_LEAN
#include <windows.h>
#define pFindExecutable(a,b,c) (GetModuleFileName(NULL,b,c) ? b : a)

#elif defined(macintosh)

#define pFindExecutable(a,b,c) a

#else

#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

// adapted from TclpFindExecutable in "tcl8.4a2/generic/tclUnixFile.c"
static const char*
pFindExecutable(const char *argv0, char *buf, int len) {
  const char *p, *q;
  struct stat sb;
  if (argv0 == NULL || strlen(argv0) >= len)
    return "";
  if (strchr(argv0, '/') != NULL)
    return argv0;
  p = getenv("PATH");
  if (p == NULL)
    p = ":/bin:/usr/bin";
  else if (*p == 0)
    p = "./";
  for (;;) {
    while (isspace(*p))
      p++;
    q = p;
    while (*p != ':' && *p != 0)
      p++;
    if (p - q + strlen(argv0) + 2 >= len)
      return argv0;
    strncpy(buf, q, p - q);
    buf[p-q] = 0;
    if (p != q && p[-1] != '/')
      strcat(buf, "/");
    strcat(buf, argv0);
    if (access(buf, X_OK) == 0 && stat(buf, &sb) == 0 && S_ISREG(sb.st_mode))
      return buf;
    if (*p == '\0')
      return argv0;
    if (*++p == 0)
      p = "./";
  }
}

#endif

int main(int argc, char *argv[])
{
  int i;
  lua_State *L = luxsys_open();
  {
    char path[500];
    lua_pushstring(L, pFindExecutable(argv[0], path, sizeof path));
  }
  lua_setglobal(L, "argv0");
  lua_newtable(L);
  for (i = 1; i < argc; ++i) {
    lua_pushnumber(L, i);
    lua_pushstring(L, argv[i]);
    lua_settable(L, -3);
  }
  lua_setglobal(L, "argv");
/* include: boot.c */

{ /* begin embedded code */
  static unsigned char B1[] = { /* run */ 27,76,117,97,64,1,4,4,4,32,6,9,8,18,
    230,91,161,176,185,178,65,8,0,0,0,61,40,110,111,110,101,41,0,0,0,0,0,0,0,
    0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,4,0,0,0,108,117,120,0,8,0,0,0,90,105,
    112,66,111,111,116,0,6,0,0,0,97,114,103,118,48,0,5,0,0,0,97,114,103,118,
    0,6,0,0,0,97,114,103,118,49,0,8,0,0,0,116,114,101,109,111,118,101,0,7,0,
    0,0,100,111,102,105,108,101,0,6,0,0,0,112,114,105,110,116,0,9,0,0,0,95,86,
    69,82,83,73,79,78,0,0,0,0,0,0,0,0,0,29,0,0,0,12,0,0,0,78,0,0,0,140,0,0,0,
    66,0,0,0,166,5,0,128,204,0,0,0,103,4,0,128,204,0,0,0,6,0,0,128,13,0,0,0,
    103,3,0,128,76,1,0,0,204,0,0,0,6,0,0,128,66,0,0,0,19,1,0,0,12,0,0,0,78,0,
    0,0,12,1,0,0,66,0,0,0,166,1,0,128,140,1,0,0,12,1,0,0,2,0,0,0,170,0,0,128,
    204,1,0,0,12,2,0,0,2,0,0,0,0,0,0,0, };
  lua_dobuffer(L,(const char*)B1,281,"run");
} /* end of embedded code */

/* resumed: mlux.c */
  lua_close(L);
  return 0;
}
