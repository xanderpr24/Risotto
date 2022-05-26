# take out the trash

import os

for file in os.listdir('./__pycache__'):
    if file[-4:] == '.pyc':
        os.remove(f'./__pycache__/{file}')
