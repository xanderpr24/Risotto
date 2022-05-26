import json
import random

with open('JSON/teachers.json', 'r') as file:
    teachers = json.load(file)

chosen = {}
for grade in teachers:
    chosen[int(grade)] = tuple(random.choices(teachers[grade], k=2))

print(chosen)
