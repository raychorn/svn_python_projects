'''
Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.


Defines a class for reading a dBase3 file format.

The format was defined by the following:

    dBASE III Database File Structure  (see attribution at end)

    The structure of a dBASE III database file is composed of a
    header and data records.  The layout is given below.
    dBASE III DATABASE FILE HEADER:
    +---------+-------------------+---------------------------------+
    |  BYTE   |     CONTENTS      |          MEANING                |
    +---------+-------------------+---------------------------------+
    |  0      |  1 byte           | dBASE III version number        |
    |         |                   |  (03H without a .DBT file)      |
    |         |                   |  (83H with a .DBT file)         |
    +---------+-------------------+---------------------------------+
    |  1-3    |  3 bytes          | date of last update             |
    |         |                   |  (YY MM DD) in binary format    |
    +---------+-------------------+---------------------------------+
    |  4-7    |  32 bit number    | number of records in data file  |
    +---------+-------------------+---------------------------------+
    |  8-9    |  16 bit number    | length of header structure      |
    +---------+-------------------+---------------------------------+
    |  10-11  |  16 bit number    | length of the record            |
    +---------+-------------------+---------------------------------+
    |  12-31  |  20 bytes         | reserved bytes (version 1.00)   |
    +---------+-------------------+---------------------------------+
    |  32-n   |  32 bytes each    | field descriptor array          |
    |         |                   |  (see below)                    | --+
    +---------+-------------------+---------------------------------+   |
    |  n+1    |  1 byte           | 0DH as the field terminator     |   |
    +---------+-------------------+---------------------------------+   |
                                                                        |
                                                                        |
    A FIELD DESCRIPTOR:      <------------------------------------------+
    +---------+-------------------+---------------------------------+
    |  BYTE   |     CONTENTS      |          MEANING                |
    +---------+-------------------+---------------------------------+
    |  0-10   |  11 bytes         | field name in ASCII zero-filled |
    +---------+-------------------+---------------------------------+
    |  11     |  1 byte           | field type in ASCII             |
    |         |                   |  (C N L D or M)                 |
    +---------+-------------------+---------------------------------+
    |  12-15  |  32 bit number    | field data address              |
    |         |                   |  (address is set in memory)     |
    +---------+-------------------+---------------------------------+
    |  16     |  1 byte           | field length in binary          |
    +---------+-------------------+---------------------------------+
    |  17     |  1 byte           | field decimal count in binary   |
    +---------+-------------------+--------------------------------
    |  18-31  |  14 bytes         | reserved bytes (version 1.00)   |
    +---------+-------------------+---------------------------------+

    The data records are layed out as follows:

    1. Data records are preceeded by one byte that is a space (20H) if 
       the record is not deleted and an asterisk (2AH) if it is deleted.
    2. Data fields are packed into records with no field separators or record 
       terminators.
    3. Data types are stored in ASCII format as follows:

    DATA TYPE      DATA RECORD STORAGE
    ---------      --------------------------------------------
    Character      (ASCII characters)
    Numeric        - . 0 1 2 3 4 5 6 7 8 9
    Logical        ? Y y N n T t F f  (? when not initialized)
    Memo           (10 digits representing a .DBT block number)
    Date           (8 digits in YYYYMMDD format, such as 19840704 for 
                   July 4, 1984)

    This information came directly from the Ashton-Tate Forum.  It can
    also be found in the Advanced Programmer's Guide available from
    Ashton-Tate.

    One slight difference occurs between files created by dBASE III and
    those created by dBASE III Plus.  In the earlier files, there is an
    ASCII NUL character between the $0D end of header indicator and the
    start of the data.  This NUL is no longer present in Plus, making a
    Plus header one byte smaller than an identically structured III file.

    Taken from the Pascal routines from DBF.PAS version 1.3
    Copyright (C) 1986 By James Troutman
    CompuServe PPN 74746,1567
    Permission is granted to use these routines for non-commercial purposes.
'''
__version__ = "$Id: dbase3.py,v 1.3 2002/08/21 12:41:48 donp Exp $"

def Build32BitInteger(four_byte_string):
    '''This unpacks a string into a 32 bit integer.  It is little endian,
    specifically for the PC environment.
    '''
    if len(four_byte_string) != 4:
        raise "Bad data", "String not 4 bytes long"
    s0 = ord(four_byte_string[0])
    s1 = ord(four_byte_string[1])
    s2 = ord(four_byte_string[2])
    s3 = ord(four_byte_string[3])
    return (s3 << 24) | (s2 << 16) | (s1 << 8) | s0

def StripNulls(str):
    '''Truncates a string at the first trailing null.  Returns the 
    truncated string.
    '''
    if len(str) < 1: return str
    first_null = -1
    for ix in xrange(len(str)):
        if ord(str[ix]) == 0:
            first_null = ix
            break
    if first_null == -1:
        return str
    else:
        return str[0:first_null]

class dBase3:
    '''Class to read a dBase3 file.  Note that this class is only 
    intended to read in the header info and give you enough functionality
    to iterate through the fields and interpret them.  You'll have to
    write a derived class if you want to write back to the dBase file.
    '''
    def __init__(self, file_name):
        '''We are passed the file name, so we open it.  Then we'll read the
        first 20 bytes of the header and get the basic data (see the
        dBase3 description above).  Then we get the whole header once we
        know the size of it.  Then we read in and parse the field 
        information.
        '''
        import string
        self.file_name = file_name
        try:
            self.fp = open(file_name, "rb")
        except:
            raise "Bad data", "Couldn't open \"%s\"" % file_name
        self.header = self.fp.read(20)  # Read the header
        if not self.header:
            raise "Bad data", "File is empty"
        if len(self.header) != 20:
            raise "Bad data", "Missing first 20 bytes in file header"
        self.version_number = ord(self.header[0])
        self.last_update_yy = ord(self.header[1])
        self.last_update_mm = ord(self.header[2])
        self.last_update_dd = ord(self.header[3])
        self.num_records    = Build32BitInteger(self.header[4:8])
        self.header_length  = (ord(self.header[9]) << 8) |                                ord(self.header[8])
        self.record_length  = (ord(self.header[11]) << 8) |                                ord(self.header[10])
        # Now go back and read the whole header including the field specs
        self.fp.seek(0)
        self.header = self.fp.read(self.header_length)
        self.reserved_bytes = self.header[12:32]
        # Calculate how many field descriptors we must have
        self.num_fields     = (self.header_length - 33)/32
        # Now read in the field information
        self.fields = []
        for ix in range(self.num_fields):
            start = 32 + ix*32
            stop  = start + 32 + 1
            field_data = self.header[start : stop]
            field = []
            # Get field name
            str = string.strip(StripNulls(field_data[0:11]))
            field.append(str)
            # Get field type character
            field.append(field_data[11])
            # Get field data address
            field.append(StripNulls(field_data[12:16]))
            # Get field length
            field.append(ord(field_data[16]))
            # Get field decimal count
            field.append(ord(field_data[17]))
            # Get field reserved bytes
            field.append(StripNulls(field_data[18:32]))
            self.fields.append(field)

    def DumpHeader(self):
        spaces = 30
        template  = "%%-%ds %%d" % spaces
        template1 = "%%-%ds 0x%%02x" % spaces
        print "File:  %s" % self.file_name
        print template1 % ("Version info", self.version_number),
        if self.version_number == 0x83:
            print " (with a .DBT memo file)"
        else:
            print " (without a .DBT memo file)"
        print template % ("Last update year", self.last_update_yy+1900)
        print template % ("Last update month", self.last_update_mm)
        print template % ("Last update day", self.last_update_dd)
        print template % ("Number of records", self.num_records)
        print template % ("Header length", self.header_length)
        print template % ("Record length", self.record_length)
        print template % ("Number of fields", self.num_fields)
        print "\nDump of field info:\n"
        print "   Num   Name        Type  Length"
        print "   ---   ----        ----  ------"
        for ix in range(self.num_fields):
            print "    %2d" % ix,            # Field number
            s = self.fields[ix]
            print "  %-12s" % s[0],          # Name
            print " %-1s"   % s[1],          # Type
            #print " \"%-4s\""   % s[2],
            print "   %3d"    % s[3]         # Length
            #print " %3d"    % s[4],
            #print " %-14s"  % s[5]
                
    def GetFileHandle(self):
        return self.fp

    def _get_record(self, record_num):
        '''Will return the specified record as a string.  Remember the
        first character is a ' ' or '*', indicating whether the record
        is deleted or not.
        '''
        if record_num < 0 or record_num > (self.num_records - 1):
            raise "Bad data", "Record number out of bounds"
        self.fp.seek(self.header_length + record_num*self.record_length)
        str = self.fp.read(self.record_length)
        return str

    def GetRecordAsList(self, record_num):
        '''Will return the indicated record as a list of strings.  The
        position in the list is the same as the field number.
        '''
        import string
        record = []
        str = self._get_record(record_num)
        if len(str) != self.record_length:
            raise "Bad data", "Record len is %d, not %d" %                 (len(str), self.record_length)
        offset = 1  # The 1 gets us past the first byte that indicates deletion
        for ix in xrange(self.num_fields):
            name   = self.fields[ix][0]
            type   = self.fields[ix][1]
            length = self.fields[ix][3]
            field  = str[offset : offset + length]
            record.append(field)
            offset = offset + length  # Position offset at start of next field
        return record

    def GetRecordAsDictionary(self, record_num):
        '''Will return the indicated record as a dictionary.  The keys
        will be the field names and the field data will be converted 
        to the proper type:  numbers will either be integers or doubles,
        dates will remain as YYYYMMDD strings, logical values and strings
        will remain as strings.
        '''
        import string
        record = {}
        str = self._get_record(record_num)
        if len(str) != self.record_length:
            raise "Bad data", "Record len is %d, not %d" %                 (len(str), self.record_length)
        offset = 1  # The 1 gets us past the first byte that indicates deletion
        for ix in xrange(self.num_fields):
            name   = self.fields[ix][0]
            type   = self.fields[ix][1]
            length = self.fields[ix][3]
            field  = str[offset : offset + length]
            if type == 'C' or type == 'L' or type == 'D':
                record[name] = field
            elif type == 'N':
                # Interpret as double if it has a '.' in it; otherwise 
                # interpret as a signed integer.
                value = 0
                field = string.strip(field)
                if field != "":
                    if '.' in field:
                        value = string.atof(field)
                    else:
                        value = string.atoi(field)
                record[name] = value
            elif type == 'M':
                # We ignore the memo field
                pass
            else:
                raise "Bad data", "Unrecognized field type"
            offset = offset + length  # Position offset at start of next field
        return record

    def DumpAsDelimited(self, no_header = 0, delimit_char = "\t", ws_strip = 1):
        '''Print each record of the database file to stdout with each 
        field delimited by the string in delimit_char.  Any leading or 
        trailing whitespace in each field is removed if ws_strip is true.
        The names of the fields are printed out as the first line if
        no_header is false.
        '''
        import sys, string
        if not no_header:
            # Print the header
            for ix in xrange(self.num_fields):
                field_name = self.fields[ix][0]
                sys.stdout.write(field_name)
                if ix != self.num_fields - 1:
                    sys.stdout.write(delimit_char)
            sys.stdout.write("\n")
        # Print each record
        for recnum in xrange(self.num_records):
            record = self.GetRecordAsList(recnum)
            for ix in xrange(self.num_fields):
                field = record[ix]
                if ws_strip:
                    field = string.strip(field)
                sys.stdout.write(field)
                if ix != self.num_records - 1:
                    sys.stdout.write(delimit_char)
            sys.stdout.write("\n")


if __name__ == '__main__':
    import sys, string
    if len(sys.argv) < 2:
        print "Usage:  dbase3 <dbase_file>"
        print "  Will dump the header and data of a dbase3 file."
        sys.exit(1)
    db = dBase3(sys.argv[1])
    db.DumpHeader()
    db.DumpAsDelimited()
