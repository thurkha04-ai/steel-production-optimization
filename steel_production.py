#import gurobi stuff
import gurobipy as gp
from gurobipy import GRB

# Create raw metals, alloys, elements

I = [1,2,3,4,5]
J = ['A','B']
E = ['Fe','C','Cr','Ni','Mn']

# availability of metals 
availability = {1: 500, 2: 50, 3:3000, 4:900,  5: 200}

# cost of raw metals 
cost = {1:400, 2:500, 3:650, 4:800,5: 1500}

# alloy price/revenue  (FIX: B must be a string)
revenue = {'A': 2200, 'B': 1200}

# percentage of elements 
elemsp = {
    1: (96, 3.5, 0, 0, 0.5),
    2: (91, 1.5, 2, 1.5, 4),
    3: (99.75, 0.05, 0, 0, 0.2),
    4: (60, 0.5, 38, 0, 1.5),
    5: (55.5, 0.1, 0, 44, 0.5)
}

# element bounds for alloys (FIX: syntax error in Ni + B dictionary)
bounds = {
    'A': {'Fe': (69,71), 'C': (None,0.3), 'Cr':(18,20), 'Ni':(8,10), 'Mn':(None,1)},
    'B': {'Fe': (90,95), 'C':(0.05,0.25), 'Cr':(None,3), 'Ni':(None,3), 'Mn': (0.5,2)}
}

# Create a model and variables
m = gp.Model("SteelProduction")

x = m.addVars(J, name="x", lb=0)
y = m.addVars(I, name="y", lb=0)
z = m.addVars(I, J, name="z", lb=0)

# Objective function
m.setObjective(
    (2200 * x['A'] + 1200 * x['B'])
    - (400 * y[1] + 500 * y[2] + 650 * y[3] + 800 * y[4] + 1500 * y[5]),
    GRB.MAXIMIZE
)

# Constraint for availability (split = y)
m.addConstr(z[1, 'A'] + z[1, 'B'] == y[1])
m.addConstr(z[2, 'A'] + z[2, 'B'] == y[2])
m.addConstr(z[3, 'A'] + z[3, 'B'] == y[3])
m.addConstr(z[4, 'A'] + z[4, 'B'] == y[4])
m.addConstr(z[5, 'A'] + z[5, 'B'] == y[5])

# Upper bounds on available metals
m.addConstr(y[1] <= 500)
m.addConstr(y[2] <= 50)
m.addConstr(y[3] <= 3000)
m.addConstr(y[4] <= 900)
m.addConstr(y[5] <= 200)

# Alloy = sum of metals used
m.addConstr(z[1, 'A'] + z[2, 'A'] + z[3, 'A'] + z[4, 'A'] + z[5, 'A'] == x['A'])
m.addConstr(z[1, 'B'] + z[2, 'B'] + z[3, 'B'] + z[4, 'B'] + z[5, 'B'] == x['B'])

# Fe (A)
m.addConstr(96*z[1,'A'] + 91*z[2,'A'] + 99.75*z[3,'A'] + 60*z[4,'A'] + 55.5*z[5,'A'] >= 69*x['A'])
m.addConstr(96*z[1,'A'] + 91*z[2,'A'] + 99.75*z[3,'A'] + 60*z[4,'A'] + 55.5*z[5,'A'] <= 71*x['A'])

# C (A)
m.addConstr(3.5*z[1,'A'] + 1.5*z[2,'A'] + 0.05*z[3,'A'] + 0.5*z[4,'A'] + 0.1*z[5,'A'] <= 0.3*x['A'])

# Cr (A)
m.addConstr(2*z[2,'A'] + 38*z[4,'A'] >= 18*x['A'])
m.addConstr(2*z[2,'A'] + 38*z[4,'A'] <= 20*x['A'])

# Ni (A)
m.addConstr(1.5*z[2,'A'] + 44*z[5,'A'] >= 8*x['A'])
m.addConstr(1.5*z[2,'A'] + 44*z[5,'A'] <= 10*x['A'])

# Mn (A)
m.addConstr(0.5*z[1,'A'] + 4*z[2,'A'] + 0.2*z[3,'A'] + 1.5*z[4,'A'] + 0.5*z[5,'A'] <= 1*x['A'])

# Fe (B)
m.addConstr(96*z[1,'B'] + 91*z[2,'B'] + 99.75*z[3,'B'] + 60*z[4,'B'] + 55.5*z[5,'B'] >= 90*x['B'])
m.addConstr(96*z[1,'B'] + 91*z[2,'B'] + 99.75*z[3,'B'] + 60*z[4,'B'] + 55.5*z[5,'B'] <= 95*x['B'])

# C (B)
m.addConstr(3.5*z[1,'B'] + 1.5*z[2,'B'] + 0.05*z[3,'B'] + 0.5*z[4,'B'] + 0.1*z[5,'B'] >= 0.05*x['B'])
m.addConstr(3.5*z[1,'B'] + 1.5*z[2,'B'] + 0.05*z[3,'B'] + 0.5*z[4,'B'] + 0.1*z[5,'B'] <= 0.25*x['B'])

# Cr (B)
m.addConstr(2*z[2,'B'] + 38*z[4,'B'] <= 3*x['B'])

# Ni (B)
m.addConstr(1.5*z[2,'B'] + 44*z[5,'B'] <= 3*x['B'])

# Mn (B)
m.addConstr(0.5*z[1,'B'] + 4*z[2,'B'] + 0.2*z[3,'B'] + 1.5*z[4,'B'] + 0.5*z[5,'B'] >= 0.5*x['B'])
m.addConstr(0.5*z[1,'B'] + 4*z[2,'B'] + 0.2*z[3,'B'] + 1.5*z[4,'B'] + 0.5*z[5,'B'] <= 2*x['B'])

# update model
m.update()

# Save model
m.write('steel_model.lp')

# Optimize
m.optimize()
print(m.Status)
