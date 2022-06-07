#modified from https://www.askpython.com/python/examples/display-images-using-python
import sys
import cv2

def showImage(fileName, title):
    img = cv2.imread(fileName, cv2.IMREAD_ANYCOLOR)

    keyPressed = False

    while not keyPressed:
        cv2.imshow(title, img)
        cv2.waitKey(0)
        keyPressed = True

    try:
        cv2.destroyWindow(title) # destroy all windows
    except cv2.error:
        pass


def genData(var1, var2): #generate random data for specified possible outcomes for each of two variables

    file = open('csv/ratings-random.csv', 'w')

    for i in range(150):
        phrase = f'{random.choice(var1)},{random.choice(var2)}\n' #write random data (e.g. yes,male/no,female) to the file
        file.write(phrase)

    file.close()
