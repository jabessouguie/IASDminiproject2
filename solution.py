import probability


class MDProblem:
    
    
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
            elif(line[0].upper() == "S"):
                for i in range(1, len(line)-1):
                    for other in line[i:]:
                        # edges format:
                        # [ Symptom , [disease, disease] ]
                        self.edges.append( [ line[1], [line[i], other]] )
                        
            # Check for line started with E
            # syntax:
            #   E [test] [disease] [true positive] [false positive]
            elif(line[0].upper() == "S"):
                self.test_dict[line[1]] = {'disease' : line[2], 'TPR' : line[3], 'FPR' : line[4]}
            
            # Check for line started with M
            # syntax:
            #   M [test] [result] [test] [result] ... [test] [result]
            elif(line[0].upper() == "M"):
                for i in range(1, len(line), 2):
                    self.tests_performed.append([line[i], line[i+1]])
            
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
    
    def __init__(self, fh):
        
        self.parseFile(fh)
        

        i = 0
        # To avoid having 2 times the same disease in the same edge

        while i < (len(edges)):
            if edges[i][0] == edges[i][1]:
                del (edges[i])
                i += 1
            else:
                i += 1
        # Taking the result of the different tests realized at different times
        measurements = []
        for i in range(0, len(tests_performed)):
            m = len(tests_performed[i])
            for j in range(0, m):
                measurements.append([i + 1, tests_performed[i][j][0], tests_performed[i][j][1]])

        disease = nodes
        disease_probability = {}
        present_disease = {}

        # At beginning we put the probability of having a disease at 0.5
        for i in disease:
            disease_probability[i] = 0.5

        # If the probability of having a disease if higher than 0, we consider that the patient has this disease
        for d in disease:
            if disease_probability[d] > 0:
                present_disease[d] = True

        time_length = t

        #  For each disease present
        for disease in nodes:
            n = []

            #  checking the disease sharing the same symptom
            for symptom in edges:
                if disease in symptom:
                    for other_disease in symptom:
                        if type(other_disease) == str:
                            if other_disease != disease:
                                if other_disease not in n:
                                    #  And add it to the list of its children
                                    n.append(other_disease)
            disease_neighbours[disease] = n

        # For each epoch of time, we apply the propagation rule

        for t in range(time_length - 2):
            print(t)
            # getting what tests were done at that time and what was the result for each of them
            test = tests_performed[t]

            # getting which disease were tested
            diseases_tested = [test_to_disease[k[0]] for k in test]

            # For each disease
            for d in nodes:
                # If this disease wasn't tested
                if d not in diseases_tested:

                    # We check the disease that share the same symptom
                    neighbors = disease_neighbours[d]

                    # And add it to the list of potential disease

                    potential_disease = []

                    # For every of theses diseases
                    if neighbors:
                        for n in neighbors:

                            # If it's the patient already has this disease
                            if n is disease:
                                # we add it to the list of potential
                                potential_disease.append(n)

                                # And note that the patient has another disease sharing the same symptom
                        is_here = len(potential_disease)
                    else:
                        is_here = 0

                    # if the patient has another disease sharing the same symptom
                    if is_here > 0:

                        # We put the probability of having this disease equal to propagation probability for this
                        # disease
                        disease_probability[d] = propagation_probability

                        # And the disease already present sharing the same symptom
                        for p in potential_disease:
                            if p not in diseases_tested:
                                disease_probability[p] = propagation_probability

        patient = []
        #  For each disease present
        for disease in nodes:
            d = [disease]

            #  checking the disease sharing the same symptom
            for symptom in edges:
                if disease in symptom:
                    for other_disease in symptom:
                        if type(other_disease) == str:
                            if other_disease != disease:
                                if other_disease not in d:
                                    #  And add it to the list of its children
                                    d.append(other_disease)

            #  Putting here the conditional probability(may be wrong)
            test = {True: disease_probability[disease], False: 1 - disease_probability[disease]}
            d.append(test)
            patient.append(tuple(d))

        self.bayesian_network = BayesNet(patient)
        self.present_disease = present_disease
        self.disease = nodes

    def solve(self):
        # Place here your code to determine the maximum likelihood
        # solution returning the solution disease name and likelihood .
        # Use probability . elimination_ask () to perform probabilistic
        # inference .
        bayesian_network = self.bayesian_network
        disease = self.disease
        present_disease = self.present_disease
        list_disease = {}
        for d in disease:
            list_disease[d] = True
        L = {}
        likelihood = 0

        # For every disease
        for disease in list_disease:
            # Use elimination algorithm to compute the likelihood
            L[disease] = elimination_ask(disease, present_disease, bayesian_network)[True]

        # Checking for the maximum
        for d in L.keys():
            if L[d] > likelihood:
                likelihood = L[d]
                disease = d

        # And return it
        return disease, likelihood
