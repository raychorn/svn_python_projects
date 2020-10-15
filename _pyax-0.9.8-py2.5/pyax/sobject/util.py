"""
Various utility functions specific to Salesforce.com/Apex
"""
import pprint
import types
import string

from pyax.baseconvert import *

def uniq_id_list(id_list):
    """
    Takes a list of SObject IDs, ensure they are all id18 (in case they are 
    mixed) and cull any duplicates while retaining the order
    """
    unique_id_list = []
    for candidate_id in id_list:
        candidate_id = id_15_to_18(candidate_id)
        if candidate_id not in unique_id_list:
            unique_id_list.append(candidate_id)
            pass
        continue
    return unique_id_list
## END uniqIdList
    

def id_18_to_15(id_18):
    """
    Truncate an 18 char sObject ID to the case-sensitive 15 char variety.
    """
    if not isinstance(id_18, str):
        raise TypeError("Expected StringType, got %s" %type(id_18))
    return id_18[:15]
## END is18to15

def id_15_to_18(id_15):
    """
    Translate a 15 char sObject ID to the case-insensitive 18-char variety.
    """
    chunkSize = 5
    caseSafeExt = ''
    if not isinstance(id_15, str):
        raise TypeError("Expected StringType, got %s" %type(id_15))

    if len(id_15) != 15:
        if len(id_15) == 18:
            return id_15
        id_15 = id_15[:15]
        
    idStr = id_15
    while len(idStr) > 0:
        chunk = idStr[:chunkSize]
        idStr = idStr[chunkSize:]
        caseSafeExt += _convert_chunk(chunk)

    return "%s%s" %(id_15, caseSafeExt)
## END convertId15ToId18


def _convert_chunk(chunk):
    """
    Used by convertId15ToId18. Not much use otherwise.
    """
    TRANSLATION_TABLE = string.ascii_uppercase + string.digits[:6]

    chunk_bin_list = []

    # for each character in chunk, give that position a 1 if uppercase,
    # 0 otherwise (lowercase or number)
    for character in chunk:
        if character in string.ascii_uppercase:
            chunk_bin_list.append('1')
        else:
            chunk_bin_list.append('0')

    chunk_bin_list.reverse() # flip it around so rightmost bit is most significant
    chunk_bin = "".join(chunk_bin_list) # compress list into a string of the binary num
    chunk_char_idx = baseconvert(chunk_bin, BINARY, DECIMAL) # convert binary to decimal
    return TRANSLATION_TABLE[int(chunk_char_idx)] # look it up in our table
## END convertChunk

