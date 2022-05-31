import pandas as pd


def loadData(fileName): #set up and return Python data from csv/txt extension
    file = open(fileName, 'r')
    row, col = [], []

    for line in file:
        lineInfo = line.strip('\n').split(',')
        row.append(lineInfo[0])
        col.append(lineInfo[1])

    return row, col


def displayCrossTab(df, margins): #returns a two-way contingency table from a given Pandas dataframe
    if margins:
        #change df.[Row], df.[Column] for different data
        crosstab = pd.crosstab(df.Rating, df.Grade, margins=True, margins_name='Total')
    else:
        crosstab = pd.crosstab(df.Rating, df.Grade)

    return crosstab


def getExpectedCounts(df): #return chi2 expected counts values for each cell in a given contingency table
    expectedCounts, rowsTotals, columnsTotals, pairs = {}, {}, {}, []

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

    #initialize a new dictionary whose values represent the chi2 expected counts for each cell
    for row in rowsTotals:
        for column in columnsTotals:
            expectedCounts[f'{row}, {column}'] = round((rowsTotals[row] * columnsTotals[column]) / len(df), 1)

    return expectedCounts



def main(fileName):

    columnsRows = [[], []]

    var1, var2 = loadData(fileName)

    #change for different data
    data = {
        'Class' : var1,
        'Rating' : var2
    }

    df = pd.DataFrame(data) #initialize Pandas dataframe based on data from external file

    #initialize columns and rows for _matplotlib
    for i, item in enumerate(data):
        for value in data[item]:
            if not value in columnsRows[i]:
                columnsRows[i].append(value)

    return df, columnsRows[0], columnsRows[1]
