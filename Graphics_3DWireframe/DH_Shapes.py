#==============================
# Diego Holguin
# CSC345: Computer Graphics
#   Fall 2016
# Description:
#   Transforms: Illustrates effects of transformations
#   on a given scene (in 3-Dimensions now).
#==============================

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

# These parameters define the camera's lens shape
CAM_NEAR = 0.01
CAM_FAR = 10000.0
CAM_ANGLE = 60.0

# These parameters define simple animation properties
MIN_STEP = 0.2
ANGLE_STEP = 1
FPS = 60.0
DELAY = int(1000.0 / FPS + 0.5)

# Object Translation Variables
objectConstantForce = 0.0000005 # Amount of force applied each frame
objectRotationStep = 0.1 # Amount of rotation applied for each user input instance
userMovement = 0.0 # The amount of movement that is applied to the car, in total

# Object Translation Constants
OBJECTMOVEMENTANIMATION = 0.01 # Default value for movement of car, without user input
OBJECTSPEEDUP = 0.005 # Default value for speed up incrementation for the car 
OBJECTSPEEDDOWN = -0.004 # Default value for speed down incrementation for the car 
OBJECTMAXDISTANCE = 2 # Max distance the car is enabled to travel

# Color's of the vehicle
OBJCOLOR_R = 1
OBJCOLOR_G = 0
OBJCOLOR_B = 0

# Global (Module) Variables
winWidth = 1000
winHeight = 1000
name = b'Car Animation'
step = MIN_STEP
animate = False
angleMovement = 0
perspectiveMode = True

"""
* main:
* 	Main Loop
"""
def main():
    # Create the initial window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(winWidth, winHeight)
    glutInitWindowPosition(100,100)
    glutCreateWindow(name)

    init()

    # Setup the callback returns for display and keyboard events
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialKeys)
    glutTimerFunc(0, timer, DELAY)

    # Enters the main loop.   
    # Displays the window and starts listening for events.
    glutMainLoop()
    return
"""
* init:
* 	Any initialization material to do...
"""
def init():
    global tube, ball
    tube = gluNewQuadric()
    gluQuadricDrawStyle(tube, GLU_LINE)
    ball = gluNewQuadric()
    gluQuadricDrawStyle(ball, GLU_LINE)

"""
* display:
* 	Callback function used to display the scene
* 	Currently it just draws a simple polyline (LINE_STRIP)
"""
def display():
    # Set the viewport to the full screen
    glViewport(0, 0, winWidth, winHeight)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if perspectiveMode:
        # Set view to Perspective Proj. (angle, aspect ratio, near/far planes)
        gluPerspective(CAM_ANGLE, winWidth/winHeight, CAM_NEAR, CAM_FAR)
    else:
        glOrtho(-winWidth/40, winWidth/40, -winHeight/40, winHeight/40, -100, 100)
    
    # Clear the Screen
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # And draw the "Scene"
    glColor3f(1.0, 1.0, 1.0)
    drawScene()

    # And show the scene
    glFlush()
    glutSwapBuffers()  # needed for double buffering!

"""
* timer: 
* 	used to animate the scene when activated
"""
def timer(alarm):
    glutTimerFunc(0, timer, DELAY)   # Start alarm clock again
    if animate:
        # Advance to the next frame
        advance()
        glutPostRedisplay()

"""
* advance: 
* 	advances the frame
"""
def advance():
    global angleMovement, objectConstantForce, objectRotationStep, OBJECTMOVEMENTANIMATION, userMovement, OBJECTMAXDISTANCE

	# Increment the value of the Object's animation variable    
    objectConstantForce += OBJECTMOVEMENTANIMATION + userMovement

    # Increment Rotation
    objectRotationStep += 0.3
    
    # Handle the back and forth motion of the objects in the scene
    if objectConstantForce > OBJECTMAXDISTANCE:
    	OBJECTMOVEMENTANIMATION = OBJECTMOVEMENTANIMATION * -1
    	userMovement = 0
    elif objectConstantForce < -OBJECTMAXDISTANCE:
    	OBJECTMOVEMENTANIMATION = (OBJECTMOVEMENTANIMATION * -1)
    	userMovement = 0
    
    # Make sure that the angle movement doesn't get too large..
    if angleMovement >= 360:
        angleMovement -= 360 
    elif angleMovement < 0:
        angleMovement += 360

"""
* specialKeys: 
* 	Callback function used to handle special key events, as defined by GLUT
* 	Currently, it just responds to the ESC key (which quits)
* 	key: ASCII value of the key that was pressed
* 	x,y: Location of the mouse (in the window) at time of key press)
"""
def specialKeys(key, x, y):
	global angleMovement, ANGLE_STEP, userMovement # get global variables.. not best practice
	
	if key == GLUT_KEY_LEFT:
		angleMovement -= ANGLE_STEP
	elif key == GLUT_KEY_RIGHT:
		angleMovement += ANGLE_STEP
	elif key == GLUT_KEY_UP:
		OBJECTMOVEMENTZ +=OBJECTSTEP
	elif key == GLUT_KEY_DOWN:
		OBJECTMOVEMENTZ -=OBJECTSTEP


"""
* keyboard:
* 	Callback function used to handle normal key events, as defined by GLUT
* 	Currently, it just responds to the ESC key (which quits)
* 	key: ASCII value of the key that was pressed
* 	x,y: Location of the mouse (in the window) at time of key press)
"""
def keyboard(key, x, y):
    if ord(key) == 27:  # ASCII code 27 = ESC-key
        exit(0)
    elif ord(key) == ord('p'):
        global perspectiveMode # get global variables.. not best practice
        # print("DEBUG: Toggling perspective mode")
        perspectiveMode = not perspectiveMode
        glutPostRedisplay()
    elif ord(key) == ord(' '):
        global animate # get global variables.. not best practice
        animate = not animate
    elif ord(key) == ord('r'):
    	# print ("DEBUG : Pressed R Key")
    	global OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B # get global variables.. not best practice
    	OBJCOLOR_R = 1
    	OBJCOLOR_G = 0
    	OBJCOLOR_B = 0
    elif ord(key) == ord('g'):
    	# print ("DEBUG : Pressed G Key")
    	global OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B # get global variables.. not best practice
    	OBJCOLOR_R = 0
    	OBJCOLOR_G = 1
    	OBJCOLOR_B = 0
    elif ord(key) == ord('b'):
    	# print ("DEBUG : Pressed B Key")
    	global OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B # get global variables.. not best practice
    	OBJCOLOR_R = 0
    	OBJCOLOR_G = 0
    	OBJCOLOR_B = 1
    elif ord(key) == ord("w"):
    	# print ("DEBUG : Pressed B Key")
    	global OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B # get global variables.. not best practice
    	OBJCOLOR_R = 1
    	OBJCOLOR_G = 1
    	OBJCOLOR_B = 1    
    elif ord(key) == ord('q'):
    	# print ("DEBUG : Pressed Q Key")
    	global userMovement, OBJECTSPEEDDOWN # get global variables.. not best practice
    	userMovement += OBJECTSPEEDDOWN
    elif ord(key) == ord('e'):
    	# print ("DEBUG : Pressed E Key")
    	global userMovement, OBJECTSPEEDUP # get global variables.. not best practice
    	userMovement += OBJECTSPEEDUP

"""
* drawScene:
*    Draws a simple scene with a few shapes
"""
def drawScene():
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslate(0, -3, -20)   # Move world coordinate system so it is in view
    glScalef(5,5,5)
    drawEnvironment()
    glRotated(angleMovement, 0, 1, 0)  # Spin around y-axis
    glColor3f(1, 1, 1)
    drawCar() 
    
def drawEnvironment():
	global OBJECTMAXDISTANCE
	
	glPushMatrix()  # get's the last used instance of a matrix from the stack
	
	glTranslated(-OBJECTMAXDISTANCE - 1,0.5,0)
	glRotated(90,1,0,0) 
	gluCylinder(tube, 0.00, 0.4, 0.5,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack
	glPushMatrix()
	
	glTranslated(OBJECTMAXDISTANCE + 1,0.5,0)
	glRotated(90,1,0,0) 
	gluCylinder(tube, 0.00, 0.4, 0.5,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack


"""
* drawCar:
*    Draws the car within the scene
"""
def drawCar():
	global OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B # get global variables.. not best practice
	
	glPushMatrix()  # get's the last used instance of a matrix from the stack
	
	# Draw Car Upper Body
	drawSquare(0.5, 0.3, 0.5, 0, 0.35, 0, OBJCOLOR_R, OBJCOLOR_G, OBJCOLOR_B) # Draw a squished rectangle 5 units away from the origin
	
	# Draw Car Lower Body
	drawSquare(0.7, 0.05, 0.7, 0, 0, 0, OBJCOLOR_R, OBJCOLOR_G, OBJCOLOR_B) # Draw a squished rectangle 0 units away from the origin
	
	# Draw Tires
	drawTires(0.1,10,10,OBJCOLOR_R,OBJCOLOR_G,OBJCOLOR_B,0.55,-0.15,0.45)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack

"""
* drawTires:
*    Draws a series of tires based upon its x,y,z scale values, transforms it to a 2D point, with a specified color
"""
def drawTires(radius, slices, stacks, r, g, b, xPos, yPos, zPos):
	global angleMovement, objectConstantForce, objectRotationStep # get global variables.. not best practice
	
	# Default tire rotation speed
	tireSpeed = 4	
		
	glColor(r, g, b) # set the tires color
	
	glPushMatrix()
	
	# Draw Tire One
	glTranslatef(xPos + objectConstantForce,yPos,zPos)
	glRotated(objectRotationStep * tireSpeed, 0, 0, 1)
	gluCylinder(tube, 0.1, 0.1, 0.1,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack
	glPushMatrix()  # get's the last used instance of a matrix from the stack
	
	# Draw Tire Two
	glTranslatef(-xPos + objectConstantForce,yPos,zPos)
	glRotated(objectRotationStep * tireSpeed, 0, 0, 1)
	gluCylinder(tube, 0.1, 0.1, 0.1,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack
	glPushMatrix()  # get's the last used instance of a matrix from the stack
	
	#Draw Tire Three
	glTranslatef(xPos + objectConstantForce,yPos,-zPos)
	glRotated(objectRotationStep * tireSpeed, 0, 0, 1)
	gluCylinder(tube, 0.1, 0.1, 0.1,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack
	glPushMatrix()  # get's the last used instance of a matrix from the stack

	#Draw Tire Four 
	glTranslatef(-xPos + objectConstantForce,yPos,-zPos)
	glRotated(objectRotationStep * tireSpeed, 0, 0, 1)
	gluCylinder(tube, 0.1, 0.1, 0.1,20,20)
	
	glPopMatrix() # Pop the matrix that has been performed on from the matrix stack

"""
* drawSquare:
*    Draws a square based upon its x,y,z scale values, transforms it to a 2D point, with a specified color
"""    
def drawSquare(xScale,yScale,zScale, xOffset, yOffset, zOffset, r,g,b):
	global objectConstantForce # get global variables.. not best practice
	
	glPushMatrix()
	glTranslatef(xOffset + objectConstantForce,yOffset,zOffset)
	glColor3f(r,g,b)
	glBegin(GL_LINE_LOOP) # Draw the back side of the square
	glVertex3f(xScale, -yScale, zScale);
	glVertex3f(xScale, yScale , zScale);
	glVertex3f(-xScale, yScale, zScale);
	glVertex3f(-xScale, -yScale, zScale);
	glEnd();
	glBegin(GL_LINE_LOOP) # Draw the right side of the square
	glVertex3f(xScale, -yScale, -zScale);
	glVertex3f(xScale,  yScale, -zScale);
	glVertex3f(xScale,  yScale, zScale);
	glVertex3f(xScale, -yScale, zScale);
	glEnd();
	glBegin(GL_LINE_LOOP) # Draw the left side of the square
	glVertex3f(-xScale, -yScale, zScale);
	glVertex3f(-xScale, yScale, zScale);
	glVertex3f(-xScale, yScale, -zScale);
	glVertex3f(-xScale, -yScale, -zScale);
	glEnd();
	glBegin(GL_LINE_LOOP)# draw the top side of the square
	glVertex3f(xScale, yScale, zScale);
	glVertex3f(xScale, yScale, -zScale);
	glVertex3f(-xScale, yScale, -zScale);
	glVertex3f( -xScale, yScale, zScale);
	glEnd();
	glBegin(GL_LINE_LOOP) # draw the bottom side of the swuare
	glVertex3f(xScale, -yScale, -zScale);
	glVertex3f(xScale, -yScale, zScale);
	glVertex3f(-xScale, -yScale, zScale);
	glVertex3f( -xScale, -yScale, -zScale);
	glEnd();
	glPopMatrix()
    
if __name__ == '__main__': main()
