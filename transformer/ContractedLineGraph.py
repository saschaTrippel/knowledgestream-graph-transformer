import numpy as np
import math

class ContractedLineGraph:
    def __init__(self, adjacency, numberOfPredicates:int):
        # List of assertions in the form (subjectID, objectID, predicateID)
        # as generated by GraphTransformer
        self.adjacency = adjacency
        self.numberOfPredicates = numberOfPredicates
        
    def generateClg(self):
        """
        Generate a contracted line graph (clg) out of the graph provided
        as list of assertions in self.adjacency.
        """

        self.clg = np.eye(self.numberOfPredicates, self.numberOfPredicates)
        for i in range(len(self.adjacency)-1):
            for j in range(i+1, len(self.adjacency)):
                fact1 = self.adjacency[i]
                fact2 = self.adjacency[j]
                if self._containSameResource(fact1, fact2):
                    self.clg[fact1[2], fact2[2]] += 1
                    self.clg[fact2[2], fact1[2]] += 1
                    
    def generateTfIdf(self):
        self.tfIdf = np.eye(self.numberOfPredicates, self.numberOfPredicates)
        for i in range(self.numberOfPredicates):
            for j in range(i+1, self.numberOfPredicates):
                score = self._calculateTfIdf(i, j)
                self.tfIdf[i, j] = score
                self.tfIdf[j, i] = score
    
    def saveTfIdf(self):
        pass
    
    def _calculateTfIdf(self, ri, rj):
        """
        C'(ri, rj, R) = log(1 + Cij) * log(R / |{ri | Cij > 0}|)
        R is the number of predicates
        """
        factor1 = math.log(1 + self.clg[ri, rj])
        factor2 = math.log(self.numberOfPredicates / self._countCoOccurences(ri))
        return factor1 * factor2
        
    def _countCoOccurences(self, ri):
        counter = 0
        for j in range(self.numberOfPredicates):
            if self.clg[ri, j] > 0:
                counter += 1
        return counter 
                
    def _containSameResource(self, fact1, fact2):
        return (fact1[0] == fact2[0] or fact1[0] == fact2[1]
            or fact1[1] == fact2[0] or fact1[1] == fact2[1])
