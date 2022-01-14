import sys

import numpy
import os
import random
import tkinter as tk


# method to randomly generate matrices
def generateMatrices(numberOfUnknowns):
    aMatrix = generateAMatrix(numberOfUnknowns)
    bMatrix = generateBMatrix(numberOfUnknowns)
    solutionMatrix = findSolutionMatrix(aMatrix, bMatrix)

    return aMatrix.astype(int), solutionMatrix.astype(int), bMatrix.astype(int)


def generateAMatrix(numberOfUnknowns):
    aMatrix = numpy.eye(numberOfUnknowns)
    turnToUnimodular(aMatrix)
    fillRows(aMatrix)
    swapValues(aMatrix, 0, random.randint(1, numberOfUnknowns - 1))

    return aMatrix.astype(int)


def turnToUnimodular(aMatrix):
    numberOfUnknowns = len(aMatrix)
    for row in range(numberOfUnknowns):
        if random.randint(0, 1) == 0:  # for diagonal elements
            aMatrix[row, row] = -1
        else:
            aMatrix[row, row] = 1

        for column in range(row + 1, numberOfUnknowns):
            aMatrix[row, column] = random.randint(-3, 3)


def fillRows(aMatrix):
    row = numberOfUnknowns = len(aMatrix)
    for column in range(numberOfUnknowns - 1, -1, -1):
        for row in range(column + row, numberOfUnknowns):
            if random.randint(0, 1) == 0:
                aMatrix[row] = fillValues(aMatrix, row, column, random.randint(-3, 1))
            else:
                aMatrix[row] = fillValues(aMatrix, row, column, random.randint(1, 4))


# method to fill values
def fillValues(matrix, row, column, value):
    return matrix[row] + value * matrix[column]


# method to randomly swap values
def swapValues(m, row, column):
    m[row] = m[row] + m[column]
    m[column] = m[row] - m[column]
    m[row] = m[row] - m[column]


def generateBMatrix(numberOfUnknowns):
    bMatrix = numpy.zeros((numberOfUnknowns, 1))  # creating B matrix

    for row in range(numberOfUnknowns):
        bMatrix[row] = random.randint(-5, 5)

    return bMatrix.astype(int)


def findSolutionMatrix(aMatrix, bMatrix):
    inverseMatrix = numpy.linalg.inv(aMatrix)  # Compute the (multiplicative) inverse of a matrix
    solutionMatrix = numpy.dot(inverseMatrix, bMatrix)

    return solutionMatrix.astype(int)


def createSLE(numberOfUnknowns):
    infile = open("Matrix.tex", "w")
    infile.write('\documentclass{article}\n')
    infile.write('\\begin{document}\n')
    infile.write('\\begin{enumerate}\n')
    infile.write('\item \n')

    aMatrix, solutionMatrix, bMatrix = generateMatrices(numberOfUnknowns)

    print(solutionMatrix)

    infile.write('$\\begin{array}{')
    for row in range(numberOfUnknowns + 1):
        infile.write('r@{\ }c@{\ }')
    infile.write('}\n')

    for row in range(numberOfUnknowns):
        text = ""
        for column in range(numberOfUnknowns):
            if aMatrix[row, column] < 0:
                if column == 0:
                    token = '-'
                else:
                    token = ' -& '

                if aMatrix[row, column] == -1:
                    k = ""
                else:
                    k = str(abs(aMatrix[row, column]))

                l = k + 'x_{' + str(column + 1) + '}&'

            elif aMatrix[row, column] == 0:
                if column == 0:
                    token = ''

                else:
                    token = '&'

                l = '&'
            else:
                if column == 0:
                    token = ''
                else:
                    token = ' +& '

                if aMatrix[row, column] == 1:
                    k = ""
                else:
                    k = str(abs(aMatrix[row, column]))

                l = k + 'x_{' + str(column + 1) + '}&'

            text = text + token + l

            if column + 1 == numberOfUnknowns:
                text = text + '=&' + str(bMatrix[row, 0]) + ' \\\\\n '

        infile.write(text)

    infile.write('\\end{array}$\n')
    infile.write('\end{enumerate}\n')
    infile.write('\end{document}\n')
    infile.close()


# main code
numberOfUnknowns = int(sys.argv[1])
createSLE(numberOfUnknowns)
