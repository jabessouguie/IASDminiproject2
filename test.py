import probatest

f = open('test.txt', 'r')
# reading the text file
ligne = f.readline()
nodes = []
edges = []
liste_mots = ligne.split()
L = [liste_mots]
ligne = f.readline()
while ligne:
    ligne = f.readline()
    liste_mots = ligne.split()
    L.append(liste_mots)

# getting what disease correspond to what test
test_to_disease = {}

# List of test that the patient actually performed
tests_performed = []

n = len(L)
#getting how long the process will last
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

print(tests_performed)
T = t

i = 0
# To avoid having 2 times the same disease in the same edge

while i < (len(edges)):
    if edges[i][0] == edges[i][1]:
        del (edges[i])
        i += 1
    else:
        i += 1
nodes_spec = edges
cpt = 0.25

measurements = []
for i in range(0, len(tests_performed)):
    m = len(tests_performed[i])
    for j in range(0, m):
        measurements.append([i + 1, tests_performed[i][j][0], tests_performed[i][j][1]])

patient = []
for i in range(len(tests_performed)):
    disease = test_to_disease[tests_performed[i][0][0]][0]
    d = [disease]
    for symptom in edges:
        if disease in symptom:
            for otherdisease in symptom:
                if type(otherdisease) == str:
                    if otherdisease != disease:
                        if otherdisease not in d:
                            d.append(otherdisease)
    test = {}
    test[(True, True)] = float(test_to_disease[tests_performed[i][0][0]][1])
    test[(True, False)] = float(test_to_disease[tests_performed[i][0][0]][2])
    d.append(test)

    patient.append(tuple(d))

