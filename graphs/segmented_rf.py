import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import _pandas
import _math


def getRowsColumnsTotals(df):
    rowsTotals, columnsTotals, pairs = {}, {}, []
    #set each list in pairs to the data from the dataframe
    for i in range(len(df)):
        pairs.append([])
        pairs[i].append(df.iloc[i][0])
        pairs[i].append(df.iloc[i][1])

    #initialize each cell from the contingency table in a dictionary, then increment the dictionary value to the number of occurences in the dataframe
    for pair in pairs:
        if not pair[0] in rowsTotals:
            rowsTotals[pair[0]] = 1
        else:
            rowsTotals[pair[0]] += 1

        if not pair[1] in columnsTotals:
            columnsTotals[pair[1]] = 1
        else:
            columnsTotals[pair[1]] += 1

    return rowsTotals, columnsTotals


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

    return df, rows, columns, observeds


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


def setupPlt(longestBar, bars, rows, columns):
    plt.title('School Rating by Grade')
    plt.legend(longestBar, rows, loc='upper center')
    plt.xlabel('Grade')
    plt.ylabel('Relative Frequency')
    plt.xticks([i for i in range(len(columns))], columns)
    plt.yticks([i * 10 for i in range(12)])


def getHeightsSorted(observeds, rows, columnsTotals):
    gradesHeightsSorted = {}
    for counter, grade in enumerate(observeds):

        percents = {}
        for freq in observeds[grade]:
            percents[freq] = observeds[grade][freq] / columnsTotals[grade]

        heights = []
        heights = [percent * 100 for percent in percents.values()]
        heightsSorted = []

        for rating in rows:
            if not rating in percents:
                heightsSorted.insert(rows.index(rating), 0)
            else:
                heightsSorted.insert(rows.index(rating), percents[rating])

        for i in range(len(heightsSorted)):
            heightsSorted[i]  = heightsSorted[i] * 100

        gradesHeightsSorted[grade] = heightsSorted

    return gradesHeightsSorted


def plotBars(observeds, rows, barWidth, gradesColors, gradesHeightsSorted):
    bars = []
    for counter, grade in enumerate(observeds):
        heightsSorted = gradesHeightsSorted[grade]

        bottoms = [top for top in heightsSorted][:-1]
        for i in range(len(bottoms)):
            if i >= 1:
                bottoms[i] += bottoms[i - 1]
        bottoms.insert(0, 0)

        colors = {
            '1-2'   : 'red',
            '3-4'   : 'orange',
            '5-6'   : 'gold',
            '7-8'   : 'forestgreen',
            '9-10'  : 'blue'
        }

        bar = plt.bar(
            counter,
            [value for value in heightsSorted],
            barWidth,
            bottoms,
            color = colors.values(),
            ec = 'k',
            label=rows[counter]
        )
        for i in range(len(bottoms)):
            if heightsSorted[i] != 0:
                plt.text(counter - barWidth/3, bottoms[i] + heightsSorted[i]/2 - 2, f'{int(heightsSorted[i])}%')
        bars.append(bar.patches)

    lengths = []
    for bar in bars:
        lengths.append(len(bar))
    longestBar = bars[lengths.index(max(lengths))]

    return bars, longestBar


def main(fileName):

    plt.figure().clear()

    barWidth = 0.3
    df, rows, columns, observeds = loadData(fileName)
    rowsTotals, columnsTotals = getRowsColumnsTotals(df)
    gradesColors = getGradesColors(columns, rows, observeds)
    gradesHeightsSorted = getHeightsSorted(observeds, rows, columnsTotals)
    bars, longestBar = plotBars(observeds, rows, barWidth, gradesColors, gradesHeightsSorted)
    setupPlt(longestBar, bars, rows, columns)

    path = r'images\segmented-rf.png'
    if os.path.exists(path):
        os.remove(path)
    plt.savefig(fname=path)
