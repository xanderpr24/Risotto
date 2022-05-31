# packages
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import os
import sys

# other .py files
sys.path.insert(0, 'funs')
sys.path.insert(0, 'graphs')
import funs
import _pandas
import bar_freq
import segmented_rf
import unsegmented_rf


# clear images directory; delete all pre-existing graphs
for i in ('bar-freq', 'segmented-rf', 'unsegmented-rf'):
    if os.path.exists(f'images/{i}.png'):
        os.remove(f'images/{i}.png')


# set up Tkinter window
bg_color = '#fdf7e7'
fg_color = '#f66'
root = tk.Tk()
root.resizable(False, False)
root.title('Risotto')
root.configure(bg=bg_color)
root.rowconfigure(1, weight=1)
frame = tk.Frame(root, bg=bg_color, width=450)
frame.pack(expand=True)
style = ('Verdana', 12)

# center window on screen
x = int((root.winfo_screenwidth()/2) - 225)
y = int((root.winfo_screenheight()/2) - 75)
root.geometry('%sx%s+%s+%s' % (450, 150, x, y))

# declare path variable to store file location
path = tk.StringVar()

# save graph as image via main() function
# display image via showImage() function
# if file cannot be found, alert user
def bar_graph_clicked(path):
    try:
        bar_freq.main(path)
        funs.showImage(r'images\bar-freq.png', 'Frequency Graph')
    except IOError:
        showinfo(message=f'No such file \'{path}\' on current path')

def segmented_rf_clicked(path):
    try:
        segmented_rf.main(path)
        funs.showImage(r'images\segmented-rf.png', 'Segmented Relative Frequency')
    except IOError:
        showinfo(message=f'No such file \'{path}\' on current path')

def unsegmented_rf_clicked(path):
    try:
        unsegmented_rf.main(path)
        funs.showImage(r'images\unsegmented-rf.png', 'Relative Frequency Graph')
    except IOError:
        showinfo(message=f'No such file \'{path}\' on current path')


# buttons/entry fields
path_label = tk.Label(frame, text="File path:", font=style, bg=bg_color, fg=fg_color)
path_label.grid(row=0, column=0)

# store path var as string entered
path_entry = ttk.Entry(frame, textvariable=path)
path_entry.grid(row=0, column=1, columnspan=3)
path_entry.focus()

# call graph display functions on-click
bar_freq_button = tk.Button(frame, text="Frequency\nBar Graph", command=lambda: bar_graph_clicked(path.get()), font=('Verdana', 10), bg=fg_color, fg=bg_color)
bar_freq_button.grid(row=2, column=0, padx=2, pady=5)

segmented_rf_button = tk.Button(frame, text="Segmented\nRF", command=lambda: segmented_rf_clicked(path.get()), font=('Verdana', 10), bg=fg_color, fg=bg_color)
segmented_rf_button.grid(row=2, column=1, padx=2, pady=5)

unsegmented_rf_button = tk.Button(frame, text='Unsegmented\nRF', command=lambda: unsegmented_rf_clicked(path.get()), font=('Verdana', 10), bg=fg_color, fg=bg_color)
unsegmented_rf_button.grid(row=2, column=2, padx=2, pady=5)

root.mainloop()
