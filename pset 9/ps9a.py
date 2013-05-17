###########################
# Problem Set 9: Space Cows 
# Name: Jorge Amaya
# Collaborators: none
# Time: 6:00

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


# Problem 2b: Curve Fitting: Finding an exponential fit
def expFit(x, y):
    """
    Find the best fit exponential curve z for the data contained in x and y.

    Parameters:
    x - a Pylab array of x values
    y - a Pylab array of y values

    Returns:
    a Pylab array of coefficients for the exponential fit function
    corresponding to the input domain x.
    """
    y = pylab.log2(y)
    return pylab.polyfit(x,y,1)
    

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
    
    def allPlots():
        """makes 3 calls to createPlots"""
        allData = [data1, data2, data3]
        prtData = 0
        
        for data in allData:
            prtData += 1
            createPlots(data, prtData)


    def createPlots(data, prtData):
        """
        This function saves 4 pylab plots, modeling:
        1. Linear
        2. Quadratic
        3. Quartic
        4. Exponential
        """
        degree = [1, 2, 4]
        iterList = [1,2,3]
        
        x = data[0]
        y = data[1]

        #use for 3 calls to polyFit()
        for i in iterList:
            #generate unique figure
            figure = i + ((prtData-1) * 4)

            #index for degree list
            index = i-1
            coef = polyFit(x, y, degree[index])
            
            #reset pylab plotter
            pylab.figure(figure)

            estimate = pylab.polyval(coef, x)
            ##print rSquare(y, estimate)

            #plots
            pylab.scatter(x, y)
            pylab.plot(x, estimate)
            pylab.savefig(str(figure), format=None)

        #single call to expFit()
        pylab.figure(4 * prtData)
        b, a = expFit(x,y)
        a = pylab.exp2(a)

        #exponential function
        estimate = ( a * ( 2 ** (b * x) ) )
        ##print rSquare(y, estimate)

        pylab.scatter(x, y)
        pylab.plot(x, estimate)
        pylab.savefig(str(4 * prtData), format=None) 
        
    allPlots()

if __name__ == "__main__":
    main()
    
