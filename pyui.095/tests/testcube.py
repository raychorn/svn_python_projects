"""This demonstrates pyui with 3D drawing in the background.
"""

import pyui

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

rotateX = 0
rotateY = 0
rotateZ = 0

dirX = 0
dirY = 0
dirZ = 0

CUBE_POINTS = (
    (0.5, -0.5, -0.5),  (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),  (-0.5, -0.5, -0.5),
    (0.5, -0.5, 0.5),   (0.5, 0.5, 0.5),
    (-0.5, -0.5, 0.5),  (-0.5, 0.5, 0.5)
)

#colors are 0-1 floating values
CUBE_COLORS = (
    (1, 0, 0),          (1, 1, 0),
    (0, 1, 0),          (0, 0, 0),
    (1, 0, 1),          (1, 1, 1),
    (0, 0, 1),          (0, 1, 1)
)

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)


def cubeSetup():
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,640/480.0,0.1,100.0)    #setup lens
    glTranslate(0.0, -0.3, -3.0)                 #move back
    glRotate(25, 1, 0.5, 0)                       #orbit higher

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

def drawCube():
    global rotateX, rotateY, rotateZ, dirX, dirY, dirZ
    
    pyui.desktop.getRenderer().clear()

    dirX += rotateX
    dirY += rotateY
    dirZ += rotateZ

    glPushMatrix()
    glRotate(dirX, 1, 0, 0)
    glRotate(dirY, 0, 1, 0)
    glRotate(dirZ, 0, 0, 1)

    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    allpoints = zip(CUBE_POINTS, CUBE_COLORS)
    
    glBegin(GL_QUADS)
    for face in CUBE_QUAD_VERTS:
        for vert in face:
            pos, color = allpoints[vert]
            glColor3(color)
            glVertex(pos)
    glEnd()

    glColor3((1.0, 1.0, 1.0))
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex(pos)
    glEnd()

    glPopMatrix()

def createControl():

    w = pyui.widgets.Frame(0,0,200,100, "Controls")
    w.setLayout(pyui.layouts.GridLayoutManager(1,3))
    sx = pyui.widgets.SliderBar(setX, 10, int(rotateX*10) )
    sy = pyui.widgets.SliderBar(setY, 10, int(rotateY*10) )
    sz = pyui.widgets.SliderBar(setZ, 10, int(rotateZ*10) )

    w.addChild(sx)
    w.addChild(sy)
    w.addChild(sz)

    w.pack()

def setX(value):
    global rotateX
    rotateX = value/10.0

def setY(value):
    global rotateY
    rotateY = value/10.0

def setZ(value):
    global rotateZ
    rotateZ = value/10.0

def run():
    import testopt
    opts = testopt.parseCommandLine(800, 600)
    pyui.init(*opts)

    cubeSetup()
    pyui.desktop.getRenderer().setBackMethod(drawCube)

    createControl()
    con = pyui.dialogs.Console(0,500,780,80)
    pyui.run()

    print "done X"
    pyui.quit()
    print "quit."



if __name__ == '__main__':
    run()
