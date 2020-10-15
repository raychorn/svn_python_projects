from visual import *

_scene = display(title='Bouncing Ball', width=600, height=400, center=(0,4,3), background=(0,1,1))
_scene.select()
_scene.autocenter = 0
_scene.uniform = 1

floor = box (pos=(0,0,0), length=4, height=0.5, width=4, color=color.blue)
ball = sphere (pos=(0,4,0), radius=1, color=color.red)
ball.velocity = vector(0,-1,0)
dt = 0.01

def animateBall(isProfiling=False):
    while (not isProfiling):
        rate (100)
        ball.pos = ball.pos + ball.velocity*dt
        if ball.y < ball.radius:
            ball.velocity.y = -ball.velocity.y
        else:
            ball.velocity.y = ball.velocity.y - 9.8*dt

import psyco
psyco.bind(animateBall)

#import cProfile
#cProfile.run('animateBall(True)')

animateBall()
