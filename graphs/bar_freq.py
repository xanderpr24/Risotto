import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import _pandas
import _math


def loadData(fileName):
    df, rows, columns = _pandas.main(fileName)
    #rows.sort()
    expectedCounts = _pandas.getExpectedCounts(df)
    observedsExpecteds = _math.getOE(df, expectedCounts)

    observeds = {}
    for column in columns:
        for key in observedsExpecteds:
            id = key[key.index(', ') + 2:]
            if id == column:
                if not column in observeds:
                    observeds[column] = {}
                observeds[column][key[:key.index(',')]] = (observedsExpecteds[key][0])

    return df, rows, columns, expectedCounts, observeds


def getGradesColors(columns, rows, observeds):

    colors = {}
    for row in rows:
        colors[row] = {}
        colorsList = ['red', 'orange', 'gold', 'forestgreen', 'blue']

    for it, row in enumerate(rows):
        colors[row] = colorsList[it]
    gradesColors = {}
    for grade in columns:
        gradeColors = []
        for rating in rows:
            if rating in observeds[grade]:
                gradeColors.append(colors[rating])
        gradesColors[grade] = (gradeColors)

    return gradesColors


def setupPlt(highestBar, longestBar, rows, tickPos, columns):
    plt.title('School Rating by Grade')
    plt.legend(longestBar, rows, loc='upper center')
    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.xticks(tickPos, columns)

    if highestBar >= 60:
        step = 4
    elif highestBar >= 20:
        step = 2
    else:
        step = 1
    if not highestBar % step == 0:
        highestBar += step - highestBar % step
    plt.yticks([i for i in range(0, highestBar, step)])


def getHeightsSorted(observeds, rows):
    gradesHeightsSorted = {}
    for counter, grade in enumerate(observeds):
        frequencies = {}
        for freq in observeds[grade]:
            frequencies[freq] = observeds[grade][freq]

        heights = []
        heights = [frequencies for frequencies in frequencies.values()]
        heightsSorted = []

        for rating in rows:
            if rating in frequencies:
                heightsSorted.insert(rows.index(rating), frequencies[rating])

        gradesHeightsSorted[grade] = heightsSorted

    return gradesHeightsSorted


def plotBars(observeds, columns, barWidth, gradesColors, gradesHeightsSorted):
    bars = []
    tickPos = []

    barsHeights = []
    for counter, grade in enumerate(observeds):


        bar = plt.bar(
            2*counter + np.array([barWidth * i for i in range(len(gradesHeightsSorted[grade]))]),
            [value for value in gradesHeightsSorted[grade]],
            barWidth,
            color = gradesColors[grade],
            ec = 'k',
            label=columns[counter]
        )
        bars.append(bar.patches)
        tickPos.append(2*counter + (((len(gradesHeightsSorted[grade]) - 1) * barWidth) / 2))

        for height in gradesHeightsSorted[grade]:
            barsHeights.append(height)

    highestBar = max(barsHeights) + 1

    lengths = []
    for bar in bars:
        lengths.append(len(bar))
    longestBar = bars[lengths.index(max(lengths))]

    return bars, tickPos, longestBar, highestBar


def main(fileName):

    plt.figure().clear()

    barWidth = 0.3
    df, rows, columns, expectedCounts, observeds = loadData(fileName)
    gradesColors = getGradesColors(columns, rows, observeds)
    gradesHeightsSorted = getHeightsSorted(observeds, rows)
    bars, tickPos, longestBar, highestBar = plotBars(observeds, columns, barWidth, gradesColors, gradesHeightsSorted)
    setupPlt(highestBar, longestBar, rows, tickPos, columns)

    path = r'images\bar-freq.png'
    if os.path.exists(path):
        os.remove(path)
    plt.savefig(fname=path)
