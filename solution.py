import probability


class MDProblem:
    def __init__(self, fh):
        f = open(fh, 'r')
        # reading the text file
        line = f.readline()
        nodes = []
        edges = []
        word_list = line.split()
        L = [word_list]
        line = f.readline()
        while line:
            line = f.readline()
            word_list = line.split()
            L.append(word_list)

        # getting what disease correspond to what test
        test_to_disease = {}
        disease_neighbours = {}

        # List of test that the patient actually performed
        tests_performed = []

        n = len(L)
        # getting how long the process will last
        t = 0
        for i in range(n - 1):

            # getting the list of node
            if L[i][0] == 'D':
                m = len(L[i])
                for j in range(1, m):
                    nodes.append(L[i][j])

            # getting the different edges
            if L[i][0] == 'S':
                m = len(L[i])
                for j in range(2, m):
                    for k in range(2, m):
                        edges.append([L[i][j], L[i][k], 0.25])

            # Associating test with disease

            if L[i][0] == 'E':
                test_to_disease[L[i][1]] = [L[i][2], L[i][3], L[i][4]]

            # getting the result of the test

            if L[i][0] == 'M':
                tests_performed_t = []
                m = len(L[i])
                for j in range(1, m):
                    if L[i][j] == 'T':
                        tests_performed_t.append([L[i][j - 1], True])
                        t += 1
                    elif L[i][j] == 'F':
                        tests_performed_t.append([L[i][j - 1], False])
                        t += 1
                tests_performed.append(tests_performed_t)

            # getting the propagation probability
            if L[i][0] == 'P':
                propagation_probability = float(L[i][1])

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
