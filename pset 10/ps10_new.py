# 6.00 Problem Set 10 Spring 2012
#
# Name: 
# Collaborators:
# Time spent:

import pylab
import random
import time

'''
Begin helper code
'''

class EventTime(object):
    """
    Represents the time for a weekly recurring event.
    """
    def __init__(self, timeStr):
        """
        Initialize a EventTime instance from the string. The input
        string needs to be of the form <dayOfWeek><times>, where
        dayOfWeek is a string that represents the days of the week the
        event occurs, with each letter being either M, T, W, R, F (e.g., MWF),
        and times is a two character digit from 00 to 23 that represents
        the hour of the day the event happens (e.g., 09).
        """
        assert isinstance(timeStr, str) and len(timeStr) <= 7 and \
               timeStr[-1].isdigit() and timeStr[-2].isdigit()
        self.time = int(timeStr[-2:])
        self.daysOfWeek = timeStr[:-2]
        assert self.time >= 0 and self.time <= 23
        assert False not in [c in 'MTWRF' for c in self.daysOfWeek]

    def getTime(self):
        """
        Gets the hour that the event happens.
        
        Returns: an integer from 0 to 23
        """
        return self.time

    def getDaysOfWeek(self):
        """
        Gets the days of the week that the event happens.
        
        Returns: a string made up with letters MTWRF
        """
        return self.daysOfWeek

    def conflict(self, other):
        """
        Checks if the passed in EventTime instance other is in conflict
        with the current instance. Two EventTime instances are in conflict
        if any occurence of one of the EventTime coincidences with
        some occurence of the other EventTime instance.
        returns: True if the two EventTime instances conflict with each other,
        False otherwise.
        """
        if not isinstance(other, EventTime):
            return False
        dayConflict = True in [d in other.daysOfWeek for d in self.daysOfWeek]
        return dayConflict and other.time == self.time

    def __str__(self):
        return self.daysOfWeek + ' ' + str(self.time)

    def __cmp__(self, other):
        if not isinstance(other, EventTime):
            raise NotImplementedError
        if self.time == other.time:
            return cmp(self.daysOfWeek, other.daysOfWeek)
        else: # the times are not equal
            return cmp(self.time, other.time)
        
    def __hash__(self):
        return hash(self.time) + hash(self.daysOfWeek)
    

def printSubjects(subjects, sortOutput=True):
    """
    Pretty-prints a list of Subject instances using the __str__ method
    of the Subject class.

    Parameters:
    subjects: a list of Subject instances to be printed
    sortOutput: boolean that indicates whether the output should be sorted
    according to the lexicographic order of the subject names
    """
    if sortOutput:
        subjectCmp = lambda s1, s2: cmp(s1.getName(), s2.getName())
        sortedSubjects = sorted(subjects, cmp=subjectCmp)
    else:
        sortedSubjects = subjects
        
    print 'Course\tValue\tWork\tTime\n======\t=====\t====\t====\n'
    totalValue, totalWork = 0, 0
    for subject in sortedSubjects:
        print subject
        totalValue += subject.getValue()
        totalWork += subject.getWork()

    print '\nNumber of subjects: %d\nTotal value: %d\nTotal work: %d\n' % \
          (len(subjects), totalValue, totalWork)
'''
End Helper Code
'''

class Subject(object):
    """
    A class that represents a subject.
    """
    def __init__(self, name, value, work, time):
        """
        Initializes a Subject instance.

        Parameters:
        name: a string that represents the name of the subject
        value: an integer that represents the value for the subject
        work: an integer that represents the amount of work for the subject
        time: an EventTime instance that represents when the subject meets
        """
        # TODO
        raise NotImplementedError
        
    def getName(self):
        """
        Gets the name of the subject.

        Returns: a string that represents the name of the subject
        """
        # TODO
        raise NotImplementedError
    
    def getValue(self):
        """
        Gets the value of the subject.
        
        Returns: an integer that represents the value of the subject
        """
        # TODO
        raise NotImplementedError

    def getWork(self):
        """
        Gets the amount of work for the subject.

        Returns: an integer that represents the work amount of the subject
        """
        # TODO
        raise NotImplementedError

    def getTime(self):
        """
        Gets the hours and days of the week that the subject meets.

        Returns: an EventTime instance that represents when the subject meets
        """
        # TODO
        raise NotImplementedError

    def conflict(self, subjectList):
        """
        Checks whether any subjects in the passed in list conflicts in
        time with the current subject instance.

        Parameters:
        subjectList: a list of Subject instances to check conflicts against

        Returns:
        True if current instance conflicts with any subjects in the list,
        and False otherwise
        """
        # TODO
        raise NotImplementedError

    def __str__(self):
        """
        Generates the string representation of the Subject class.

        Returns:
        a string of the form <subject name>\t<value>\t<work>\t<times of the day>
        where \t is the tab character, and <times of the day> is the
        string representation when the subject meets
        """
        # TODO
        raise NotImplementedError


def loadSubjects(filename):
    """
    Loads in the subjects contained in the given file. Assumes each line of
    the file
    is of the form "<subject name>,<value>,<work>,<times of the week>" where
    each field is separated by a comma.

    Parameter:
    filename: name of the data file as a string

    Returns:
    a list of Subject instances, each representing one line from the data file
    """
    # TODO
    raise NotImplementedError


class SubjectAdvisor(object):
    """
    An abstract class that represents all subject advisors.
    """
    
    def pickSubjects(self, subjects, maxWork):
        """
        Pick a set of subjects from the subjects list such that the value of
        the picked set is maximized, with the constraint that the total amount
        of work of the picked set needs to be <= maxWork. To be implemented
        by subclasses.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on

        Returns:
        a list of Subject instances that are chosen to take
        """
        raise NotImplementedError('Should not call SubjectAdvisor.pickSubjects!')

    def getName(self):
        """
        Gets the name of the advisor. Useful for generating plot legends. To be
        implemented by subclasses.

        Returns:
        A string that represents the name of this advisor
        """
        raise NotImplementedError('Should not call SubjectAdvisor.getName!')


def cmpValue(subject1, subject2):
    """
    A comparator function for two subjects based on their values. To be used
    by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has more value than subject2, 1 if subject1 has less value
    than subject2, 0 otherwise
    """
    # TODO
    raise NotImplementedError

def cmpWork(subject1, subject2):
    """
    A comparator function for two subjects based on their amount of work.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has more less than subject2, 1 if subject1 has more work
    than subject2, 0 otherwise
    """
    # TODO
    raise NotImplementedError

def cmpRatio(subject1, subject2):
    """
    A comparator function for two subjects based on their value to work ratio.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has higher value to work ratio than subject2, 1 if subject1
    has lower value to work ratio than subject1, 0 otherwise
    """
    # TODO
    raise NotImplementedError

class GreedyAdvisor(SubjectAdvisor):
    """
    An advisor that picks subjects based on a greedy algorithm.
    """
    
    def __init__(self, comparator):
        """
        Initializes a GreedyAdvisor instance.

        Parameter:
        comparator: a comparator function, either one of cmpValue, cmpWork,
                    or cmpRatio
        """
        # TODO
        raise NotImplementedError

    def pickSubjects(self, subjects, maxWork):
        """
        Picks subjects to take from the subjects list using a greedy algorithm,
        based on the comparator function that is passed in during
        initialization.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on

        Returns:
        a list of Subject instances that are chosen to take
        """
        # TODO
        raise NotImplementedError

    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Greedy"


class BruteForceAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a BruteForceAdvisor instance.
        """
        # TODO
        raise NotImplementedError

    def pickSubjects(self, subjects, maxWork):
        """
        Pick subjects to take using brute force. Use recursive backtracking
        while exploring the list of subjects in order to cut down the number
        of paths to explore, rather than exhaustive enumeration
        that evaluates every possible list of subjects from the power set.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on

        Returns:
        a list of Subject instances that are chosen to take
        """
        # TODO
        raise NotImplementedError

    def getName(self):
        """
        Gets the name of the advisor. 

        Returns:
        A string that represents the name of this advisor
        """
        return "Brute Force"

class MemoizingAdvisor(SubjectAdvisor):

    def __init__(self):
        """
        Initializes a MemoizingAdvisor instance.
        """
        # TODO
        raise NotImplementedError

    def pickSubjects(self, subjects, maxWork):
        """
        Pick subjects to take using memoization. Similar to
        BruteForceAdvisor except that the intermediate results are
        saved in order to avoid re-computation of previously traversed
        subject lists.

        Parameters:
        subjects: list of Subject instances to choose from, each subject
                  can be chosen at most once
        maxWork: maximum amount of work the student is willing to take on

        Returns:
        a list of Subject instances that are chosen to take
        """
        # TODO
        raise NotImplementedError

    def getName(self):
        """
        Gets the name of the advisor.

        Returns:
        A string that represents the name of this advisor
        """
        return "Memoizing"


def measureTimes(filename, maxWork, subjectSizes, numRuns):
    """
    Compare the time taken to pick subjects for each of the advisors
    subject to maxWork constraint. Run different trials using different number
    of subjects as given in subjectSizes, using the subjects as loaded
    from filename. Choose a random subject of subjects for each trial.
    For instance, if subjectSizes is the list [10, 20, 30], then you should
    first select 10 random subjects from the loaded subjects, then run them
    through the three advisors using maxWork for numRuns times, measuring
    the time taken for each run, then average over the numRuns runs. After that,
    pick another set of 20 random subjects from the loaded subjects,
    and run them through the advisors, etc. Produce a plot afterwards
    with the x-axis showing number of subjects used, and y-axis showing
    time. Be sure you label your plots.

    After plotting the results, answer this question:
    What trend do you observe among the three advisors?
    How does the time taken to pick subjects grow as the number of subject
    used increases? Why do you think that is the case? Include the answers
    to these questions in your writeup.
    """
    # TODO
    raise NotImplementedError
            
            
