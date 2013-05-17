# 6.00 Problem Set 10 Spring 2012
#
# Name: Jorge Amaya
# Collaborators: none
# Time spent: 9:00

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
        self.name = name
        self.value = value
        self.work = work
        self.time = time
        
    def getName(self):
        """
        Gets the name of the subject.

        Returns: a string that represents the name of the subject
        """
        return self.name
    
    def getValue(self):
        """
        Gets the value of the subject.
        
        Returns: an integer that represents the value of the subject
        """
        return self.value

    def getWork(self):
        """
        Gets the amount of work for the subject.

        Returns: an integer that represents the work amount of the subject
        """
        return self.work

    def getTime(self):
        """
        Gets the hours and days of the week that the subject meets.

        Returns: an EventTime instance that represents when the subject meets
        """
        return self.time

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
        for subject in subjectList:
             if self.time.conflict(subject.getTime()):
                 return True
        return False

    def __str__(self):
        """
        Generates the string representation of the Subject class.

        Returns:
        a string of the form <subject name>\t<value>\t<work>\t<times of the day>
        where \t is the tab character, and <times of the day> is the
        string representation when the subject meets
        """
        
        return "%s\t%s\t%s\t%s\t" % (self.name, self.value, self.work, self.time)


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
    txtFile = open(filename)
    subjectList = []

    for line in txtFile:
        each = line.split(',')

        name = each[0]
        value = int(each[1])
        work = int(each[2])
        time = EventTime(each[3].strip('\n').strip('\r'))
       
        subject = Subject(name, value, work, time)
        subjectList.append(subject)

    txtFile.close()
    return subjectList


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
    return subject1.getValue() - subject2.getValue()

def cmpWork(subject1, subject2):
    """
    A comparator function for two subjects based on their amount of work.
    To be used by the GreedyAdvisor class.

    Paramters:
    subject1, subject2: two Subject instances

    Returns:
    -1 if subject1 has less work than subject2, 1 if subject1 has more work
    than subject2, 0 otherwise
    """
    return subject1.getWork() - subject2.getWork()

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
    s1 = subject1.getValue() / subject1.getWork()
    s2 = subject2.getValue() / subject2.getWork()

    return s1 - s2


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
        self.comparator = comparator
        

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
        work = 0
        subjectList = []
        subjectsCopy = sorted(subjects, cmp=self.comparator, reverse=True)
    
        for subject in subjectsCopy:
            if work + subject.getWork() <= maxWork and not subject.conflict(subjectList):
                work += subject.getWork()
                subjectList.append(subject)
        
        return subjectList

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
        results = self.maxVal(subjects, maxWork)
        return list(results[1])


    def maxVal(self, subjects, maxWork):
        if subjects == [] or maxWork == 0:
            result = (0, ())
            
        elif subjects[0].getWork() > maxWork:
            result = self.maxVal(subjects[1:], maxWork)
        else:
            nextItem = subjects[0]
            
            #LEFT
            withVal, withToTake = self.maxVal(subjects[1:], maxWork - nextItem.getWork())
            withVal += nextItem.getValue()
                
            #RIGHT
            withoutVal, withoutToTake = self.maxVal(subjects[1:], maxWork)
            
            #CHOOSE BETTER
            if withVal >= withoutVal and not nextItem.conflict(withToTake):
                result = (withVal, withToTake + (nextItem,))
            else:
                result = (withoutVal, withoutToTake)
                
        return result

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
        self.memo = {}
        
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
        results = self.fastSolve(subjects, maxWork, memo=None)
        return list(results[1])
        
    def fastSolve(self, subjects, maxWork, memo):
        if memo == None:
            memo = {}
            
        timeCheck = []
        for each in subjects:
            timeCheck.append(each.getTime())
        timeCheckTup = tuple(sorted(timeCheck))
        
        #check if in memo        
        if (len(subjects), maxWork, timeCheckTup) in memo:
            return memo[len(subjects), maxWork, timeCheckTup]
            
        elif subjects == [] or maxWork == 0:
            result = (0, ())
            
        elif subjects[0].getWork() > maxWork:
            result = self.fastSolve(subjects[1:], maxWork, memo)
        else:
            nextItem = subjects[0]
            
            #LEFT
            withVal, withToTake = self.fastSolve(subjects[1:], maxWork - nextItem.getWork(), memo)
            withVal += nextItem.getValue()
                
            #RIGHT
            withoutVal, withoutToTake = self.fastSolve(subjects[1:], maxWork, memo)
            
            #CHOOSE BETTER
            if withVal >= withoutVal and not nextItem.conflict(withToTake):
                result = (withVal, withToTake + (nextItem,))
            else:
                result = (withoutVal, withoutToTake)

        time = []
        for each in result[1]:
            time.append(each.getTime())
        timeTup = tuple(sorted(time))

        memo[(len(subjects), maxWork, timeTup)] = result
        return result

    
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
    loadSub = loadSubjects(filename)

    def selectRandomSubjects(num, subjects):
        '''returns list of n # of random subjects'''
        return random.sample(subjects, num)
    
    def Advisors(subjects, maxWork):
        '''times each advisor'''
        times = []
        start = time.time()
        greedy = GreedyAdvisor(cmpRatio).pickSubjects(subjects, maxWork)
        end = time.time()
        greedyTime = end - start
        
        start = time.time()
        brute = BruteForceAdvisor().pickSubjects(subjects, maxWork)
        end = time.time()
        bruteTime = end - start
        
        start = time.time()
        memoiz = MemoizingAdvisor().pickSubjects(subjects, maxWork)
        end = time.time()
        memoTime = end - start

        return [greedyTime, bruteTime, memoTime]
        
    def eachRun(numRuns, loadSub, num):
        '''makes 5 runs of each subjectSize'''
        results = []
        subjects = selectRandomSubjects(num, loadSub)
       
        for value in range(numRuns):
            run = Advisors(subjects, maxWork)
            if results == []:
                for each in run:
                    results.append(each)
            else:
                for i in range(3):
                    results[i] += run[i]

        for i in range(3):
            results[i] /= numRuns
            
        return results
    

    def pylabPlot(numRuns, subjectSizes):
        '''creates plot of 3 advisor implementatioins'''
        greedy = []
        brute = []
        memo = []

        #run each version of subjectSize, 10, 20...
        for num in subjectSizes:
            results = eachRun(numRuns, loadSub, num)
            greedy.append(results[0])
            brute.append(results[1])
            memo.append(results[2])

        pylab.title("3 Different Advisor Implementations")
        pylab.xlabel("How many Subject Choices Initialy")
        pylab.ylabel("How long each Advisor takes (seconds)")
        
        pylab.plot(subjectSizes, greedy, label='greedy')
        pylab.plot(subjectSizes, brute, label='brute force')
        pylab.plot(subjectSizes, memo, label='memoization')

        pylab.legend(loc="best")

        pylab.show()

    pylabPlot(numRuns, subjectSizes)
    
filename = "subjects.txt"
subjectSizes = [10, 20, 30, 40, 50]
maxWork = 40
numRuns = 5

##comment out to not run plot generation
##measureTimes(filename, maxWork, subjectSizes, numRuns)    
            

