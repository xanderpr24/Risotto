import json
import random

with open('JSON/teachers.json', 'r') as file:
    teachers = json.load(file)

chosen = {9 : [], 10 : [], 11 : [], 12 : []}
for grade in teachers:
    chosen[int(grade)] = tuple(random.choices(teachers[grade], k=2))

print(chosen)
