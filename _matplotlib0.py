import matplotlib.pyplot as plt
import _pandas

def setupPlt(rows, columns, tickPos, catsPos, cats, barWidth, colors):
    plt.xlabel('Grade')
    plt.ylabel('Frequency')
    plt.title('Rating of School by Grade')
    plt.legend(labels=[row for row in rows])

    for column in columns:
        for row in range(len(rows)):
            plt.bar(catsPos[row], cats[row], label=rows[row], width=barWidth, color=colors[row], ec='k')

    plt.xticks(tickPos, columns)
    plt.legend(labels=[row for row in rows])


def loadFromPandas(barWidth):
    cats, catsPos = [], []
    cellValues, rows, columns = _pandas.main()
    cat1XPos = [i for i, _ in enumerate(columns)]

    tickPos = [val + (barWidth * (len(rows)-1)/2) for val in cat1XPos]

    for i, row in enumerate(rows):
        catsPos.append([])
        catsPos[i] = [val + (barWidth * i) for val in cat1XPos]

    for row in range(len(cellValues)):
        cats.append([])
        for cell in cellValues[row]:
            cats[row].append(cell)

    rows.sort()

    def byLen(item):
        return len(item)
    columns.sort(key=byLen)

    return cats, catsPos, cellValues, rows, columns, tickPos


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
    plt.show()

main()
