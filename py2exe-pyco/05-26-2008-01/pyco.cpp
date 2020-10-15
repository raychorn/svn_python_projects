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

// pyco (pronounced like 'pico') is a tiny self-extracting Python
// interpreter.

// changes by cliechti@gmx.net
// - chdir to tempdir before cleaning up (important when client app changes
//   the dir...)
// - execute the module and not a specific function
// - _pyco_loader.py is executed
// - Py_NoSiteFlag is set to prevent "import site"
// - include of python.h is not needed, time.h instead

#include "inflate.h"
#include <stdlib.h>
#include <process.h>
#include <time.h>
#include <direct.h>

#define X(s) \
{ \
    char buff[5000]; \
    sprintf(buff, "%s (%d)", s, __LINE__); \
    MessageBox(NULL, buff, "Hey", MB_OK); \
}

/*
Note: Functions return bOk.

File format = last 4 bytes of file tell offset of first stored file entry

by convention, first entry in the TOC is the program that will be launched.
*/

// Copies ulSize bytes from pInF to pOutF, returns number read
unsigned long Copy(FILE *pInF, unsigned long ulSize, FILE * pOutF)
{
    bool bOk = true;
    const int BUFF_SIZE = 16384;
    char acBuff[BUFF_SIZE + 1];
    unsigned long ulTotalCopied = 0;
    while (ulSize)
    {
        size_t tNumRead = fread(acBuff, 1, MIN(ulSize, BUFF_SIZE), pInF);
        ASSERT(tNumRead > 0, "No records read during Copy");
        ulSize -= tNumRead;
        size_t tNumWritten = fwrite(acBuff, 1, tNumRead, pOutF);
        ASSERT(tNumWritten == tNumRead, "No data written during Copy");
        ulTotalCopied += tNumWritten;
    }

Error:
    if (!bOk)
        ulTotalCopied = 0;
    return ulTotalCopied;
}

typedef struct TOC_ENTRY
{
    unsigned uCompressedSize;
    unsigned uFullSize;
    unsigned char ucNameLen;
    unsigned char ucIsCompressed;
    char * pcName;
    TOC_ENTRY * pNext;
} TOC_ENTRY;

// Reads the TOC from a given file, returns pointer to a list of TOC_ENTRIES
// (returns the list in reverse order. Deal with it.)
bool ReadTOC(char * pcFileName, TOC_ENTRY **ppEntries)
{
    bool bOk = true;
    unsigned uOffset = 0;
    FILE * fIn;
    ASSERT(ppEntries != NULL, "Empty TOC");
    *ppEntries = NULL;

    // Move to near the end and read the total TOC size
    fIn = fopen(pcFileName, "rb");
    ASSERT(fIn != NULL, "Failed to open archive for reading");
    ASSERT(fseek(fIn, -4, SEEK_END) == 0, "Seek to end of archive failed");
    ASSERT(fread(&uOffset, sizeof(unsigned), 1, fIn) == 1, "Read first offset failed");
    ASSERT(fseek(fIn, uOffset, SEEK_SET) == 0, "Seek to first offset failed");

    // Read and extract the files
    while (1)
    {
        TOC_ENTRY * pEntry = (TOC_ENTRY *)malloc(sizeof(TOC_ENTRY));
        ASSERT(pEntry != NULL, "Failed to allocate memory for new entry");

        // Read the parts
        if (fread(&(pEntry->uCompressedSize), sizeof(unsigned), 1, fIn) != 1 ||
            fread(&(pEntry->uFullSize), sizeof(unsigned), 1, fIn) != 1 ||
            fread(&(pEntry->ucNameLen), 1, 1, fIn) != 1 ||
            fread(&(pEntry->ucIsCompressed), 1, 1, fIn) != 1)
        {
            // All done
            free(pEntry);
            break;
        }
        
        // Read in the name
        pEntry->pcName = (char *)malloc(pEntry->ucNameLen + 1);
        ASSERT(pEntry->pcName != NULL, "Failed to alloc mem for entry name");
        ASSERT(fread(pEntry->pcName, pEntry->ucNameLen, 1, fIn) == 1, "Read name failed");
        pEntry->pcName[pEntry->ucNameLen] = '\0';

        // Read, decompress, and save this file
        FILE * fOut = fopen(pEntry->pcName, "wb");
        ASSERT(fOut != NULL, "Failed to create output file");
        unsigned uFullSize;
        if (pEntry->ucIsCompressed) {
            uFullSize = Inflate(fIn, pEntry->uCompressedSize, fOut);
        } else {
            uFullSize = Copy(fIn, pEntry->uFullSize, fOut);
        }
        fclose(fOut);
        ASSERT(uFullSize == pEntry->uFullSize, "Size mismatch in expanded file");

        // Save this entry
        pEntry->pNext = *ppEntries;
        *ppEntries = pEntry;
    }

Error:
    return bOk;
}

// Frees the memory used by a TOC list
bool FreeTOC(TOC_ENTRY *pEntries)
{
    while (pEntries != NULL)
    {
        TOC_ENTRY * pNext = pEntries->pNext;
        if (pEntries->pcName != NULL)
            free(pEntries->pcName);
        free(pEntries);
        pEntries = pNext;
    }

    return true;
}

// Returns true if pcString ends with pcSuffix (case-insensitive)
bool EndsWith(char *pcString, char *pcSuffix)
{
    int iSuffLen = strlen(pcSuffix);
    return strnicmp(pcString + strlen(pcString) - iSuffLen, pcSuffix, iSuffLen) == 0;
}

char acGlobalTempDir[_MAX_PATH + 1]; // the system-wide temp dir
char acTempDir[_MAX_PATH + 1]; // our own temp dir inside the global temp dir
char acCurdir[_MAX_PATH + 1]; // current dir at the time of starting
char pycostartdir[_MAX_PATH + 12]; // current dir at the time of starting

// Changes the current working directory to a new temp directory
void Fatal(char *msg)
{
    bool bOk = false;
    ASSERT(0, msg);
Error:
    exit(1);
}

void MoveToTempDir()
{
    // Find the global temp directory
    if (!GetTempPath(_MAX_PATH, acGlobalTempDir))
        Fatal("Failed to find temporary directory - check TMP / TEMP env variables");

    // Get a unique name in the dir
    srand((unsigned)time(NULL));
    char buff[2048];
    sprintf(buff, "xl%d", rand());
    if (!GetTempFileName(acGlobalTempDir, buff, 0, acTempDir))
        Fatal("Failed to create temp directory name - check TMP / TEMP env variables");

    // Create our own temp directory
    // Windows creates the file in GetTempFileName if the 3rd param is 0. If it's not
    // 0, then Windows doesn't verify that the file doesn't already exist. So delete
    // the file and quickly create a directory having the same name. Does not 
    // guarantee lack of name collisions though, but using a pseudo-random prefix
    // for the file in the first place makes that likelihood effectively nil.
    DeleteFile(acTempDir);
    if (!CreateDirectory(acTempDir, NULL))
        Fatal("Failed to create temp directory - check TMP / TEMP env variables");

    // Move into that new directory
    if (!SetCurrentDirectory(acTempDir))
        Fatal("Failed to move to temp directory");
}

// Moves out of the temp directory and deletes it
void CleanUpTempDir()
{
    HANDLE hFind;
    WIN32_FIND_DATA zFindData;

    // Move into the temp directory again
    if (!SetCurrentDirectory(acTempDir))
        Fatal("Failed to move to temp directory");

    // Remove all files in this directory
    hFind = FindFirstFile(".\\*", &zFindData);
    if (hFind != INVALID_HANDLE_VALUE)
    {
        do {
            remove(zFindData.cFileName);
        } while (FindNextFile(hFind, &zFindData));
        FindClose(hFind);
    }

    // Move out of our temp directory
    SetCurrentDirectory(acGlobalTempDir);

    // Remove our temp directory
    RemoveDirectory(acTempDir);
}


typedef void (*VOIDFUNC)();
typedef int (*CHARFUNC)(char *);
typedef int (*INTCHARFUNC)(int, char *);
typedef int (*FILECHARINT)(FILE *, char *, int);
#ifdef _DEBUG
  #define PYDLL "python25_d.dll"
#else
  #define PYDLL "python25.dll"
#endif


int WINAPI WinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPSTR     lpCmdLine,
                     int       nCmdShow)
{
    bool bOk = true;
    int sts = 0;
    bool status;
    char acCmdLine[_MAX_PATH + 5]; // Need a little extra in case we append '.exe'
    HMODULE hDLL;
    TOC_ENTRY * pEntries = NULL;
    TOC_ENTRY * pCur;

    GetCurrentDirectory(sizeof acCurdir, acCurdir);
    
    // Figure out our own name
    ASSERT(GetModuleFileName(NULL, acCmdLine, _MAX_PATH), "GetModuleFileName failed");

    // A file X.exe can be called by just 'X'. :(
    if (!EndsWith(acCmdLine, ".exe"))
        strcat(acCmdLine, ".exe");


    MoveToTempDir();

    // Extract the files
    status = ReadTOC(acCmdLine, &pEntries);
    ASSERT(status, "Failed to read TOC");
    if (status)
    {
        HINSTANCE hDLL = LoadLibrary(PYDLL);
        ASSERT(hDLL, "Failed to find " PYDLL);
        
        // Run the main program
        int* Py_NoSiteFlag = (int*)GetProcAddress(hDLL, "Py_NoSiteFlag");
        *Py_NoSiteFlag = 1;
        VOIDFUNC Py_Initialize = (VOIDFUNC)GetProcAddress(hDLL, "Py_Initialize");
        ASSERT(Py_Initialize, "Failed to find Py_Initialize");
        VOIDFUNC Py_Finalize = (VOIDFUNC)GetProcAddress(hDLL, "Py_Finalize");
        ASSERT(Py_Finalize, "Failed to find Py_Finalize");
        CHARFUNC Py_SetProgramName = (CHARFUNC)GetProcAddress(hDLL, "Py_SetProgramName");
        ASSERT(Py_Initialize, "Failed to find Py_SetProgramName");
        INTCHARFUNC PySys_SetArgv = (INTCHARFUNC)GetProcAddress(hDLL, "PySys_SetArgv");
        ASSERT(Py_Initialize, "Failed to find PySys_SetArgv");
        FILECHARINT PyRun_AnyFileEx = (FILECHARINT)GetProcAddress(hDLL, "PyRun_AnyFileEx");
        ASSERT(Py_Initialize, "Failed to find PyRun_AnyFileEx");
        
        //set current dir in environment variable. the current directory was
        //changed to the temp dir and the embedded script needs to get back
        //to the current dir.
        sprintf(pycostartdir, "PYCOSTARTDIR=%s", acCurdir);
        putenv(pycostartdir);
        
        #define filename "_pyco_loader.py"
        FILE *fp;
        if ((fp = fopen(filename, "r")) == NULL) {
            fprintf(stderr, "%s: can't open file '%s': [Errno %d] %s\n",
                __argv[0], filename, errno, strerror(errno));
            ASSERT(fp, "Failed to open user script.");
            sts = 2;
        } else {
            //~ __argv[0] = acCmdLine;      //XXX writing to argv allowed?
            Py_SetProgramName(filename);
            Py_Initialize();
            PySys_SetArgv(__argc, (char*)__argv);
            sts = PyRun_AnyFileEx(fp, filename, 1) != 0;
            Py_Finalize();
        }
        
        FreeLibrary(hDLL);
    }

    // Clean up the result
    if (!SetCurrentDirectory(acTempDir)) {
        Fatal("Failed to cleanup temp directory");
    } else {
        pCur = pEntries;
        while (pCur != NULL)
        {
            // Unload the library first if needed
            if (EndsWith(pCur->pcName, ".pyd"))
            {
                hDLL = GetModuleHandle(pCur->pcName);
                if (hDLL != NULL)
                    FreeLibrary(hDLL);
            }
    
            remove(pCur->pcName);
            pCur = pCur->pNext;
        }
    }

    CleanUpTempDir();
    FreeTOC(pEntries);

Error:
    return (bOk) ? sts : 3;     // exit code: ok -> sts; ASSERT -> 3
}
