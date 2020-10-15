import time
import pyui
import PyUnseen


def CreateTestTerrainDetails():
  foo = (4, 4, [0,9,2,3,4,5,3,7,3,6,5,4,3,2,7,1], [])  # height, width, heightmap, features
  return foo



def onbutton(self):
    print "got a button " 
    
def run():
    done = 1
    frame = 0
    t = time.time()

    import testopt
    opts = testopt.parseCommandLine(800, 600, "dx")
    pyui.init(*opts)
    
    #w = pyui.widgets.ViewWindow(10, 10, 400, 300)
    #w.pack()


    terrainDetails = CreateTestTerrainDetails()
    terrain = PyUnseen.createTerrainRegion( terrainDetails )  # will take dictionary of stuff
    rootWorld = PyUnseen.getRootWorld()

    PyUnseen.addToWorld( rootWorld, terrain ) # just like any other object 

    cameraPos = ( -10, 6, -10 )
    cameraDir = ( 45, -45, 0 )

    view1 = PyUnseen.createView( rootWorld ) # will also take zMin, zMax?
    PyUnseen.setCameraParameters( view1, cameraPos, cameraDir )

    rootView = PyUnseen.getRootView()
    PyUnseen.setCameraParameters( rootView, cameraPos, cameraDir )

    while done:
        pyui.draw()
        done = pyui.update()

    print "done"
    pyui.quit()


if __name__ == '__main__':
    run()
