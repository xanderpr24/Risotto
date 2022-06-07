import _pandas
import json

def loadFromPandas(fileName):
    df, rows, columns = _pandas.main(fileName)
    expectedCounts = _pandas.getExpectedCounts(df)
    dOF = (len(rows) - 1) * (len(columns) - 1)

    return df, rows, columns, expectedCounts, dOF


def getOE(df, expectedCounts):
    observedsExpecteds = {}
    pairs = []
    for i in range(len(df)):
        pairs.append([])
        pairs[i].append(df.iloc[i][0])
        pairs[i].append(df.iloc[i][1])

    for pair in range(len(pairs)):
        id = ', '.join(pairs[pair])

        if not id in observedsExpecteds:
            observedsExpecteds[id] = []
            observedsExpecteds[id].append(pairs.count(pairs[pair]))
            observedsExpecteds[id].append(expectedCounts[id])

    return observedsExpecteds


def getStatistic(observedsExpecteds):
    unSums = []

    contributions = {}
    for id in observedsExpecteds:
        contributions[id] = (round(observedsExpecteds[id][0] - observedsExpecteds[id][1], 1))
        unSums.append(
            ((observedsExpecteds[id][0] - observedsExpecteds[id][1]) ** 2) / observedsExpecteds[id][1]
        )

    chi2 = sum(unSums)
    return chi2


def getP(jsonFile, df, statistic):
    df = str(df)
    tailProbs = [0.995, 0.990, 0.975, 0.95, 0.9, 0.75, 0.5, 0.25, 0.1, 0.05, 0.01, 0.005, 0.001]

    with open(jsonFile, 'r') as file:
        table = json.load(file)

    row = table[df]
    if not statistic in row:
        try:
            greaterIndex = row.index([value for value in row if value > statistic][0])
        except IndexError:
            return (0, 0.001)

        try:
            lessIndex = row.index([value for value in row if value < statistic][-1])
        except IndexError:
            return (0.995, 1)

        return tailProbs[greaterIndex], tailProbs[lessIndex]
    else:
        index = row.index(statistic)
        return tailProbs[index], tailProbs[index]


def main(fileName):
    data, rows, columns, expectedCounts, df = loadFromPandas(fileName)
    observedsExpecteds = getOE(data, expectedCounts)
    statistic = getStatistic(observedsExpecteds)

    pValue = getP('JSON/chi2-table0.json', df, statistic)
    return pValue
