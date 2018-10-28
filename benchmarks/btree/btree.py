from z3 import *
import src.path_analyzer as pa
from src.utils import writeSolutionToFile

class Node:
    def __init__(self, value, value_sym_):
        self.value = value
        self.value_sym_ = value_sym_
        self.right = None
        self.left = None

class BTree:

    def __init__(self):
        self.root = None
        self.path_cond = []

    def getAssertions(self):

        return self.path_cond



    def insert(self, number, number_sym_):

    
        if(self.root==None):
            self.root = Node(number, number_sym_)
            return

        curr = self.root

        self.path_cond.append("l1_s")

        while(True):

            if(number >= curr.value):
                self.path_cond.append(numbers_sym_>=curr.value_sym_)

                if(curr.right==None):
                    curr.right = Node(number, number_sym_)
                    self.path_cond.append("l1_e")
                    return
                else:
                    curr = curr.right
            else:
                self.path_cond.append(number_sym_ < curr.value_sym_)
                if(curr.left==None):
                    curr.left = Node(number, number_sym_)
                    self.path_cond.append("l1_e")
                    return
                else:
                    curr = curr.left

        

    def search(self, number, number_sym_):

        curr = self.root

        self.path_cond.append("l2_s")

        while(curr!=None):
            if(curr.value == number):
                self.path_cond.append(curr.value_sym_ == number_sym_)
                return True
            elif(curr.value < number):
                self.path_cond.append(curr.value_sym_ < number_sym_)
                curr = curr.right
            else:
                self.path_cond.append(curr.value_sym_ > number_sym_)
                curr = curr.left

        self.path_cond.append("l2_e")

        return False


    def addToBTree(self, numbers, numbers_sym_):

        for i in range(0,len(numbers)):
            self.insert(numbers[i], numbers_sym_[i])


# nums = [10,9,8,7,6,5,4,3,2,1]
# nums_sym_ = IntVector("nums", 10)
# key = -1
# key_sym_ = Int('key')

# s = Solver()

# tree = BTree(s)

# tree.addToBTree(nums, nums_sym_)

# print(tree.search(key, key_sym_))

# print(s.assertions())

wc_inputs = [
[[1],-1],
[[2,1],-1],
[[3,2,1],-1],
[[4,3,2,1],-1],
[[5,4,3,2,1],-1],
[[6,5,4,3,2,1],-1],
[[7,6,5,4,3,2,1],-1],
[[8,7,6,5,4,3,2,1],-1],
[[9,8,7,6,5,4,3,2,1],-1],
[[10,9,8,7,6,5,4,3,2,1],-1],
]

wc_expressions = []

for i in range(0, len(wc_inputs)):

    numbers = wc_inputs[i][0]
    numbers_sym_ = IntVector("nums_sym_", len(numbers))
    key = wc_inputs[i][1]
    key_sym_ = IntVector("key_sym_",1)

    tree = BTree()

    tree.addToBTree(numbers, numbers_sym_)

    tree.search(key, key_sym_[0])

    #print(tree.getAssertions())

    wc_expressions.append(tree.getAssertions())


path_analyzer = pa.PathAnalyzer(wc_expressions)
path_analyzer.buildModel()

large_scale = 20
pc = path_analyzer.genScaleTest(large_scale)
sol = path_analyzer.solve(pc)
writeSolutionToFile(sol, large_scale)


