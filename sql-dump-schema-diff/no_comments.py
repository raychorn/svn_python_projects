import re, sys

if (__name__ == '__main__'):
    sql = sys.stdin.read()
    regex = re.compile(r'/\*![^\n]* \*/;\n', re.M)
    print regex.sub('', sql)
