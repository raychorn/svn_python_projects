import dis

def swap(a,b):
    print a,b
    return b,a

dis.dis(swap)

print swap(1,2)

swap2 = lambda a,b:(b,a)

print swap2(1,2)

dis.dis(swap2)
