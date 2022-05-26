# importing packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import _pandas
import _math


def loadData(fileName):
    df, rows, columns = _pandas.main(fileName)
    rows.sort()
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
    colors = {
        '1-2'   : 'red',
        '3-4'   : 'orange',
        '5-6'   : 'gold',
        '7-8'   : 'forestgreen',
        '9-10'  : 'blue'
    }
    gradesColors = {}
    for grade in columns:
        gradeColors = []
        for rating in rows:
            if rating in observeds[grade]:
                gradeColors.append(colors[rating])
        gradesColors[grade] = (gradeColors)

    return gradesColors


def setupPlt(longestBar, rows, tickPos, columns):
    plt.title('School Rating by Grade')
    plt.legend(longestBar, rows, loc='upper center')
    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.xticks(tickPos, columns)
    plt.yticks([i * 2 for i in range(11)])


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


def plotBars(observeds, rows, barWidth, gradesColors, gradesHeightsSorted):
    bars = []
    tickPos = []

    for counter, grade in enumerate(observeds):

        bar = plt.bar(
            2*counter + np.array([barWidth * i for i in range(len(gradesHeightsSorted[grade]))]),
            [value for value in gradesHeightsSorted[grade]],
            barWidth,
            color = gradesColors[grade],
            ec = 'k',
            label=rows[counter]
        )
        bars.append(bar.patches)
        tickPos.append(2*counter + (((len(gradesHeightsSorted[grade]) - 1) * barWidth) / 2))

    lengths = []
    for bar in bars:
        lengths.append(len(bar))
    longestBar = bars[lengths.index(max(lengths))]

    return bars, tickPos, longestBar


def main(fileName):

    plt.figure().clear()

    barWidth = 0.3
    df, rows, columns, expectedCounts, observeds = loadData(fileName)
    gradesColors = getGradesColors(columns, rows, observeds)
    gradesHeightsSorted = getHeightsSorted(observeds, rows)
    bars, tickPos, longestBar = plotBars(observeds, rows, barWidth, gradesColors, gradesHeightsSorted)
    setupPlt(longestBar, rows, tickPos, columns)

    path = r'images\bar-freq.png'
    if os.path.exists(path):
        os.remove(path)
    plt.savefig(fname=path)
