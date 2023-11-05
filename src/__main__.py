'''
This program is created with the purpose of solving any 5x5 nonogram (with a solution)
using propositional logic applied to object-oriented programming. The solution of the
nonogram will be displayed using the Matplotlib library.
'''

from itertools import combinations


from __init__ import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from types import MethodType
import random





def write_cells(self, literal):
    
    '''
    Description: method functions as a translator for compiled propositional language represented as propositional letters
    into the standard language.
    '''
    
    if '-' in literal:
        atomo = literal[1:]
        neg = ' No'
    else:
        atomo = literal
        neg = ''
    x, y  = self.inv(atomo)
    return f"La casilla ({x},{y}) {neg} esta rellena"






class Nanogram:
    '''
    Description: The Nanogram class is responsible for creating objects that represent unique nonograms with
    specific initial conditions, each designed to solve various types of puzzles.
    The initial conditions consist of the numbers that would typically appear above
    each row and column in a nonogram. These numbers indicate the count of filled cells
    in the corresponding row/column.
    
    Class representation for solving the Nonogram puzzle.
    Reference: https://nonogramas.relaxweb.es/nonograma/96041    
    '''



    def __init__(self):

        self.RenC                  =  Descriptor([5,5])
        self.RenC.write            =  MethodType(write_cells, self.RenC)
        self.initial_conditions    =  {x : None for x in range(10)}

        # Initial conditions for the rows
        self.initial_conditions[0] =  1
        self.initial_conditions[1] =  1
        self.initial_conditions[2] =  2
        self.initial_conditions[3] =  [2,1]
        self.initial_conditions[4] =  2

        # Initial conditions for the columns
        self.initial_conditions[5] =  2
        self.initial_conditions[6] =  3
        self.initial_conditions[7] =  1
        self.initial_conditions[8] =  [1,1]
        self.initial_conditions[9] =  1



        self.rules = []

#

    def rules_classifier(self):
        '''
        This method is responsible for selecting the 10 rules needed to solve the Nonogram puzzle
        based on the given initial conditions.
        Upon initialization, self.rules = []
        At the end of this process, self.rules will contain 10 rules which form the core of the solution.
        '''


        for x in self.initial_conditions.keys():
            '''
            If the condition is a number, it will simply append the rule to self.rules based on the numeric value
            of the initial condition for that row and/or column.
            '''

            try:
                rules_functions = {0: self.rule1, 1: self.rule2, 2: self.rule3,3: self.rule4, 4: self.rule5, 5: self.rule6}
                condition_value = self.initial_conditions[x]
                
                if condition_value in rules_functions:
                    self.rules.append(rules_functions[condition_value](x))

            except TypeError:

                '''
                If the condition is a sequence of numbers, it will append the rule to self.rules based on the numeric values
                of the initial condition for that row and/or column.
                '''

                if self.initial_conditions[x]   == [1,1]:   self.rules.append(self.rule7(x))
                elif self.initial_conditions[x] == [1,2]:   self.rules.append(self.rule8(x))
                elif self.initial_conditions[x] == [1,3]:   self.rules.append(self.rule9(x))

                elif self.initial_conditions[x] == [2,1]:   self.rules.append(self.rule10(x))
                elif self.initial_conditions[x] == [2,2]:   self.rules.append(self.rule11(x))

                elif self.initial_conditions[x] == [3,1]:   self.rules.append(self.rule12(x))

                elif self.initial_conditions[x] == [1,1,1]: self.rules.append(self.rule13(x))




    # No filled cells
    def rule1(self, cr):
        
        conditions = []

        # Case for initial condition in a row
        if cr < 5:
            # The interval for row cr would be [(cr, 0), (cr, 1), (cr, 2), (cr, 3), (cr, 4)] where cr is the row number
            current_interval = [(cr, x) for x in range(5)]

        # Case for initial condition in a column, where cr-5 is the column number
        else:
            # The interval for column cr would be [(0, cr), (1, cr), ..., (4, cr)] where cr is the column number
            current_interval = [(x, cr-5 ) for x in range(5)]
            
        negation_list = ['-' + self.RenC.P([*i]) for i in current_interval]
        
        conditions.append(Ytoria(negation_list))
        return Otoria(conditions)



    # Single filled cell
    def rule2(self, cr):
        
        conditions = []
        
        if cr < 5:
            current_interval = [(cr, x) for x in range(5)]
            
            for x in range(5):
                literals        =   [self.RenC.P([cr,x])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x ]
                conditions.append(Ytoria(literals + negation_list))
        else:
            
            current_interval = [(x,cr-5) for x in range(5)]
            
            for x in range(5):
                literals        =   [self.RenC.P([x,cr-5])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x ]
                
                conditions.append(Ytoria(literals + negation_list))
                
        return Otoria(conditions)
    
    
    

    # Filled in two consecutive cells
    def rule3(self, cr):
        conditions = []
        
        if cr <5:
            current_interval = [(cr,x) for x in range(5)]
            
            for x in range(4):
                literals        =   [self.RenC.P([cr,x]), self.RenC.P([cr,x+1])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x and i[1] != x+1 ]
                conditions.append(Ytoria(literals + negation_list))

        else:
            current_interval = [(x,cr-5) for x in range(5)]
            
            for x in range(4):
                literals        =   [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x and i[0] != x+1 ]
                conditions.append(Ytoria(literals + negation_list))

        return Otoria(conditions)

    # Filled in three consecutive cells
    def rule4(self,cr):
        conditions = []
        
        if cr<5:
            current_interval= [(cr,x) for x in range(5)]
            
            for x in range(3):
                literals        =   [self.RenC.P([cr,x]), self.RenC.P([cr,x+1]), self.RenC.P([cr, x+2])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] not in range(x, x+3)]
                conditions.append(Ytoria(literals + negation_list))

        else:
            current_interval= [(x,cr-5) for x in range(5)]
            
            for x in range(3):
                literals        =   [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,]), self.RenC.P([x+2, cr-5])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] not in range(x, x+3)]
                conditions.append(Ytoria(literals + negation_list))

        return Otoria(conditions)

    # Filled in four consecutive cells
    def rule5(self, cr):
        conditions = []
        
        if cr<5:
            current_interval = [(cr,x) for x in range(5)]
            
            for x in range(2):
                literals        =   [self.RenC.P([cr,x]), self.RenC.P([cr,x+1]), self.RenC.P([cr, x+2]), self.RenC.P([cr, x+3])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] not in range(x, x+4)]
                conditions.append(Ytoria(literals + negation_list))

        else:
            current_interval = [(x,cr-5) for x in range(5)]
            
            for x in range(2):
                literals        =   [self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5,]), self.RenC.P([x+2, cr-5]), self.RenC.P([x+3, cr-5])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] not in range(x, x+4)]
                conditions.append(Ytoria(literals + negation_list))
                
        return Otoria(conditions)

    # Filled in five consecutive cells
    def rule6(self,cr):
        conditions = []

        if cr<5: current_interval   =   [(cr,x) for x in range(5)]
        else:  current_interval     =   [(x, cr-5 ) for x in range(5)]

        conditions.append(Ytoria([self.RenC.P([*i]) for i in current_interval]))
        return Otoria(conditions)



    # Filled in two cells with at least one space between them input[1,1]
    def rule7(self,cr):
        conditions = []
        
        if cr<5:
            current_interval = [(cr,x) for x in range(5)]
            
            for x in range(2,5):
                literals        =   [self.RenC.P([cr,0]), self.RenC.P([cr,x])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x and i[1] != 0]
                conditions.append(Ytoria(literals + negation_list))

            for x in range(3,5):
                literals        =   [self.RenC.P([cr,1]), self.RenC.P([cr,x])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x and i[1] != 1]
                conditions.append(Ytoria(literals + negation_list))

            conditions.append(Ytoria([self.RenC.P([cr,2]), self.RenC.P([cr,4])]+ [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != 2 and i[1] != 4]))


        else:
            current_interval = [(x, cr-5 ) for x in range(5)]
            
            for x in range(2,5):
                literals        =   [self.RenC.P([0,cr-5]), self.RenC.P([x,cr-5])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x and i[0] != 0]
                conditions.append(Ytoria(literals + negation_list))

            for x in range(3,5):
                literals        =   [self.RenC.P([1,cr-5]), self.RenC.P([x,cr-5])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x and i[0] != 1]
                conditions.append(Ytoria(literals + negation_list))
                
            conditions.append(Ytoria([self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])]+ [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != 2 and i[0] != 4]))

        return Otoria(conditions)


    # Filled in one cell, then at least one space up to two consecutive cells input: [1,2]
    def rule8(self, cr):
        conditions = []
        
        if cr<5:
            current_interval = [(cr,x) for x in range(5)]
            
            for x in range(2,4):
                literals        =   [self.RenC.P([cr,0]), self.RenC.P([cr,x]), self.RenC.P([cr,x+1])]
                negation_list   =   [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x and i[1] != 0 and i[1] != x+1]
                conditions.append(Ytoria(literals + negation_list))
                
            conditions.append(Ytoria([self.RenC.P([cr,1]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != 1 and i[1] != 3 and i[1] !=4] ))

        else:
            current_interval = [(x, cr-5) for x in range(5)]
            
            for x in range(2,4):
                literals = [self.RenC.P([0, cr-5]), self.RenC.P([x, cr-5]), self.RenC.P([x+1, cr-5])]
                negation_list = [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x and i[0] != 0 and i[0] != x+1]
                conditions.append(Ytoria(literals + negation_list))
            
            conditions.append(Ytoria([self.RenC.P([1, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != 1 and i[0] != 3 and i[0] !=4] ))

        return Otoria(conditions)


    # Filled in one cell, then at least one space up to three consecutive cells input: [1,3]
    def rule9(self, cr):
        
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,2]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,1])])
        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([2, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([1, cr-5])])



    # Filled in two consecutive cells, then at least one space and followed by one filled cell input: [2,1]
    def rule10(self, cr):
        conditions = []
        
        if cr<5:
            current_interval= [(cr,x) for x in range(5)]
            for x in range(3,5):
                literals = [self.RenC.P([cr,0]), self.RenC.P([cr,1]), self.RenC.P([cr,x])]
                negation_list = [ '-' + self.RenC.P([*i])  for i in current_interval if i[1] != x and i[1] != 1 and i[1]!=0]
                conditions.append(Ytoria(literals + negation_list))
                
            conditions.append(Ytoria([self.RenC.P([cr,1]),self.RenC.P([cr,2]), self.RenC.P([cr,4])]+ [ '-' + self.RenC.P([cr,0]), '-' + self.RenC.P([cr,3]) ]))

        else:
            current_interval = [(x, cr-5 ) for x in range(5)]
            for x in range(3,5):
                literals = [self.RenC.P([0,cr-5]), self.RenC.P([1, cr-5]), self.RenC.P([x, cr-5])]
                negation_list = [ '-' + self.RenC.P([*i])  for i in current_interval if i[0] != x and i[0] != 1 and i[0]!=0]
                conditions.append(Ytoria(literals + negation_list))
                
            conditions.append(Ytoria([self.RenC.P([1, cr-5]),self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])]+ [ '-' + self.RenC.P([0, cr-5]), '-' + self.RenC.P([3, cr-5]) ]))

        return Otoria(conditions)


    # Filled in two consecutive cells, followed by at least one space and then two more filled cells input: [2,2]
    def rule11(self, cr):
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,1]), self.RenC.P([cr,3]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,2])])

        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([1, cr-5]), self.RenC.P([3, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([2, cr-5])])

    # Filled in three consecutive cells, followed by at least one space and then one filled cell input: [3,1]
    def rule12(self,cr):
        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,1]), self.RenC.P([cr,2]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,3])])
        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([1, cr-5]), self.RenC.P([2, cr-5]), self.RenC.P([4, cr-5])] +  [ '-' + self.RenC.P([3, cr-5])])


    # Filled in three cells with spaces in between input: [1,1,1]
    def rule13(self, cr):

        if cr<5: return Ytoria([self.RenC.P([cr,0]) ,self.RenC.P([cr,2]), self.RenC.P([cr,4])] +  [ '-' + self.RenC.P([cr,1]), '-' + self.RenC.P([cr,3])])
        else: return Ytoria([self.RenC.P([0, cr-5]) ,self.RenC.P([2, cr-5]),  self.RenC.P([4, cr-5])] +  ['-' + self.RenC.P([1, cr-5]),'-' + self.RenC.P([3, cr-5])])





    def visualize(self, I):

        fig, axes = plt.subplots()
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)
        step = 1./5
        tangulos = []


        for i in range(3):
            for j in range(3):
                tangulos.append(patches.Rectangle((i * step, j * step), step, step, facecolor='white'))


        for j in range(5):
            locacion = j * step
            tangulos.append(patches.Rectangle((0, step + locacion), 1, 0.005, facecolor='black'))
            tangulos.append(patches.Rectangle((step + locacion, 0), 0.005, 1, facecolor='black'))


        for f in tangulos:
            axes.add_patch(f)

        arr_img = plt.imread("./img/cuadrado.png", format='png')
        imagebox = OffsetImage(arr_img, zoom=0.161)
        imagebox.image.axes = axes


        direcciones = {(x,y): (0.100 + 0.200 * y, 0.880 - 0.200 * x) for x in range(5) for y in range(5)}

        for l in I:

            if I[l]:
                try:
                    x, y = self.RenC.inv(l)
                    ab = AnnotationBbox(imagebox, direcciones[(x, y)], frameon=False)
                    axes.add_artist(ab)
                except KeyError: pass

        plt.show()



import time

## Creating the object with the initial conditions or rules that make each nonogram unique
c = Nanogram()

# The rule classifier appends the rules after taking the unique arguments of that nonogram
c.rules_classifier()


'''
SAT Solvers: Algorithms to Find Solutions to Problems Represented Using Propositional Logic in Python

SAT solvers (Satisfiability solvers) are algorithms designed to determine the satisfiability
of a propositional logic formula. They aim to find an assignment of truth values to the variables
that satisfies the given formula. SAT solvers play a crucial role in solving various problems
across different domains.
'''


# print(c.initial_conditions)
# # print(c.initial_conditions)

# A = inorder_to_tree(Ytoria(c.rules))
# print(A.ver(c.RenC))

'''
                        DPLL Algorithm
                        
This algorithm follows the general rule to find the solution, which is a
combination of all the rules to find a possible solution. The DPLL algorithm
works as follows:
It checks the satisfiability of a formula and finds a model for it
by finding an interpretation that makes the formula true.
- More details in logic.py

After conducting several tests comparing times, it is concluded that
this is the best algorithm to find a solution to the problem with an average time
close to --- 0.18398690223693848 seconds ---
'''

start_time = time.time()

A = Ytoria(c.rules)
S = tseitin(A)
S, I = dpll(S, {})


if I != None:
    for k in I:
        c.RenC.write(k), I[k]


else:
    print('¡No hay solución!')

c.visualize(I)

print("--- %s seconds ---" % (time.time() - start_time))



'''
SATtableaux: An Algorithm Dividing the Formula Like a Tree

SATtableaux is an algorithm that works by dividing the formula as if it were a tree.
At the end, only leaves are left, and an interpretation is assigned to them to make
the formula true.

After conducting tests, it is concluded that the average time, varying with complexity,
is approximately --- 11.225515842437744 seconds ---
'''




# start_time = time.time()

# A = inorder_to_tree(Ytoria(c.rules[0:5]))
# I = A.SATtabla()


# if I != None:
#     for k in I:
#         print(c.RenC.write(k), I[k])
# else:
#     print('¡No hay solución!')

# c.visualize(I)

# print("--- %s seconds ---" % (time.time() - start_time))





##  WalkSAT


## Not working

#start_time = time.time()

#A = Ytoria(c.rules)
#S = tseitin(A)
#S, I = walkSAT(S)


#if I != None:
    #for k in I:
        #print(c.RenC.write(k), I[k])


#else:
#    print('¡No hay solución!')

#c.visualizar(I)


#print("--- %s seconds ---" % (time.time() - start_time))

