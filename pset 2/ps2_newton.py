# 6.00 Problem Set 2
# Name: Jorge Amaya
# Collaborators: None
# Time: 3:30

# Successive Approximation: Newton's Method


def evaluate_poly(poly, x):
    """
    Computes the value of a polynomial function at given value x. Returns that
    value as a float.

    Example:
    >>> poly = [0.0, 0.0, 5.0, 9.3, 7.0]    # f(x) = 5x^2 + 9.3x^3 + 7x^4 
    >>> x = -13
    >>> print evaluate_poly(poly, x)  # f(-13) = 5(-13)^2 + 9.3(-13)^3 + 7(-13)^4 
    180339.9

    poly: list of numbers, length > 0
    x: number
    returns: float
    """
    if len(poly) == 0:
        print "Please enter list for poly"
        assert False
    
    #define result to use and return a float
    result = 0.0

    #loops through each part of the polynomial and adds up the total value    
    for i in range(len(poly)):
        result = result + poly[i]*(x**i)

    #print result
    return result

#test variables
##poly = [0.0, 0.0, 5.0, 9.3, 7.0]
##x = -13
##evaluate_poly(poly, x)


def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function as a list of
    floats. If the derivative is 0, returns [0.0].

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> print compute_deriv(poly)        # 35^x + 9x^2 + 4x^3
    [0.0, 35.0, 9.0, 4.0]

    poly: list of numbers, length > 0
    returns: list of numbers (floats)
    """
    if len(poly) == 0:
        print "Please enter list for poly"
        assert False
        
    #define empty list to append to later
    result = []

    for i in range(1, len(poly)):
        #derivative stored to temp variable
        temp = poly[i] * i
        #turn value into float
        temp = temp/1.0
        result.append(temp)

    #print result
    return result

#test variables
##poly = [-13.39, 0.0, 17.5, 3.0, 1.0]
##compute_deriv(poly)
        
  
def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a list containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = [-13.39, 0.0, 17.5, 3.0, 1.0]    # - 13.39 + 17.5x^2 + 3x^3 + x^4
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [0.80679075379635201, 8]
    >>> poly = [1, 9, 8]
    >>> x_0 = -3
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    [-1.0000079170005467, 6]

    poly: list of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: list [float, int]
    """
    #define initial variables
    iteration = 0
    guess = x_0
    result = 1
    deriv = compute_deriv(poly)

    #loop that uses Newton's methond to iterate for poly root
    while abs(result) > epsilon:
        iteration += 1
        #checks how close guess is to 0 
        result = evaluate_poly(poly, guess)
        #new guess generated through Newton's equation
        guess = guess - (evaluate_poly(poly, guess)/evaluate_poly(deriv, guess))
        
    return guess, iteration
        
#test variables
##poly = [-13.39, 0.0, 17.5, 3.0, 1.0]
##x_0 = 0.1
##epsilon = 0.0001
##
##compute_root(poly, x_0, epsilon)
