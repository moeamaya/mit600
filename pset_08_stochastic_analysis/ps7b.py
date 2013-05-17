# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name: Jorge Amaya
# Collaborators: none
# Time: 13:00

#from ps7b_precompiled_27 import *
import numpy
import random
import pylab
import math

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        
    def probabilityChoice(self, probPercent):
        """
        probPercent: probability (float) 0 -> 1
        returns True or False depending on input probability
        """
        
        probability = int((1.0/probPercent))
        probIndex = range(probability)
        probChoice = random.choice(probIndex)
        
        return probChoice == 0
        
    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """        
        return self.probabilityChoice(self.clearProb)      
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        prob = self.maxBirthProb * (1 - popDensity)
        if self.probabilityChoice(prob):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            pass
            #result = NoChildException()
            #return result
                

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop
        self.totalPop = len(self.viruses)

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return self.totalPop       

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        def survive():
            virusCount = self.viruses[:]
            for virus in virusCount:
                if virus.doesClear():
                   self.viruses.remove(virus)
        
        def populationDensity():
            self.totalPop = len(self.viruses)

        def reproduceOrNot():
            virusCount = self.viruses[:]
            for virus in virusCount:        
                popDen = (float(self.totalPop) / self.maxPop)
                if popDen < 1:
                    #reproduce under given probability
                    newVir = virus.reproduce(popDen)
                    if newVir:
                        self.viruses.append(newVir)               

        survive()
        reproduceOrNot()

        return len(self.viruses)
#
# PROBLEM 2
#

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """    
    def listViruses(numViruses):
        """creates list of instantiated simple virus objects"""
        viruses = []
        for i in range(numViruses):
            vir = SimpleVirus(maxBirthProb, clearProb)
            viruses.append(vir)
        return viruses
    
    def simTimeStep(numVir):
        """simulates single run of patient update"""
        viruses = listViruses(numVir)
        patient = Patient(viruses, maxPop)
        
        numVir = patient.update()
        return numVir
    
    def simTrials(numTrials):
        """
        Returns final virus count in a dictionary with each time step
        as key and virus count as value in a list
        """
        numVir = numViruses
        dictTrials = {}
        timeSteps = 300
        #generate dictionary with lists as value
        for i in range(timeSteps):
            dictTrials[i] = list()
        #trial loop    
        for i in range(numTrials):
            numVir = numViruses
            #one 300 time step loop
            for j in range(timeSteps):
                numVir = simTimeStep(numVir)
                dictTrials[j].append(numVir)

        return dictTrials

    def meanResults():
        avg = []
        dictTrials = simTrials(numTrials)
        #make list of avg virus count, indexed at each time step
        for i in range(len(dictTrials)):
            stepAvg = sum(dictTrials[i]) / len(dictTrials[i])
            avg.append(stepAvg)
        return avg
    
    def showPlot(title, x_label, y_label):
        """
        Produce a plot of average virus counts at each time step
        """
        results = meanResults()
        time = range(len(results))
        
        pylab.plot(results, time)
        pylab.title(title)
        pylab.xlabel(x_label)
        pylab.ylabel(y_label)
        pylab.show()


#####################################################
#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        return self.resistances[drug]
    
    def reverseBoolean(self, boo):
        """turns True to False or False to True"""
        if True:
            return False
        return True

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        resDrug = []
        for drug in activeDrugs:
            resDrug.append(self.isResistantTo(drug))
        #only reproduce if resistant
        if all(resDrug):
            prob = self.maxBirthProb * (1 - popDensity)
            #reproduce under given probability
            if self.probabilityChoice(prob):
                #see if child will have same resistance
                if self.probabilityChoice(self.mutProb):
                    for drug in self.resistances:
                        self.reverseBoolean(self.resistances[drug])
                return ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
        else:
            pass
            #result = NoChildException()
            #return result
            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.totalPop = len(self.viruses)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        total = 0
        for virus in self.viruses:
            resDrug = []
            #list of boolean values
            for drug in drugResist:
                resDrug.append(virus.isResistantTo(drug))
                               
            if all(resDrug):
                total += 1
                
        return total

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        def survive():
            virusCount = self.viruses[:]
            for virus in virusCount:
                if virus.doesClear():
                   self.viruses.remove(virus)
        
        def populationDensity():
            self.totalPop = len(self.viruses)

        def reproduceOrNot():
            virusCount = self.viruses[:]
            for virus in virusCount:        
                popDen = (float(self.totalPop) / self.maxPop)
                if popDen < 1:
                    newVir = virus.reproduce(popDen, self.getPrescriptions())
                    #if virus reproduces add to virus list
                    if newVir:
                        self.viruses.append(newVir)               

        survive()
        reproduceOrNot()

        return len(self.viruses)       

#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a list of drugs that each ResistantVirus is resistant to
                 (a list of strings, e.g., ['guttagonol'])
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    def listViruses(numViruses):
        """creates list of instantiated simple virus objects"""
        viruses = []
        for i in range(numViruses):
            vir = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(vir)
        return viruses
    
    def simTimeStep(numVir):
        """simulates single run of patient update"""
        viruses = listViruses(numVir)
        patient = TreatedPatient(viruses, maxPop)

        numVir = patient.update()
        return numVir

    def simTimeStepDrug(numVir):
        """simulates single run of patient update with drug"""
        drugList = []
        for drug in resistances:
            drugList.append(drug)
        
        viruses = listViruses(numVir)
        patient = TreatedPatient(viruses, maxPop)
        #administer drug
        patient.addPrescription(drugList[0])

        numVir = patient.update()
        return numVir
        
    def simTrials(numTrials):
        """
        Returns final virus count in a dictionary with each time step
        as key and virus count as value in a list
        """
        numVir = numViruses
        dictTrials = {}
        timeSteps = 300
        
        for i in range(timeSteps):
            dictTrials[i] = list()
            
        for i in range(numTrials):
            #reset each trial to orginal starting virus count
            numVir = numViruses
            for j in range(timeSteps):
                #split the timeSteps to different functions
                if j > 150:
                    numVir = simTimeStepDrug(numVir)
                    dictTrials[j].append(numVir)
                else:
                    numVir = simTimeStep(numVir)
                    dictTrials[j].append(numVir)

        return dictTrials

    def meanResults():
        avg = []
        dictTrials = simTrials(numTrials)
        #take all values at each step and make list of averages
        for i in range(len(dictTrials)):
            stepAvg = sum(dictTrials[i]) / len(dictTrials[i])
            avg.append(stepAvg)
        return avg
    

#simulationWithDrug(100, 1000, 0.1, 0.05, {"guttagonol": False}, 0.005, 100)
