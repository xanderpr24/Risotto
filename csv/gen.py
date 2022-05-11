import random

var1 = ['1-2', '3-4', '5-6', '7-8', '9-10']
var2 = ['9th', '10th', '11th', '12th']

file = open('csv/movies.csv', 'w')

for i in range(150):
    phrase = f'{random.choice(var1)},{random.choice(var2)}\n'
    file.write(phrase)

file.close()
