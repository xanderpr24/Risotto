import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import _matplotlib0
import _math


root = tk.Tk()
root.title('Risotto')
window_width = 640
window_height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.iconbitmap('chisq.ico')

pValue = tk.StringVar()

def submitFilePath(path):
    found = False
    try:
        file = open(path, 'r')
        found = True
    except FileNotFoundError:
        showinfo(
            message=f'No such file or directory "{path}"'
        )

    if found:
        pValue = str(_math.main())
        print(pValue)

def generateRandomData():
    _matplotlib0.genData()

def enableDisableSubmit(*args):
    pathStatus = filePath.get()
    if pathStatus:
        submit.config(state='normal')
    else:
        submit.config(state='disabled')

def showPValue():
    pValueText = pValue.get()
    thing = ttk.Label(main, text=pValueText)
    thing.pack()

filePath = tk.StringVar()
filePath.trace('w', enableDisableSubmit)

main = ttk.Frame(root)
main.pack()

fileLabel = ttk.Label(main, text='Enter file path:')
fileLabel.pack()

fileEntry = ttk.Entry(main, textvariable=filePath)
fileEntry.pack()

submit = ttk.Button(main, text='Submit', command=lambda: submitFilePath(filePath.get()))
submit.pack(fill='x', expand=True)

showPValue = ttk.Button(main, text='Show Data', command=showPValue)
showPValue.pack()

pLabel = ttk.Label(main, text=pValue.get())
pLabel.pack()

root.mainloop()
