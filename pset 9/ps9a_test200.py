###########################
# Problem Set 9: Space Cows 
# Name: Jorge Amaya
# Collaborators: none
# Time:

import pylab

#============================
# Part A: Breeding Alien Cows
#============================

# Problem 1: File I/O
def loadData(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated x,y pairs.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    (x, y) - a tuple containing a Pylab array of x values and
             a Pylab array of y values
    """
    
    txtFile = open(filename)

    #parse file
    xList = []
    yList = []
    for line in txtFile:
        each = line.split(',')
        x = each[0]
        y = each[1].strip('\n')
        xList.append(int(x))
        yList.append(int(y))

    #pylab arrays
    xArray = pylab.array(xList)
    yArray = pylab.array(yList)
    
    return (xArray,yArray)


# Problem 2a: Curve Fitting: Finding a polynomial fit
def polyFit(x, y, degree):
    """
    Find the best fit polynomial curve z of the specified degree for the data
    contained in x and y and returns the expected y values for the best fit
    polynomial curve for the original set of x values.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values
    degree - the degree of the desired best fit polynomial

    Returns:
    a Pylab array of coefficients for the polynomial fit function of the
    specified degree, corresponding to the input domain x.
    """
    return pylab.polyfit(x, y, degree)
    

# Problem 3: Evaluating regression functions
def rSquare(measured, estimated):
    """
    Calculate the R-squared error term.

    Parameters:
    measured - one dimensional array of measured values
    estimate - one dimensional array of predicted values

    Returns: the R-squared error term
    """
    assert len(measured) == len(estimated)
    EE = ((estimated - measured)**2).sum()
    mMean = measured.sum()/float(len(measured))
    MV = ((mMean - measured)**2).sum()
    return 1 - EE/MV


#======================
# TESTING CODE
#======================
def main():
    # Problem 1
    data1 = loadData('ps9a_data1.txt')
    data2 = loadData('ps9a_data2.txt')
    data3 = loadData('ps9a_data3.txt')

    # Checks for Problem 1
    assert all( [len(data) == 25 for xy in data] for data in [data1, data2] ), \
        "Error loading data from files; number of terms does not match expected"
    assert all( [len(data) == 100 for xy in data] for data in [data1, data2] ), \
        "Error loading data from files; number of terms does not match expected"


    # Problem 4
    # TODO: Make calls to other functions here for calculating errors and
    # generating plots.
    

    def createPlots(data):
        x = data[0]
        y = data[1]

        a,b,c = polyFit(x, y, 2)

        x = pylab.arange(201)
        y = a*x**2 + b*x + c

        print pylab.polyval((a,b,c), 200)
        pylab.plot(x, y)
        pylab.show()
        
    createPlots(data3)

if __name__ == "__main__":
    main()
    
