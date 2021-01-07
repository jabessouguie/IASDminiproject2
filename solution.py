import probability as prob


class MDProblem:
    
    

    
    def __init__(self, fh):
        
        self.parseFile(fh)
        
        print(self.prop_const)
        print(self.time_instants)
        print(self.nodes)
        print(self.edges)
        print(self.tests_performed)
        print(self.test_dict)
        
        #self.solve()
        
        
    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .
        self.BNet = prob.BayesNet()
        
        for t in range(self.time_instants):
            t += 1  
            for disease in self.nodes:
                name = (disease + 't' + str(t))
                cpt = self.returnCPT(disease, t)
                parents = self.returnParents(disease, t)
                self.BNet.add(prob.BayesNode( name, parents, cpt))
                
            evidence = {}
            for test in self.tests_performed[t-1]:
                #TODO add tests to disease
                name = (test[0] + 't' + str(t))
                parents = ''
                self.BNet.add(prob.BayesNode( name, parents, cpt))
                evidence[name] = test[1]
                
            likelihood = []
            for disease in self.nodes:
                likelihood.append([disease, prob.elimination_ask(disease, evidence, self.BNet)])

        # And return it
        return disease, likelihood
    
    def returnCPT(self, disease, instant):
        if(instant == 0):
            return 0.5
        else:
            cpt = {}
            # TODO compute cpt
            return cpt
        
    def returnParents(self, disease, instant):
        parents = ''
        
        if(instant != 1):
            # TODO check parents
            a = 0
        
        return parents
    
    def parseFile(self, fh):
        
        
        f = open(fh, 'r')
        
        # this is a buffer variable to hold our file data
        L = []
        
        # for each line in file, split() and append resulting list to be processed later        
        for rl in f.readline():
            L.append(rl.split())
            
        self.processInputData(L)
            
        return
    
    def processInputData(self, data):
        
        # data variables used to create the BNet
        # using class variables is convenient
        self.prop_const = 0
        self.time_instants = 0
        self.nodes = []
        self.edges = []
        self.tests_performed = []
        self.test_dict = {}

        
        for line in data:
            
            # Check for line started by D
            # syntax:
            #   D [disease] [disease] ... [disease]
            if(line[0].upper() == "D"):
                for disease in line[1:]:
                    self.nodes.append(disease)
            
            # Check for line started with S
            # syntax:
            #   S [symptom] [disease] [disease] ... [disease]
            # TODO check edge creation logic
            # Edges already avoid duplication
            elif(line[0].upper() == "S"):
                for i in range(2, len(line)-1):
                    for other in line[i+1:]:
                        # edges format:
                        # [ Symptom , [disease, disease] ]
                        self.edges.append( [ line[1], [line[i], other]] )
                        
            # Check for line started with E
            # syntax:
            #   E [test] [disease] [true positive] [false positive]
            # For the tests we have a dictionary that returns a list:
            #       [ disease, probability.ProbDist ]
            # ProbDist is correctly initialized with values TPR and FPR that can be called directly
            elif(line[0].upper() == "E"):
                self.test_dict[line[1]] = [line[2], prob.ProbDist(line[1], {True : float(line[3]), False : float(line[4])})]
            
            # Check for line started with M
            # syntax:
            #   M [test] [result] [test] [result] ... [test] [result]
            elif(line[0].upper() == "M"):
                self.time_instants += 1
                tests_at_instant = []
                for i in range(1, len(line), 2):
                    tests_at_instant.append([line[i], line[i+1]])
                self.tests_performed.append(tests_at_instant)
            
            # Check for line started with P
            # syntax:
            #   P [propagation constant]
            elif(line[0].upper() == "P"):
                self.prop_const = line[1]
            
            # Sanity check, warning for the future
            # TODO raise exception
            else:
                print("There was an unparsed line!")
                print(line)
                print("------------------------------------")
        
        return