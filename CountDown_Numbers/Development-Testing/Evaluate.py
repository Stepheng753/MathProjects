#!/usr/bin/env python3

import math
import csv
import random
import time
from Solver import *

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
            newline = line
            for i in range(0, len(letters)):
                newline = replace(newline, letters[i], s.get_numbers()[i])
            newline = newline[1 : ]
            solution = s.simplify_expression(newline)
            print(str(counter) + ": ", printArr(newline) + " = " + str(solution))
            counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")


def find_solutions(target = random.randint(100, 999), num_large = random.randint(0, 4), numbers = []):
    counter = 0
    s = Solver(target, num_large)
    if len(numbers) > 0:
        s.set_numbers(numbers)
    start = time.perf_counter()
    print(s)
    solutions = s.get_solutions()
    for sol in solutions:
        print(str(counter) + ": ", printArr(sol) + " = " + str(s.get_target()))
        counter = counter + 1
        print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
    return [counter, round(time.perf_counter() - start, 4)]


def find_solutions_csv(target = random.randint(100, 999), num_large = random.randint(0, 4), numbers = []):
    s = Solver(target, num_large)
    if len(numbers) > 0:
        s.set_numbers(numbers)
    start = time.perf_counter()
    print(s)
    with open("all_perms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        counter = 0
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for line in csvreader:
            newline = line
            for i in range(0, len(letters)):
                newline = replace(newline, letters[i], s.get_numbers()[i])
            newline = newline[1 : ]
            solution = s.simplify_expression(newline)

            if (solution == s.get_target()):
                print(str(counter) + ": ", printArr(newline) + " = " + str(solution))
                counter = counter + 1
            print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs", end='\r')
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
    return [counter, round(time.perf_counter() - start, 4)]


def find_one_solution(target = random.randint(100, 999), num_large = random.randint(0, 4), numbers = []):
    s = Solver(target, num_large)
    if len(numbers) > 0:
        s.set_numbers(numbers)
    s.get_all_expressions()
    start = time.perf_counter()
    print(s)
    sol = s.get_solutions(True)
    if sol != None:
        print(printArr(sol) + " = " + str(s.get_target()))
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
    return round(time.perf_counter() - start, 4)


def find_one_solution_csv(target = random.randint(100, 999), num_large = random.randint(0, 4), numbers = []):
    s = Solver(target, num_large)
    if len(numbers) > 0:
        s.set_numbers(numbers)
    start = time.perf_counter()
    print(s)
    with open("all_perms.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        for line in csvreader:
            newline = line
            for i in range(0, len(letters)):
                newline = replace(newline, letters[i], s.get_numbers()[i])
            newline = newline[1 : ]
            solution = s.simplify_expression(newline)
            if (solution == s.get_target()):
                print(printArr(newline) + " = " + str(s.get_target()))
                break
    print("Time: " + str(round(time.perf_counter() - start, 4)) + " secs")
    return round(time.perf_counter() - start, 4)


def test(s, get_all):    
    print("Target: ", s.get_target())
    print("Num of Large: ", s.get_num_large())
    print("Numbers: ", s.get_numbers())

    printStr = ""

    print("\n----------------Without CSV----------------")
    if get_all:
        wo_csv = find_solutions(target=s.get_target(), num_large=s.get_num_large(), numbers=s.get_numbers())
        printStr = printStr + "Num Solutions - without CSV: " + str(wo_csv[0]) + "\n"
        printStr = printStr + "Time - without CSV: " + str(wo_csv[1]) + "\n"
    else:
        wo_csv = find_one_solution(target=s.get_target(), num_large=s.get_num_large(), numbers=s.get_numbers())
        printStr = printStr + "Time - without CSV: " + str(wo_csv) + "\n"

    print("\n-----------------With CSV-----------------")
    if get_all:
        w_csv = find_solutions_csv(target=s.get_target(), num_large=s.get_num_large(), numbers=s.get_numbers())
        printStr = printStr + "Num Solutions - with CSV: " + str(w_csv[0]) + "\n"
        printStr = printStr + "Time - with CSV: " + str(w_csv[1]) + "\n"
    else:
        w_csv = find_one_solution_csv(target=s.get_target(), num_large=s.get_num_large(), numbers=s.get_numbers())
        printStr = printStr + "Time - with CSV: " + str(w_csv) + "\n"

    print(printStr)



if __name__ == '__main__':

    # writeCSV()
    # printAll()
    # find_solutions()
    # readCSV()
    # find_solutions_csv()
    s = Solver(141, 3)
    s.set_numbers([5, 6, 4, 75, 25, 100])
    test(s, False)