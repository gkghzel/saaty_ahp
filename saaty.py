# Saaty AHP
from utils import timeStamp, comment, get
from criteria import Criteria
import numpy as np


# building preference matrix
def buildPrefrenceMatrix(criteriaArray):
    numberOfCriteria = len(criteriaArray)
    comment(f"Building prefernce matrix for {numberOfCriteria} criterias...")
    matrix = np.ones((numberOfCriteria, numberOfCriteria))
    comment("Enter priority rating:", empty=True)
    comment(" [1: equal importance, 3: Moderate importance, 5: Strong importance, 7: very strong importance, 9: Extreme importance, 1/3=0.333 1/5=0.2 1/7=0.143 1/9=0.111: inverse comparaison]", empty=True)
    for row in range(numberOfCriteria):
        for col in range(row+1, numberOfCriteria):
            matrix[row][col] = compareCriteria(
                criteriaArray[row], criteriaArray[col])
            matrix[col][row] = 1/matrix[row][col]
    return matrix


def compareCriteria(c1, c2):
    comment(
        f"How important is \"{c1.name}\" is to \"{c2.name}\" ?", empty=True)
    return float(get())


# processing preference matrix
def processPreferenceMatrix(preferenceMatrix):
    matrixSize = len(preferenceMatrix)
    comment(f"Processing size {matrixSize} prefernce matrix...")
    verticalSum = np.sum(preferenceMatrix, axis=0)
    nomalisedPreferenceMatrix = np.ones((matrixSize, matrixSize))
    for col in range(matrixSize):
        nomalisedPreferenceMatrix[:,col] = preferenceMatrix[:, col]/verticalSum[col]
    print(preferenceMatrix)
    print(verticalSum)
    print(nomalisedPreferenceMatrix)


# main process
def main():
    print(f"\n\n                ======== {timeStamp()} :: Saaty ========\n\n")
    comment("Enter number of criteria")
    numberOfCriteria = int(get())
    criteriaArray = []
    for _ in range(numberOfCriteria):
        comment(f"Enter critera, {numberOfCriteria-_} left: ")
        cname = get("Criteria name: ")
        criteriaArray.append(Criteria(cname))
    preferenceMatrix = buildPrefrenceMatrix(criteriaArray)
    processPreferenceMatrix(preferenceMatrix)


if __name__ == "__main__":
    main()
