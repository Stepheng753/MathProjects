import itertools
import math
import csv
import random
import time

class Solver:

    def __init__(self, target = 0, num_large = 4, num_total=6):
        self.target = target
        self.num_large = num_large
        self.num_total = num_total
        self.small_numbers = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        self.large_numbers = [25, 50, 75, 100] 
        self.numbers = random.sample(self.small_numbers, self.num_total - self.num_large) + \
                        random.sample(self.large_numbers, self.num_large)
        self.operations = ['+', '-', 'x', '/']
        self.expression_arrs = []
        self.solution_arrs = []

    def set_numbers(self, numbers):
        self.numbers = numbers
    
    def get_permutations(self, num_total):
        number_arrs = []
        for perm in list(itertools.permutations(self.numbers, num_total)):
            number_arrs.append(perm)
        return number_arrs

    def get_product(self, num_total):
        operation_arrs = []
        for prod in list(itertools.product(self.operations, repeat = num_total - 1)):
            operation_arrs.append(prod)
        return operation_arrs

    def get_expressions_wo_parens(self, number_arrs, operation_arrs):
        for num_seq in number_arrs:
            for op_seq in operation_arrs:
                expression = []
                for i in range(0, len(op_seq)):
                    expression.append(num_seq[i])
                    expression.append(op_seq[i])
                expression.append(num_seq[len(num_seq) - 1])
                self.expression_arrs.append(expression)

    def make_parentheses(self, expression, top_level=False):
        if len(expression) > 3:
            num_groups =  math.floor(len(expression) / 2) - 1 
            exp_paren = []
            for i in range(1, num_groups + 1):
                paren_length = len(expression) - (2 * i)
                pre_left_parenthesis = 0
                post_right_parenthesis = pre_left_parenthesis + paren_length

                check1 = (post_right_parenthesis < len(expression) and pre_left_parenthesis == 0 and \
                        self.is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis])) or \
                        \
                        (pre_left_parenthesis > 0 and post_right_parenthesis == len(expression) and \
                        self.is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1])) or \
                        \
                        (pre_left_parenthesis > 0 and post_right_parenthesis < len(expression) and \
                        self.is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis]) and \
                        self.is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1]))

                check2 = post_right_parenthesis <= len(expression)

                while check2:
                    if check1:
                        left = [expression[0: pre_left_parenthesis]]
                        middle = expression[pre_left_parenthesis : post_right_parenthesis]
                        right = [expression[post_right_parenthesis : len(expression)]]
                        
                        if len(left[0]) >= 3:
                            right_op = left[0][-1]
                            left = self.make_parentheses(left[0][0:-1])
                            for item in left:
                                item.append(right_op)
                        if len(right[0]) >= 3:
                            left_op = right[0][0]
                            right = self.make_parentheses(right[0][1:])
                            for item in right:
                                item.insert(0, left_op)

                        middle = self.make_parentheses(middle)

                        for litem in left:
                            for mitem in middle:
                                for ritem in right:
                                    append_item = []
                                    if top_level: 
                                        append_item = litem +  mitem + ritem
                                    else:
                                        append_item = ["("] + litem +  mitem + ritem + [")"]
                                    if append_item not in exp_paren:
                                            exp_paren.append(append_item)
                
                    pre_left_parenthesis = pre_left_parenthesis + 2
                    post_right_parenthesis = pre_left_parenthesis + paren_length

                    check1 = (post_right_parenthesis < len(expression) and pre_left_parenthesis == 0 and \
                            self.is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis])) or \
                            \
                            (pre_left_parenthesis > 0 and post_right_parenthesis == len(expression) and \
                            self.is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1])) or \
                            \
                            (pre_left_parenthesis > 0 and post_right_parenthesis < len(expression) and \
                            self.is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis]) and \
                            self.is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1]))

                    check2 = post_right_parenthesis <= len(expression)

            
            return exp_paren if len(exp_paren) != 0 else [["("] + expression + [")"]]
        else:
            return [["("] + expression + [")"]] if not top_level else [expression]

    def is_opposite_operators(self, element1, element2):
        return (element1 == "+" and element2 == "x") or (element1 == "+" and element2 == "/") or \
                (element1 == "-" and element2 == "x") or (element1 == "-" and element2 == "/") or \
                (element1 == "x" and element2 == "+") or (element1 == "x" and element2 == "-") or \
                (element1 == "/" and element2 == "+") or (element1 == "/" and element2 == "-")

    def get_all_expressions(self):
        self.get_expressions_wo_parens(self.get_permutations(self.num_total), self.get_product(self.num_total))

        every_expression = []
        for expwop in self.expression_arrs:
            for exp in self.make_parentheses(expwop, True):
                every_expression.append(exp)

        self.expression_arrs = every_expression

        return self.expression_arrs

    def simplify_expression(self, expression):
        left_parenthesis_index = -1
        right_parenthesis_index = -1
        parentheses_count = 0

        while left_parenthesis_index != len(expression) - 1:
            while left_parenthesis_index < len(expression) - 1:
                left_parenthesis_index = left_parenthesis_index + 1
                if expression[left_parenthesis_index] == "(":
                    break

            if left_parenthesis_index == len(expression) - 1:
                break

            while right_parenthesis_index < len(expression) - 1:
                right_parenthesis_index = right_parenthesis_index + 1
                if expression[right_parenthesis_index] == "(" and right_parenthesis_index != left_parenthesis_index:
                    parentheses_count = parentheses_count + 1
                if expression[right_parenthesis_index] == ")" and parentheses_count != 0:
                    parentheses_count = parentheses_count - 1
                elif expression[right_parenthesis_index] == ")" and parentheses_count == 0:
                    break
            
            if left_parenthesis_index != len(expression) - 1:
                expression = expression[0 : left_parenthesis_index] + \
                            [self.simplify_expression(expression[left_parenthesis_index + 1: right_parenthesis_index])] + \
                            expression[right_parenthesis_index + 1 : ] 
                left_parenthesis_index = -1
                right_parenthesis_index = -1
                parentheses_count = 0

        try:
            multiplier_index = 0
            while multiplier_index < len(expression):
                if expression[multiplier_index] == "x":
                    product = float(expression[multiplier_index - 1] * expression[multiplier_index + 1])
                    expression = expression[0 : multiplier_index - 1] + [product] + expression[multiplier_index + 2 : ]
                    multiplier_index = multiplier_index - 1
                    continue
                if expression[multiplier_index] == "/":
                    quotient = float(expression[multiplier_index - 1] / expression[multiplier_index + 1])
                    expression = expression[0 : multiplier_index - 1] + [quotient] + expression[multiplier_index + 2 : ]
                    multiplier_index = multiplier_index - 1
                    continue
                multiplier_index = multiplier_index + 1

            sum = expression[0]
            sum_index = 1
            while (sum_index < len(expression)):
                if expression[sum_index] == "+":
                    sum = sum + expression[sum_index + 1]
                if expression[sum_index] == "-":
                    sum = sum - expression[sum_index + 1]
                sum_index = sum_index + 2
        except:
            return None

        return sum

    def get_solutions(self):
        for exp in self.expression_arrs:
            if self.simplify_expression(exp) == self.target:
                self.solution_arrs.append(exp)

    def __str__(self):
        rtnStr = ""
        rtnStr = rtnStr + "Target: " + str(self.target) + "\n"
        rtnStr = rtnStr + "Numbers: " + str(self.numbers)
        return rtnStr



def printArr(arr):
    rtnStr = ""
    for item in arr:
        rtnStr = rtnStr + str(item) + " "
    return rtnStr


def printAll():
    counter = 0
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    for i in range(2, 7):
        s = Solver(0, 0, i)
        s.set_numbers(letters[0: i + 1])
        expressions = s.get_all_expressions()
        for exp in expressions:
            print(str(counter) + ": " + printArr(exp) + " = " + str(s.simplify_expression(exp)))
            counter = counter + 1  


def writeCSV():
    with open('all_perms.csv', "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        counter = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(2, 7):
            s = Solver(0, 0, i)
            s.set_numbers(letters[0: i + 1])
            expressions = s.get_all_expressions()
            for exp in expressions:
                csvwriter.writerow([counter] + exp)
                print(str(counter) + ": " + printArr(exp))
                counter = counter + 1
        

def readCSV():
    s = Solver()
    with open("all_perms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        i = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for line in csvreader:
            newLine = line
            for i in range(0, len(letters)):
                newLine = replace(newLine, letters[i], s.numbers[i])
            newLine = newLine[1 : ]
            solution = s.simplify_expression(newLine)
            print(str(i) + ": ", printArr(newLine) + " = " + str(solution))
            i = i + 1


def find_solutions():
    start = time.perf_counter()
    s = Solver(random.randint(100, 999), random.randint(0, 4))
    print(s)
    with open("all_perms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        counter = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for line in csvreader:
            newLine = line
            for i in range(0, len(letters)):
                newLine = replace(newLine, letters[i], s.numbers[i])
            newLine = newLine[1 : ]

            solution = s.simplify_expression(newLine)
            if (s.target == solution):
                print(str(counter) + ": ", printArr(newLine) + " = " + str(solution))
            counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')

def replace(arr, element1, element2):
    for i in range(0, len(arr)):
        if (arr[i] == element1):
            arr[i] = element2
    return arr


if __name__ == '__main__':

    # writeCSV()
    # printAll()
    # readCSV()
    find_solutions()