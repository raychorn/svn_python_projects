'''
#4
'''
__vectors__ = [('x', 1), ('y', 1), ('x', -1), ('y', -1)]

def spiral(w, h):
    matrix = []
    for hh in xrange(0, h):
        matrix.append([0 for i in xrange(0, w)])
    vi = 0
    x, y = (0, 0)
    i = 1
    m = (w*h)+1
    def turn_the_corner(x, y, vi, _is_=False):
        if (__vectors__[vi][0] == 'x'):
            x -= __vectors__[vi][-1]
        else:
            y -= __vectors__[vi][-1]
        vi += 1
        if (vi >= len(__vectors__)):
            vi = 0
        if (_is_):
            if (__vectors__[vi][0] == 'x'):
                x += __vectors__[vi][-1]
            else:
                y += __vectors__[vi][-1]
        return (x, y, vi)
    while (i < m):
        try:
            if (matrix[y][x] == 0):
                matrix[y][x] = i
            else:
                x, y, vi = turn_the_corner(x, y, vi, _is_=True)
                matrix[y][x] = i
            i += 1
        except IndexError:
            x, y, vi = turn_the_corner(x, y, vi)
        if (__vectors__[vi][0] == 'x'):
            x += __vectors__[vi][-1]
            if (x < 0):
                x, y, vi = turn_the_corner(x, y, vi, _is_=True)
        else:
            y += __vectors__[vi][-1]
            if (y < 0):
                x, y, vi = turn_the_corner(x, y, vi, _is_=True)
    return matrix

if (__name__ == '__main__'):
    for row in  spiral(3, 4):
        print row
    print '\n'
    for row in  spiral(5, 6):
        print row
