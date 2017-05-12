#==============================
# Diego Holguin
# CSC345: Computer Graphics
#   Fall 2016
# ScreenSaver.py
#	To use OpenGL's GLUT library to render a 640 by 480 window of a screen saver. One
# 	that renders a parabolic curve along with the fading out of colors after some 
# 	specified number of lines have been rendered. 
#==============================

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import collections 
from collections import namedtuple
import sys
import math

# Deque container that will contain all of the lines that will rendered for each cycle
# ------------------------------------------------------------------------------------
linesToBeDrawn = collections.deque()

# Window Related Variables
# -----------------------
winWidth = 640
winHeight = 480
halfX = winWidth/2
halfY = winHeight/2

# Graph Related Variables
# -----------------------
coordinateMarks = 20 # The number of coordinate points for each X+ and Y+ axis
xCoordinate = halfX/coordinateMarks # The unit x coordinate value (X axis's first positive index)
yCoordinate = halfY/coordinateMarks # The unit y coordinate value ((Y axis's first positive index )
yScale = coordinateMarks
xScale = (coordinateMarks - (coordinateMarks-1))
quadrentDraw = 1
colorRatio = 1

# Name of the GLUT Window
# -----------------------
name = b'Parabolic Curve Screen Saver'

# Animation Related Variables
# -----------------------
lineCount = 0 # The number of lines that need to be drawn 
spacePressed = True # The flag that indicates whether the space bar has been pressed or not

# Constants
# ---------
DELAY=50 # Delay value used to delay the rendering process
MAXLINES=50 # The maximum number of lines that can be rendered at any given time
STEPS=1 # Nothing at the moment, might use later


def main():
    # Create the initial window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(100,100)
    glutCreateWindow(name)

    init()
    
    # This callback is invoked when window needs to be drawn or redrawn
    glutDisplayFunc(display)

    # This callback is invoked when a keyboard event happens
    glutKeyboardFunc(keyboard);

    glutTimerFunc(DELAY, timer, 0)

    # Enters the main loop.   
    # Displays the window and starts listening for events.
    glutMainLoop()
    return

def timer(alarm):
    global degree
    glutTimerFunc(DELAY, timer, 0)
    # degree += STEPS
    glutPostRedisplay()

# Initialize some of the OpenGL matrices
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    halfX = winWidth/2
    halfY = winHeight/2
    gluOrtho2D(-halfX,halfX, -halfY, halfY)
    
def drawGraph():
	# Enable read/write access to global variables
	global halfX
	global halfY
	
	# Set up the X and Y coordinates line positions
	graphXVertices = (-halfX, 0.0, 0.0, halfX, 0.0, 0.0)
	graphYVertices = (0.0, halfY, 0.0, 0.0, -halfY, 0.0)
	
	# Set up the X and Y coordinates colors
	graphYColor = (0.0,1.0,0.0)
	graphXColor = (0.0,1.0,0.0)
	
	# Create a tuple containing the X and Y coordinates line positions as well as color
	graphYLine = graphYVertices + graphYColor
	graphXLine = graphXVertices + graphXColor
	
	# Add the X and Y line's to the deque, so they can be rendered
	linesToBeDrawn.append(graphXLine)
	linesToBeDrawn.append(graphYLine)
    
def drawShape():
	# Enable read/write access to global variables
    global halfX
    global halfY
    global quadrentDraw
    global coordinateMarks
    global MAXLINES
    global xScale
    global yScale
    global quadrentDraw
    global colorRatio
    
    if spacePressed == True:
    
   		# Set up instance variables that will be used for the rendering process
    	colorFadeRatio = 0.05
       	
		# ------------------------ Draw Cases for drawing the parabolic curve!  ------------------------ #
    	
    	if quadrentDraw == 1:
    		# Create a tuple containing the two vertices' location for Quadrent 1
    		lineVertices = (0.0, yCoordinate*yScale, 0.0, xCoordinate*xScale, 0.0, 0.0)
    	elif quadrentDraw == 2:
    		# Create a tuple containing the two vertices' location for Quadrent 2
    		lineVertices = (-0.0, yCoordinate*yScale, 0.0, -xCoordinate*xScale, 0.0, 0.0)
    	elif quadrentDraw == 3:
    		# Create a tuple containing the two vertices' location for Quadrent 3
    		lineVertices = (-0.0, -yCoordinate*yScale, 0.0, -xCoordinate*xScale, -0.0, 0.0)
    	else:
    		# Create a tuple containing the two vertices' location for Quadrent 4
    		lineVertices = (0.0, -yCoordinate*yScale, 0.0, xCoordinate*xScale, -0.0, 0.0)
    	    		
    	# -------- The Process of drawing/calculating the original parabolic curve (non-rotated) -------- #
    	
    	# Mathematical Calculations for the non-rotated line's slope, angle in Degrees & Radians, and it's magnitude
    	lineSlope = (lineVertices[4] - lineVertices[1])/ (lineVertices[3] - lineVertices[0])
    	lineAngleInDegrees = math.atan(lineSlope)
    	lineAngleInRadians = math.pi*lineAngleInDegrees/180
    	lineMagnitude = math.sqrt((lineVertices[3] - lineVertices[0])**2 + (lineVertices[4] - lineVertices[1])**2)
    	
    	# Create a tuple containing mathematical information about the non-rotated line
    	lineMInfo = (lineSlope, lineAngleInDegrees, lineAngleInRadians, lineMagnitude)
    	
    	# Create a tuple containing the color, vertice positions, and line information for a given line
    	line = lineVertices + lineMInfo
    	    	
    	if len(linesToBeDrawn) < MAXLINES:
    		linesToBeDrawn.append(line)
    	else:
    		linesToBeDrawn.popleft()
    	linesToBeDrawn.append(line)
    	    	
    	# Render the graph, optional
    	# drawGraph()
    	    	
    	# Update Variables
    	yScale = yScale - 1
    	xScale = xScale + 1
    
    # Make background black 
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    # Clear the Color buffer before drawing
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw every line within the scene
    for index, singleLine in enumerate(linesToBeDrawn):
        glBegin(GL_LINES)
        colorRatio = (MAXLINES/(index+1)) * 0.2
        quadrentColor = (1.0 * colorRatio,0.0,0.0) # Red
        glColor3f(quadrentColor[0] ,quadrentColor[1], quadrentColor[2])
        glVertex3f(singleLine[0], singleLine[1], singleLine[2])
        glVertex3f(singleLine[3],singleLine[4],singleLine[5])
        glEnd()

    # Since we have now drawn for one quadrant, let's move to another quadrant
    if yScale <= 1:
    	quadrentDraw = quadrentDraw + 1
    	yScale = coordinateMarks
    	xScale = (coordinateMarks - (coordinateMarks-1))
   		
    # Swap Buffers
    glutSwapBuffers()
    
    # After drawing for quadrants 1 - 4, start again, beginning in the first quadrant 
    if quadrentDraw == 5:
    	quadrentDraw = 1
    
# Callback function used to display the scene
# Currently it just draws a simple polyline (LINE_STRIP)
def display():
	drawShape()
    
# Callback function used to handle any key events
# Currently, it just responds to the ESC key (which quits)
# key: ASCII value of the key that was pressed
# x,y: Location of the mouse (in the window) at time of key press)
def keyboard(key, x, y):
	global spacePressed
	if ord(key) == 27:  # ASCII code 27 = ESC-key
		exit(0)
	elif ord(key) == 32:
		spacePressed = not spacePressed

if __name__ == '__main__': main()
