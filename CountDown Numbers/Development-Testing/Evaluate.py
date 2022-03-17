#!/usr/bin/env python3

import itertools
import math
import csv
import random
import time

class Solver:

    def __init__(self, target = 0, num_large = 4, num_total=6):
        self.__target = float(target)
        self.__num_large = num_large
        self.__num_total = num_total
        self.__small_numbers = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
        self.__large_numbers = [25, 50, 75, 100] 
        self.__numbers = random.sample(self.__small_numbers, self.__num_total - self.__num_large) + \
                        random.sample(self.__large_numbers, self.__num_large)
        self.__operations = ['+', '-', 'x', '/']
        self.__expression_arrs = []
        self.__solution_arrs = []

    def get_numbers(self):
        return self.__numbers

    def set_numbers(self, numbers):
        self.__numbers = numbers

    def get_target(self):
        return self.__target
    
    def __get_permutations(self, num_total):
        number_arrs = []
        for perm in list(itertools.permutations(self.__numbers, num_total)):
            number_arrs.append(perm)
        return number_arrs

    def __get_product(self, num_total):
        operation_arrs = []
        for prod in list(itertools.product(self.__operations, repeat = num_total - 1)):
            operation_arrs.append(prod)
        return operation_arrs

    def __get_expressions_wo_parens(self, number_arrs, operation_arrs):
        for num_seq in number_arrs:
            for op_seq in operation_arrs:
                expression = []
                for i in range(0, len(op_seq)):
                    expression.append(num_seq[i])
                    expression.append(op_seq[i])
                expression.append(num_seq[len(num_seq) - 1])
                self.__expression_arrs.append(expression)

    def __make_parentheses(self, expression, top_level=False):
        if len(expression) > 3:
            num_groups =  math.floor(len(expression) / 2) - 1 
            exp_paren = []
            for i in range(1, num_groups + 1):
                paren_length = len(expression) - (2 * i)
                pre_left_parenthesis = 0
                post_right_parenthesis = pre_left_parenthesis + paren_length

                check1 = (post_right_parenthesis < len(expression) and pre_left_parenthesis == 0 and \
                        self.__is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis])) or \
                        \
                        (pre_left_parenthesis > 0 and post_right_parenthesis == len(expression) and \
                        self.__is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1])) or \
                        \
                        (pre_left_parenthesis > 0 and post_right_parenthesis < len(expression) and \
                        self.__is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis]) and \
                        self.__is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1]))

                check2 = post_right_parenthesis <= len(expression)

                while check2:
                    if check1:
                        left = [expression[0: pre_left_parenthesis]]
                        middle = expression[pre_left_parenthesis : post_right_parenthesis]
                        right = [expression[post_right_parenthesis : len(expression)]]
                        
                        if len(left[0]) >= 3:
                            right_op = left[0][-1]
                            left = self.__make_parentheses(left[0][0:-1])
                            for item in left:
                                item.append(right_op)
                        if len(right[0]) >= 3:
                            left_op = right[0][0]
                            right = self.__make_parentheses(right[0][1:])
                            for item in right:
                                item.insert(0, left_op)

                        middle = self.__make_parentheses(middle)

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
                            self.__is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis])) or \
                            \
                            (pre_left_parenthesis > 0 and post_right_parenthesis == len(expression) and \
                            self.__is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1])) or \
                            \
                            (pre_left_parenthesis > 0 and post_right_parenthesis < len(expression) and \
                            self.__is_opposite_operators(expression[post_right_parenthesis - 2], expression[post_right_parenthesis]) and \
                            self.__is_opposite_operators(expression[pre_left_parenthesis - 1], expression[pre_left_parenthesis + 1]))

                    check2 = post_right_parenthesis <= len(expression)

            
            return exp_paren if len(exp_paren) != 0 else [["("] + expression + [")"]]
        else:
            return [["("] + expression + [")"]] if not top_level else [expression]

    def __is_opposite_operators(self, element1, element2):
        return (element1 == "+" and element2 == "x") or (element1 == "+" and element2 == "/") or \
                (element1 == "-" and element2 == "x") or (element1 == "-" and element2 == "/") or \
                (element1 == "x" and element2 == "+") or (element1 == "x" and element2 == "-") or \
                (element1 == "/" and element2 == "+") or (element1 == "/" and element2 == "-")

    def get_all_expressions(self, start=2):
        for i in range(start, self.__num_total + 1):
            self.__get_expressions_wo_parens(self.__get_permutations(i), self.__get_product(i))

        every_expression = []
        for expwop in self.__expression_arrs:
            for exp in self.__make_parentheses(expwop, True):
                every_expression.append(exp)

        self.__expression_arrs = every_expression

        return self.__expression_arrs

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
        if len(self.__expression_arrs) == 0:
            self.get_all_expressions()
        for exp in self.__expression_arrs:
            if self.simplify_expression(exp) == self.__target:
                self.__solution_arrs.append(exp)

        return self.__solution_arrs

    def __str__(self):
        rtnStr = ""
        rtnStr = rtnStr + "Target: " + str(self.__target) + "\n"
        rtnStr = rtnStr + "Numbers: " + str(self.__numbers)
        return rtnStr


def printArr(arr):
    rtnStr = ""
    for item in arr:
        rtnStr = rtnStr + str(item) + " "
    return rtnStr

def replace(arr, element1, element2):
    for i in range(0, len(arr)):
        if (arr[i] == element1):
            arr[i] = element2
    return arr

def printAll():
    start = time.perf_counter()
    counter = 0
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    s = Solver(0, 0, 6)
    s.set_numbers(letters)
    expressions = s.get_all_expressions()
    for exp in expressions:
        print(str(counter) + ": " + printArr(exp) + " = " + str(s.simplify_expression(exp)))
        counter = counter + 1  
        print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
    

def find_solutions():
    start = time.perf_counter()
    counter = 0
    s = Solver(random.randint(100, 999), random.randint(0, 4))
    print(s)
    solutions = s.get_solutions()
    for sol in solutions:
        print(str(counter) + ": ", printArr(sol) + " = " + str(s.get_target()))
        counter = counter + 1
        print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
     


def writeCSV():
    start = time.perf_counter()
    with open('all_perms.csv', "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        counter = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        s = Solver(0, 0, 6)
        s.set_numbers(letters)
        expressions = s.get_all_expressions()
        for exp in expressions:
            csvwriter.writerow([counter] + exp)
            print(str(counter) + ": " + printArr(exp))
            counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
        

def readCSV():
    start = time.perf_counter()
    s = Solver()
    with open("all_perms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        counter = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for line in csvreader:
            newLine = line
            for i in range(0, len(letters)):
                newLine = replace(newLine, letters[i], s.get_numbers()[i])
            newLine = newLine[1 : ]
            solution = s.simplify_expression(newLine)
            print(str(counter) + ": ", printArr(newLine) + " = " + str(solution))
            counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")


def find_solutions_csv():
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
                newLine = replace(newLine, letters[i], s.get_numbers()[i])
            newLine = newLine[1 : ]
            solution = s.simplify_expression(newLine)

            if (solution == s.get_target()):
                print(str(counter) + ": ", printArr(newLine) + " = " + str(solution))
                counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")

if __name__ == '__main__':

    # writeCSV()
    # printAll()
    # find_solutions()
    # readCSV()
    find_solutions_csv()