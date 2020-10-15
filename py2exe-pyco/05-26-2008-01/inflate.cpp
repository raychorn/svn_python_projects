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

#include "inflate.h"
#include "zlib.h"
#include <string.h>

// Inflates ulCompressSize bytes read from iInFD, writing them uncompressed to iOutFD.
// Returns 0 on error, else number of decompressed bytes written
const int BUFF_SIZE = 16384;
unsigned long Inflate(FILE *pInF, unsigned long ulCompressSize, FILE * pOutF)
{
    bool bOk = true;
    unsigned char acInBuffer[BUFF_SIZE+1];
    unsigned char acOutBuffer[BUFF_SIZE+1];
    unsigned long ulBytesWritten = 0;
    int iResult;
    z_stream zStream;
    memset(&zStream, 0, sizeof(z_stream));

    zStream.next_in = acInBuffer;
    zStream.next_out = acOutBuffer;
    zStream.avail_in = 0;
    zStream.avail_out = BUFF_SIZE;

    ASSERT(inflateInit(&zStream) == Z_OK, "inflateInit error");

    while (1)
    {
        bool bDidSomeWork = false;

        // See if we need to read some more data
        if (zStream.avail_in == 0 && ulCompressSize > 0)
        {
            bDidSomeWork = true;
            size_t tCount = fread(acInBuffer, 1, MIN(ulCompressSize, BUFF_SIZE), pInF);
            ASSERT(tCount > 0, "tCount after fread <= 0");
            zStream.avail_in = tCount;
            ulCompressSize -= tCount;
            zStream.next_in = acInBuffer;
        }

        // Decompress some
        iResult = inflate(&zStream, Z_SYNC_FLUSH);
        ASSERT(iResult == Z_OK || iResult == Z_STREAM_END, "Bad iResult from inflate");
        if (zStream.avail_out < BUFF_SIZE)
        {
            bDidSomeWork = true;

            // Have some data to write out
            size_t tAmnt = BUFF_SIZE - zStream.avail_out;
            size_t tCount = fwrite(acOutBuffer, 1, tAmnt, pOutF);
            ASSERT(tCount == tAmnt, "Mismatch in amount written");
            ulBytesWritten += tCount;
            zStream.avail_out = BUFF_SIZE;
            zStream.next_out = acOutBuffer;
        }

        if (iResult == Z_STREAM_END)
            break;        

        ASSERT(bDidSomeWork, "No work performed");
    }

    ASSERT(inflateEnd(&zStream) == Z_OK, "inflateEnd failed");

Error:
    return (bOk ? ulBytesWritten : 0);
}

/*
int main(int argc, char **argv)
{
    bool bOk = true;
    FILE * fIn;
    FILE * fOut;
    fIn = fopen("h:\\xlon\\zlib\\doc.z", "rb");
    fOut = fopen("h:\\xlon\\zlib\\doc.u2", "wb");
    ASSERT(fIn != NULL);
    ASSERT(fOut != NULL);
    printf ("Wrote %lu bytes\n", Inflate(fIn, 511187, fOut));

Error:
    return (bOk != true);
}
*/
