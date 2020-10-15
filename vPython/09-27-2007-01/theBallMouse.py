from visual import *

_scene = display(title='Bouncing Ball', width=600, height=400, center=(0,4,3), background=(0,1,1))
_scene.select()
_scene.autocenter = 0
_scene.uniform = 1

floor = box (pos=(0,0,0), length=4, height=0.5, width=4, color=color.blue)
ball = sphere (pos=(0,4,0), radius=1, color=color.red)
ball.velocity = vector(0,-1,0)
dt = 0.01

while 1:
    rate (100)
    temp = _scene.mouse.project(normal=(0,1,0), point=(0,3,0))
    if temp: # temp is None if no intersection with plane
        ball.pos = temp

