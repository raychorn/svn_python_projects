#ifndef INFLATE_H
#define INFLATE_H

/* ======================================================================
 Copyright 2001, 2002 by Solus Software

                         All Rights Reserved

 Permission to use, copy, modify, and distribute this software and
 its documentation for any purpose and without fee is hereby
 granted, provided that the above copyright notice appear in all
 copies and that both that copyright notice and this permission
 notice appear in supporting documentation.

 SOLUS SOFTWARE DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
 INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
 NO EVENT SHALL SOLUS SOFTWARE BE LIABLE FOR ANY SPECIAL, INDIRECT OR
 CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
 OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 ====================================================================== */

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include <stdio.h>
unsigned long Inflate(FILE *pInF, unsigned long ulCompressSize, FILE * pOutF);

#define MIN(a, b) ((a) > (b) ? (b) : (a))
#define ASSERT(EXPR, MSG) { \
  if (!(EXPR)) \
  { \
    char buffer[2000]; \
    sprintf(buffer, "Assertion failed in %s, line %d:\n%s", __FILE__, __LINE__, MSG);\
	MessageBox(NULL, buffer, "Failed", MB_OK | MB_ICONERROR);\
    bOk = false; goto Error; } \
  }

#endif //INFLATE_H
