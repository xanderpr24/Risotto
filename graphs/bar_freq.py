import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
sys.path.insert(0, 'folder')
import _pandas
import _math

# call _pandas to get dataframe, expected counts, observed counts, graph rows, and graph columns
def loadData(fileName):

    df, rows, columns = _pandas.main(fileName)
    rows.sort()
    expectedCounts = _pandas.getExpectedCounts(df)
    observedsExpecteds = _math.getOE(df, expectedCounts)

    observeds = {}                                                                      # a dictionary of each cell in the contingency table and its observed counts in the sample
    for column in columns:

        for key in observedsExpecteds:                                                  # for each cell in the observedsExpecteds table
            id = key[key.index(', ') + 2:]                                              # id = graph column (e.g. 9th)
            if id == column:
                if not column in observeds:
                    observeds[column] = {}                                              # if id = current column in iterator and column has not been accounted for, add it to observeds dict

                observeds[column][key[:key.index(',')]] = (observedsExpecteds[key][0])  # add observed value to column dict in observeds dict

    return df, rows, columns, expectedCounts, observeds # dataframe, graph rows, graph columns, expected counts table as dict, observed counts table as dict


# get the color for each bar within each group
def getGradesColors(columns, rows, observeds):

    colors = {}                         # a dictionary for row will be assigned which colors
    for row in rows:                    # for each row in the dataframe (e.g. 1-2, 3-4, 5-6, 7-8, 9-10)
        colors[row] = {}
        colorsList = ['red', 'orange',  # the maximum number of colors for an entire bar
        'gold', 'forestgreen', 'blue']

    for it, row in enumerate(rows):
        colors[row] = colorsList[it]    # each row is given its correspondent color in colorsList

    groupsColors = {}                   # a dictionary of colors for bars for each row (e.g. 1-2, 3-4, 5-6, 7-8, 9-10) groups (e.g. 9th, 10th, 11th, 12th )
    for group in columns:
        groupColors = []                # a list of what colors will be assigned to this group
        for row in rows:
            if row in observeds[group]: # if this row has a bar in the group:
                groupColors.append(colors[row])  # add the color assigned to this row to this group

        groupsColors[group] = (groupColors)         # add colors for each bar to each grade

    return groupsColors     # dictionary of each color for each row for each group


# set up matplotlib graph (e.g. labels) without creating graphics
def setupPlt(legend, x_label, title, highestBar, longestBar, rows, tickPos, columns):
    plt.title(title)    # title of the graph

    if legend:
        plt.legend(longestBar, rows, loc='upper center') # give a value to the legend for each row and its color
    plt.xlabel(x_label)
    plt.ylabel('Frequency')
    plt.xticks(tickPos, columns)

    # set the step of the y-axis
    if highestBar >= 60:
        step = 4
    elif highestBar >= 20:
        step = 2
    else:
        step = 1
    if not highestBar % step == 0:
        highestBar += step - highestBar % step
    plt.yticks([i for i in range(0, highestBar, step)]) # add a tick for every step until top of graph


# sort each bar (e.g. 1-2, 3-4, 5-6, 7-8, 9-10) within each group (e.g. 9th, 10th, 11th, 12th)
def getHeightsSorted(observeds, rows):
    gradesHeightsSorted = {}            # a dictionary of heights for each bar for each group
    for counter, grade in enumerate(observeds):
        frequencies = {}                # height of each bar for each group
        for freq in observeds[grade]:   # for each height for each bar for each grade
            frequencies[freq] = observeds[grade][freq]

        heights = []
        heights = [frequencies for frequencies in frequencies.values()]
        heightsSorted = []  # sorted list of heights for each bar

        for row in rows:
            if row in frequencies:  # if group has a bar for this row
                heightsSorted.insert(rows.index(row), frequencies[row]) # add height to corresponding location in sorted list

        gradesHeightsSorted[grade] = heightsSorted  # add sorted list to dictionary of sorted heights for each grade

    return gradesHeightsSorted


# plot the bars on the matplotlib figure
def plotBars(observeds, columns, barWidth, gradesColors, gradesHeightsSorted):
    bars = []                                       # a list of bars (rectangles)
    tickPos = []

    barsHeights = []                                # the heights of bars for each group
    for counter, grade in enumerate(observeds):

        bar = plt.bar(
            2*counter + np.array([barWidth * i for i in range(len(gradesHeightsSorted[grade]))]),   # location of bars on x-axis
            [value for value in gradesHeightsSorted[grade]],                                        # heights of bars
            BAR_WIDTH,                                                                              # width of bars
            color = gradesColors[grade],                                                            # color for each bar
            ec = 'k',                                                                               # black outline for each bar
            label=columns[counter]                                                                  # label in legend
        )
        bars.append(bar.patches)        # add rectangle to bars list
        tickPos.append(2*counter + (((len(gradesHeightsSorted[grade]) - 1) * barWidth) / 2))        # set x tick location to center of group

        for height in gradesHeightsSorted[grade]:
            barsHeights.append(height)  # add int height of bar to barsHeights list

    highestBar = max(barsHeights) + 1

    lengths = []
    for bar in bars:
        lengths.append(len(bar))
    longestBar = bars[lengths.index(max(lengths))]  # largest bar height is the height of the tallest bar

    return bars, tickPos, longestBar, highestBar


def main(fileName, title, x_label, legend):

    plt.figure().clear()    # clear figure of previous plots

    BAR_WIDTH = 0.3
    df, rows, columns, expectedCounts, observeds = loadData(fileName)
    gradesColors = getGradesColors(columns, rows, observeds)
    gradesHeightsSorted = getHeightsSorted(observeds, rows)
    bars, tickPos, longestBar, highestBar = plotBars(observeds, columns, BAR_WIDTH, gradesColors, gradesHeightsSorted)
    setupPlt(legend, x_label, title, highestBar, longestBar, rows, tickPos, columns)

    path = r'static\bar-freq.png'   # path to save image to
    if os.path.exists(path):        # delete image if it exists
        os.remove(path)
    plt.savefig(fname=path)         # save image
