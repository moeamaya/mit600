# Problem Set 6: Simulating robots
# Name: Jorge Amaya
# Collaborators: None
# Time: 10:00

import math
import random

import ps6_visualize
import pylab

# For python 2.6:
#from ps6_verify_movement26 import testRobotMovement

# If you get a "Bad magic number" ImportError, comment out what's above and
# uncomment this line (for python 2.7):
from ps6_verify_movement27 import testRobotMovement

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.clean = []
        
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()
        tileX = math.floor(x)
        tileY = math.floor(y)
        #checking whether tile is cleaned for adding to cleaned list
        if not self.isTileCleaned(tileX,tileY):
            self.clean.append((tileX, tileY))
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m,n) in self.clean:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.clean)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))

        return Position(x,y)


    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        #checking extents of rectangle to make sure position in bounds
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return True
        else:
            return False


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = room.getRandomPosition()
        self.dir = random.choice(range(360))

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position
        

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """ 
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #generates new position
        move = self.pos.getNewPosition(self.dir, self.speed)
        #if in bounds will clean and move on
        if self.room.isPositionInRoom(move):
            self.setRobotPosition(move)
            self.room.cleanTileAtPosition(move)
        #otherwise just rotates robot and tries again    
        else:
            angle = random.choice(range(360))
            self.setRobotDirection(angle)
        

# Uncomment this line to see your implementation of StandardRobot in action!
testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    room = RectangularRoom(width, height)
    
    def listRobots(num_robots, room, speed, robot_type):
        """creates a list of robots depending on type and number"""
        robots = []
        for i in range(num_robots):
            robot = robot_type(room, speed)
            robots.append(robot)
        return robots
       
    def simClean(room, min_coverage):
        """simulates a # of steps req for # of robots to clean certain %"""
        #resetting all values
        cleanPercent = 0.0
        clean = 0.0
        steps = 0
        robots = listRobots(num_robots, room, speed, robot_type)
        total = float(room.getNumTiles())
        
        #loop to run until % reached
        while cleanPercent < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean()
            #anim.update(room, robots)
            steps += 1
            clean = float(room.getNumCleanedTiles())
            #test percentage
            cleanPercent = clean / total
        
        return steps
        
    def simTrials(room, num_trials):
        """simulates a number of trials on simClean() and returns total step #"""
        totalSteps = 0
        for n in range(num_trials):
            room = RectangularRoom(width, height)
            #anim = ps6_visualize.RobotVisualization(num_robots, width, height)
            totalSteps += simClean(room, min_coverage)

        #returns the mean value of steps
        return totalSteps / num_trials

    return simTrials(room, num_trials)
 
# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #generates new position
        move = self.pos.getNewPosition(self.dir, self.speed)

        #if in bounds will clean, rotate and move on
        if self.room.isPositionInRoom(move):
            angle = random.choice(range(360))

            self.setRobotDirection(angle)
            self.setRobotPosition(move)
            self.room.cleanTileAtPosition(move)

        #otherwise just rotates robot and tries again 
        else:
            angle = random.choice(range(360))
            self.setRobotDirection(angle)

avg = runSimulation(1, 1.0, 10, 10, .75, 100, StandardRobot)
print avg

# === Problem 5
#
# 1a) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       Located at the end   
#
# 1b) How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
#       The randomness of the RandomWalkRobot as the # of robots increase
#       starts to approach the same time/steps as the StandardRobot. Over a larger
#       sum of robots, the randomness is mitigated. 
#
# 2a) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       Located at the end 
#
# 2b) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, 50x6
#
#       The more square the dimension, the better the RandomWalkRobot does. This makes
#       sense since it allows the most amount of options for an object that moves in all
#       four directions. As the room narrows, the random robot has more difficulty cleaning
#       the extents of the room.
#



def showPlot1(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
#showPlot1("Time to clean 80% of a 20x20 room for various number of robots", "Robots", "Time/Steps")
#showPlot2("Time to clean 80% of a various room dimensions with 2 robots", "Aspect Ratio", "Time/Steps")
