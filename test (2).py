import solution

fh = open('PUB1.txt', 'r')

a = solution.MDProblem(fh)

print(a.solve())
fh.close()