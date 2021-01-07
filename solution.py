import probability as prob
from itertools import permutations

class MDProblem:
    
    

    
    def __init__(self, fh):
        
        self.parseFile(fh)
        
        self.solve()
        
        
    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .
        self.BNet = prob.BayesNet()
        evidence = {}
        
        for t in range(self.time_instants):
            inst = t+1  
            for disease in self.nodes:
                name = (disease + 't' + str(inst))
                # returnParents WORKING!!!!
                parents = self.returnParents(disease, inst)
                # returnCPT WORKING!!!!
                cpt = self.returnCPT(disease, parents,inst)
                self.BNet.add((name, parents, cpt))

            for test in self.tests_performed[t]:
                name = (test[0] + 't' + str(inst))
                test_info = self.test_dict[test[0]]
                parent = test_info[0]+'t'+str(inst)
                self.BNet.add((name, parent, test_info[1]))
                evidence[name] = test[1]
        
        print(evidence)
        print('---------------------')
        print(self.BNet)
        print('---------------------')
        print(self.BNet.variables)
        likelihood = []
        for disease in self.nodes:
            print('\n'+'trying to get likelyhood for -> '+disease+' <-\n')
            likelihood.append([disease, prob.elimination_ask(disease, evidence, self.BNet)])

        # And return it
        return disease, likelihood
    
    def returnCPT(self, disease, parents, instant):
        if(instant == 1):
            return 0.5
        else:
            cpt = {}
            cpt_len = len(parents.split())
            # check how many parents
            # I'm being smarter than I ought to, generating cpt from binary
            binrep = 2**cpt_len-1
            while(binrep >= 0):
                temp1 = []
                for i in bin(binrep)[2:]:
                    temp1.append(i)
                while(len(temp1) < cpt_len):
                    temp1.insert(0,'0')
                temp2 = []
                for t in temp1:
                    if(t == '1'):
                        temp2.append(True)
                    elif(t == '0'):
                        temp2.append(False)
                    #TODO add redundant else
                cpt_element = tuple(temp2)
                
                if(cpt_element[0]):
                    if(True in cpt_element[1:]):
                        cpt_element_prob = self.prop_const
                    else:
                        cpt_element_prob = 1
                else:
                    cpt_element_prob = 0
                
                cpt[cpt_element] = cpt_element_prob
                binrep -= 1
            '''   
            print('---------------------')
            print(disease)
            print(parents)
            print(cpt)
            print('---------------------')
            '''
            # TODO compute cpt
            #for 
            
            return cpt
        
    def returnParents(self, disease, instant):
        parents = ''
        
        if(instant != 1):
            # TODO check parents
            current = [disease+'t'+str(instant-1)]
            for e in self.edges:
                if(disease in e[1]):
                    for d in e[1]:
                        if d+'t'+str(instant-1) not in current:
                            current.append(d+'t'+str(instant-1))
                            
            
            for p in current:
                parents += ' ' + p

        return parents
    
    def parseFile(self, fh):
        
        # this is a buffer variable to hold our file data
        L = []
        
        # for each line in file, split() and append resulting list to be processed later        
        for rl in fh:
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
                self.test_dict[line[1]] = [line[2], {True : float(line[3]), False : float(line[4])}]
            
            # Check for line started with M
            # syntax:
            #   M [test] [result] [test] [result] ... [test] [result]
            elif(line[0].upper() == "M"):
                self.time_instants += 1
                tests_at_instant = []
                for i in range(1, len(line), 2):
                    if(line[i+1].upper() == "T"):
                        res = True
                    else:
                        res = False
                    tests_at_instant.append([line[i], res])
                self.tests_performed.append(tests_at_instant)
            
            # Check for line started with P
            # syntax:
            #   P [propagation constant]
            elif(line[0].upper() == "P"):
                self.prop_const = float(line[1])
            
            # Sanity check, warning for the future
            # TODO raise exception
            else:
                print("There was an unparsed line!")
                print(line)
                print("------------------------------------")
        
        return