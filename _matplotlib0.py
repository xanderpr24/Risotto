import matplotlib.pyplot as plt
import _pandas
import random

def setupPlt(rows, columns, tickPos, catsPos, cats, barWidth, colors): #label plot (axes/title) and add legend and x-scale

    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.title('Rating of School by Grade')
    plt.legend(labels=[row for row in rows])

    #plot frequency  for each cell from contingency table
    for column in columns:
        for row in range(len(rows)):
            plt.bar(catsPos[row], cats[row], label=rows[row], width=barWidth, color=colors[row], ec='k')

    plt.xticks(tickPos, columns)
    plt.legend(labels=[row for row in rows]) #each var2 value from external file gets a legend label


def loadFromPandas(barWidth): #get data from pandas and initialize for different format
    cats, catsPos = [], []
    cellValues, rows, columns = _pandas.main()
    cellValues = _pandas.displayCrossTab(cellValues, False).values

    cat1XPos = [i for i, _ in enumerate(columns)] #0, 1, 2, ..., len(columns)-1

    tickPos = [val + (barWidth * (len(rows)-1)/2) for val in cat1XPos] #center tick for multiple bars

    #individual position for each category
    for i, row in enumerate(rows):
        catsPos.append([])
        catsPos[i] = [val + (barWidth * i) for val in cat1XPos]

    #cell values for each category
    for row in range(len(cellValues)):
        cats.append([])
        for cell in cellValues[row]:
            cats[row].append(cell)

    #sort rows/columns on plot, column sorting may be subject to change for different data
    rows.sort()

    #data specific?
    def byLen(item):
        dig = ''
        for char in item:
            if char.isdigit():
                dig += char
        return int(dig)
    columns.sort(key=byLen)

    return cats, catsPos, cellValues, rows, columns, tickPos


def genData(var1, var2): #generate random data for specified possible outcomes for each of two variables

    file = open('csv/movies.csv', 'w')

    for i in range(150):
        phrase = f'{random.choice(var1)},{random.choice(var2)}\n' #write random data (e.g. yes,male/no,female) to the file
        file.write(phrase)

    file.close()



def main():

    barWidth = 0.15
    colors = {
        0 : 'r',
        1 : 'g',
        2 : 'b',
        3 : 'y',
        4 : '0',
    }
    cats, catsPos, cellValues, rows, columns, tickPos = loadFromPandas(barWidth)
    setupPlt(rows, columns, tickPos, catsPos, cats, barWidth, colors)

    #generate random data for grades 9-12 and ratings 1-10
    genData(
        ['1-2', '3-4', '5-6', '7-8', '9-10'],
        ['9th', '10th', '11th', '12th']
    )

    #plt.show()
