import MySQLdb,os

from vyperlogix.products.keys import _decode

_sql_ = '''
SELECT * INTO OUTFILE 'result.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM my_table;'''

path='.'
absPath = os.path.abspath(path)
print absPath

conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd=_decode('7065656B61623030'),db='django-heat-maps-prototype')

db_cursor = conn.cursor()

query = "LOAD DATA INFILE '"+ absPath + "/data.csv" +"' INTO TABLE django-heat-maps-prototype.smithmicro_sampleheatmapdata FIELDS TERMINATED BY ' ' LINES TERMINATED BY '\n' "

db_cursor.execute(query)
connection.commit()