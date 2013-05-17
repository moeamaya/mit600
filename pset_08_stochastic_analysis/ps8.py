# 6.00 Problem Set 8
#
# Name: Moe Amaya
# Collaborators: None
# Time: 3:00

import numpy
import random
import pylab
#from ps7b import *
from ps7b_precompiled_27 import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb, clearProb,
                               resistances, mutProb, numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: maximum reproduction probability (a float between 0-1)        
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
        #delay = [0, 75, 150, 300]
        #change to print each timestep
        delay = [300]
        
        for num in delay:
            dictTrials[num] = list()
            
        for num in delay:
            for i in range(numTrials):
                #reset each trial to orginal starting virus count
                numVir = numViruses
                #allow virus population to grow for 0...300 timesteps
                for time in range(num):
                    numVir = simTimeStep(numVir)
                #administer Guttagonol for 150 timesteps
                for i in range(150):
                    numVir = simTimeStepDrug(numVir)
                #store all the trials into a dictionary where key = timestep#
                dictTrials[num].append(numVir)
                
        return dictTrials

    def showPlot(title, x_label, y_label):
        """
        Produce a plot of average virus counts at each time step
        """
        results = simTrials(numTrials)
        #change to print each timestep
        plot = results[300]
        
        pylab.hist(plot)
        pylab.title(title)
        pylab.xlabel(x_label)
        pylab.ylabel(y_label)
        pylab.show()

    showPlot("300-Timestep Delayed Delivery of Guttagonol", "Final virus count", "How many trials")

simulationDelayedTreatment(100, 1000, 0.1, 0.05, {"guttagonol": False}, 0.005, 50)
