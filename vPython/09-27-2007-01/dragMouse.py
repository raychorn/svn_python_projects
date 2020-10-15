from visual import *

scene = display(title='Drag the Ball', width=600, height=400, center=(0,4,3), background=(0,1,1))
scene.select()
scene.autocenter = 0
scene.uniform = 1

scene.range = 10 # fixed size, no autoscaling
ball = sphere(pos=(-5,0,0), radius=1., color=color.cyan)
cube = box(pos=(+5,0,0), size=(2,2,2), color=color.red)
pick = None # no object picked out of the scene yet
while 1: 
    if scene.mouse.events: 
        m1 = scene.mouse.getevent() # obtain drag or drop event
        if m1.drag and m1.pick == ball: # if clicked on the ball
            drag_pos = m1.pickpos # where on the ball the mouse was
            pick = m1.pick # pick is now True (nonzero)
            scene.cursor.visible = 0 # make cursor invisible 
        elif m1.drop: # released the mouse button at end of drag
            pick = None # end dragging (None is False)
            scene.cursor.visible = 1 # cursor visible again
    if pick: 
        new_pos = scene.mouse.project(normal=(0,1,0)) # project onto xz plane
        if new_pos != drag_pos: # if the mouse has moved since last position
            pick.pos += new_pos - drag_pos # offset for where the ball was clicked
            drag_pos = new_pos # update drag position

