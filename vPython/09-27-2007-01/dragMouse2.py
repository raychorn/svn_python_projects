from visual import *

scene = display(title='Drag the Arrow', width=600, height=400, center=(0,4,3), background=(0,1,1))
scene.select()
scene.autocenter = 0
scene.uniform = 1

scene.range = 10 # fixed size, no autoscaling
pointer = arrow(pos=(0,4,0), axis=(3,2,0), color=color.yellow)
tolerance = 0.3 # must click within this distance of tail or tip
drag = None # have not selected tail or tip of arrow
while 1: 
    if scene.mouse.events: 
        m1 = scene.mouse.getevent() # obtain press or drag or drop event
        if m1.press:
            if mag(pointer.pos-m1.pos) <= tolerance:
                drag = 'tail' # pressed near tail of arrow
            elif mag((pointer.pos+pointer.axis)-m1.pos) <= tolerance:
                drag = 'tip' # pressed near tip of arrow
                drag_pos = m1.pos # save press location
        elif m1.drag and drag: # if drag event and something to drag
            scene.cursor.visible = 0 # make cursor invisible 
        elif m1.drop: # released the mouse button at end of drag
            drag = None # end dragging (None is False)
            scene.cursor.visible = 1 # cursor visible again
    if drag: 
        new_pos = scene.mouse.pos
        if new_pos != drag_pos: # if the mouse has moved since last position
            displace = new_pos - drag_pos # how much the mouse moved
            drag_pos = new_pos # update drag position
            if drag == 'tail':
                pointer.pos += displace # displace the tail
            else:
                pointer.axis += displace # displace the tip
