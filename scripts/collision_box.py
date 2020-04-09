# -*- coding: utf-8 -*-
"""
Created: Apr 2020
Classy Interacting Bouncing Balls in a box!

@author: Ryan Clement (RRCC)
"""

import random
import math as m
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

### Ball Class:
class Ball:
    """ Class for bouncing balls """
    ballCount = 0
    dt = 0.01              # s
    boxU = 10.0            # m
    boxD = 0.0             # m
    boxL = 0.0             # m
    boxR = 10.0            # m

    def __init__(self, x=0, y=0, vx=0, vy=0):
        """ Constructor """
        self.x = x
        self.xo = x
        self.y = y
        self.yo = y
        self.vx = vx
        self.vy = vy
        self.t = 0.0
        Ball.ballCount += 1

    def __del__(self):
        """ Destructor """
        Ball.ballCount -= 1

    def move(self):
        # X
        self.xo = self.x
        self.x += self.vx*Ball.dt
        # Y
        self.yo = self.y
        self.y += self.vy*Ball.dt
        # Collision with wall?
        self.__boundaries()
        # Time
        self.t += Ball.dt

    def __boundaries(self):
        # Y
        if( self.y < Ball.boxD ):
            tD = Ball.dt - (Ball.boxD - self.yo)/self.vy
            self.vy *= -1.0
            self.y = Ball.boxD + self.vy*tD
            self.yo = Ball.boxD
        elif( self.y > Ball.boxU ):
            tU = Ball.dt - (Ball.boxU - self.yo)/self.vy
            self.vy *= -1.0
            self.y = Ball.boxU + self.vy*tU
            self.yo = Ball.boxU
        # X
        if( self.x < Ball.boxL ):
            tL = Ball.dt - (Ball.boxL - self.xo)/self.vx
            self.vx *= -1.0
            self.x = Ball.boxL + self.vx*tL
            self.xo = Ball.boxL
        elif( self.x > Ball.boxR ):
            tR = Ball.dt - (Ball.boxR - self.xo)/self.vx
            self.vx *= -1.0
            self.x = Ball.boxR + self.vx*tR
            self.x = Ball.boxR
### END: Ball Class


### Collision Functions:
def collision(balls):
    d = 0.3       # For ms=5
    for i in np.arange(Ball.ballCount-1):
        for j in np.arange(i+1,Ball.ballCount):
            drx = balls[i].x - balls[j].x
            dry = balls[i].y - balls[j].y
            drs = drx*drx + dry*dry
            dr = m.sqrt( drs )
            if( dr < d ):
                # Over-Shot Collision
                # TODO: Add switch for method selection
                if( False ):
                    # Physics Based Collision Correction
                    xi = balls[i].x - 10.0*Ball.dt*balls[i].vx
                    yi = balls[i].y - 10.0*Ball.dt*balls[i].vy
                    xj = balls[j].x - 10.0*Ball.dt*balls[j].vx
                    yj = balls[j].y - 10.0*Ball.dt*balls[j].vy
                    drx = xi - xj
                    dry = yi - yj
                    dvx = balls[i].vx - balls[j].vx
                    dvy = balls[i].vy - balls[j].vy
                    drs = d*d
                    a = dvx*dvx + dvy*dvy
                    b = 2.0*(drx*dvx + dry*dvy)
                    c = drx*drx + dry*dry - drs
                    s = b*b - 4.0*a*c
                    tp = (-b + m.sqrt(s))/(2.0*a)
                    tm = (-b - m.sqrt(s))/(2.0*a)
                    if( tp>0 and tm>0 ):
                        tc = min(tp,tm)
                    elif( tm<0 ):
                        tc = tp
                    else:
                        tc = tm
                    xci = xi + tc*balls[i].vx
                    yci = yi + tc*balls[i].vy
                    xcj = xj + tc*balls[j].vx
                    ycj = yj + tc*balls[j].vy
                    drx = xci - xcj
                    dry = yci - ycj
                elif( True ):
                    # Game Engine Style Collision Correction
                    offset = (d - dr)/2.0
                    dx = offset*drx/dr
                    dy = offset*dry/dr
                    xiNew = balls[i].x + dx
                    yiNew = balls[i].y + dy
                    xjNew = balls[j].x - dx
                    yjNew = balls[j].y - dy
                    drx = xiNew - xjNew
                    dry = yiNew - yjNew
                    drs = d*d
                    dvx = balls[i].vx - balls[j].vx
                    dvy = balls[i].vy - balls[j].vy
                    fac = (dvx*drx + dvy*dry)/drs
                    delvx = fac*drx
                    delvy = fac*dry
                    balls[i].vx -= delvx
                    balls[i].vy -= delvy
                    balls[j].vx += delvx
                    balls[j].vy += delvy
                    balls[i].x = xiNew
                    balls[i].y = yiNew
                    balls[j].x = xjNew
                    balls[j].y = yjNew
            elif( dr == d ):
                # Perfect Collision!
                # This is going to be a VERY rare event ...
                dvx = balls[i].vx - balls[j].vx
                dvy = balls[i].vy - balls[j].vy
                fac = (dvx*drx + dvy*dry)/drs
                delvx = fac*drx
                delvy = fac*dry
                balls[i].vx -= delvx
                balls[i].vy -= delvy
                balls[j].vx += delvx
                balls[j].vy += delvy

### END: Collision Functions


### Animation Functions:
def init():
    tText.set_text('Time = ')
    return scat, tText

def animate(i):
    s = 'Time = %.1f s' % ballList[0].t
    tText.set_text(s)
    sList = []
    for b in ballList:
        sList.append([b.x,b.y])
    scat.set_offsets(sList)
    # Graphics are updated every 10 time steps.
    # ... update positions and check for collisions 10 times.
    for i in np.arange(10):
        for b in ballList:
            b.move()
        collision(ballList)
    return scat,tText
### END: Animation Functions


##### Movie Time!
numBalls = 25
ballList = []
xList = []
yList = []
for i in range(numBalls):
    xR  = random.uniform(1,9)
    yR  = random.uniform(1,9)
    vxR = random.uniform(-5.0,5.0)
    vyR = random.uniform(-5.0,5.0)
    ballList.append( Ball(xR,yR,vxR,vyR) )
    xList.append(xR)
    yList.append(yR)

fig, ax = plt.subplots()
ax.set_title('Bouncing Balls!')
ax.set_xlim([0,10])
ax.set_ylim([0,10])
tText = ax.text(4.5, 9.5, 'Time = ')
scat = ax.scatter(xList,yList,c=xList,cmap='gist_rainbow')
# scat = ax.scatter(xList,yList,c=xList,cmap='seismic')


ani = animation.FuncAnimation(fig, animate, frames=101,
                              interval=100, blit=True,
                              init_func=init, repeat=False)

# Uncomment next two lines to write file to disk.
#pwriter = animation.PillowWriter(fps=5, metadata=dict(artist='Dr. Ryan Clement'))
#ani.save('../movies/bouncing_balls.gif',writer=pwriter)

plt.show()
##### END: Movie Time
