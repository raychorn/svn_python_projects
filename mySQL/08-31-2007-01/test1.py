import _mysql
from heapq import heappush, heappop

fieldsHeap = []

db = _mysql.connect("192.168.105.67","root","foobarbaz","reports_development")

xx = db.query("""SHOW COLUMNS FROM reports""")

rx = db.store_result()

print """type(rx)=""", type(rx)

print """rx.num_fields=""", rx.num_fields()

nx = rx.num_rows()

print """nx=""", nx

for i in range(nx):
    xx = rx.fetch_row()
    print """type(xx)=""", type(xx)
    print """len(xx)=""", len(xx)
    print """xx[""", i, """]""", xx[0]
    heappush(fieldsHeap, xx[0])

print """fieldsHeap=""", fieldsHeap

x = db.query("""SELECT * FROM reports""")

r = db.store_result()

x = r.fetch_row()

print """type(r)=""", type(r)

print """type(x)=""", type(x)

print """r.num_fields=""", r.num_fields()

#print r.row_tell()

n = len(x)

print """n=""", n

print """x[0]""", x[0]

print """len(x[0])""", len(x[0])

for v in x:
    print """v=""", v
    for vv in v:
        print """vv=""", vv

print """<reports>"""
for v in x:
    print """<report"""
    for vv in v:
        print vv
print """>"""
