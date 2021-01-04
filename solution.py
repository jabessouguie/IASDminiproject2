import probability

class MDProblem :
    
    def __init__ (self , fh):
        
        # diseases will be the nodes
        self.diseases = []
        
        
        
        dataFile = open(fh, 'r')
        
        for line in dataFile:
    
            # split input string by spaces
            rawData = line.split(" ")
    
            # last string will end in /n, remove it here
            rawData[-1] = rawData[-1][:-1]
            
            # last project had malformed inputs, fix lowercases here
            rawData[0] = rawData[0].upper()
            
            # read the disease list and 
            if(rawData[0] == 'D'):
                for disease in rawData[1:]:
                    self.diseases.append(disease)
                
        
        return ()

    def solve ( self ):
    # Place here your code to determine the maximum likelihood
    # solution returning the solution disease name and likelihood .
    # Use probability . elimination_ask () to perform probabilistic
    # inference .
        return ( disease , likelihood )
