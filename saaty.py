# Saaty AHP
from utils import timeStamp, comment, get
from criteria import Criteria
import numpy as np

# init
global RATIO_COEF
RATIO_COEF = {
    1: 1,  # is in fact 0 but changed for division purposes
    2: 1,  # is in fact 0 but changed for division purposes
    3: 0.58,
    4: 0.9,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49
}


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
        f"How important is \"{c1.name}\" compared to \"{c2.name}\" ?", empty=True)
    return float(get())


# processing preference matrix
# calculating criteria weights
def calculateCriteriaWeights(preferenceMatrix, criteriaArray):
    comment(f"Calculating criteria weights...")
    matrixSize = len(preferenceMatrix)
    verticalSum = np.sum(preferenceMatrix, axis=0)
    criteriaWeights = (np.sum(preferenceMatrix/verticalSum, axis=1))/matrixSize
    for _ in range(matrixSize):
        criteriaArray[_].weight = criteriaWeights[_]
    return criteriaWeights


# calculating consistency
def computeConsistency(preferenceMatrix, criteriaWeights):
    comment(f"Calculating consistency index...")
    matrixSize = len(preferenceMatrix)
    consistencyMatrix = preferenceMatrix*criteriaWeights
    weightedSum = np.sum(consistencyMatrix, axis=1)
    lmdMax = sum(weightedSum/criteriaWeights)/matrixSize
    consistencyIndex = (lmdMax-matrixSize)/(matrixSize-1)
    consistencyRatio = consistencyIndex/RATIO_COEF[matrixSize]
    return (consistencyIndex, consistencyRatio)


def processPreferenceMatrix(preferenceMatrix, criteriaArray):
    comment(f"Processing size {len(criteriaArray)} prefernce matrix...")
    criteriaWeights = calculateCriteriaWeights(preferenceMatrix, criteriaArray)
    consistencyIndex = computeConsistency(preferenceMatrix, criteriaWeights)
    return consistencyIndex


# sorting criteria weight-waise
def sortCriteria(criteriaArray):
    criteriaWeightsArray = []
    for crt in criteriaArray:
        criteriaWeightsArray.append(crt.weight)
    criteriaWeightsArray.sort(reverse=True)
    for crt in criteriaArray:
        crt.rank = criteriaWeightsArray.index(crt.weight)+1


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
    _, consistencyRatio = processPreferenceMatrix(preferenceMatrix, criteriaArray)

    if consistencyRatio < 0.1:
        comment("Computed criteria weights are valid for use.", empty=True)
        sortCriteria(criteriaArray)
    else:
        comment("Computed criteria weights are not valid for use! please check priority rating.", empty=True)

    comment("Criteria weights for the specified matrix are: ")
    for crt in criteriaArray:
        comment(f"rank: {crt.rank} - {crt.name}: {round(crt.weight,3)}", empty=True)
    comment(f"with consistency ratio of: {round(consistencyRatio,4)}", empty=True)


if __name__ == "__main__":
    main()
