'''
Alexander Melby
Honors Computer Programming
Period 4
Final Project: Risotto
Purpose: Statistical Analysis with HTML GUI
'''

'''
Most of what I learned about Flask during the project: https://www.bing.com/search?q=everything%20you%20need\
%20to%20know%20about%20flask&qs=n&form=QBRE&=%25eManage%20Your%20Search%20History%25E&sp=-1&pq=everything%20\
you%20need%20to%20know%20about%20&sc=8-34&sk=&cvid=8E1D0AFEEA664C0CB0A1ED646C5CD2A0
Most of what I learned about Matplotlib during the project: https://www.w3schools.com/python/matplotlib_intro.asp
'''

#import dependencies
from flask import Flask, redirect, url_for, request, render_template
import sys
sys.path.insert(0, 'graphs') #add 'graphs' folder onto project path
import bar_freq
import segmented_rf
import unsegmented_rf

app = Flask(__name__) #create instance of Flask object

@app.route('/') #localhost traffic routes to this function
def risotto():

    return render_template('risotto.html') #returns and writes localhost HTML to string conversion of templates/risotto.html

@app.route('/templates/loading', methods=['GET', 'POST']) #localhost/templates/loading traffic routes to this function
def out():

    if request.method == 'POST': #if data is being fetched from server:

        #retrieve csv path, graph title, and x-label from HTML inputs
        entries = dict(request.form)
        path = entries['path']
        title = entries['title']
        x_label = entries['x-label']

        #if legend checkbox in templates/risotto.html was filled, legend = True, else, False
        try:
            legend = entries['legend']
        except KeyError:
            legend = False

        #if the file is found, save the graphs to static folder
        try:
            bar_freq.main(path, title, x_label, legend)
            segmented_rf.main(path, title, x_label, legend)
            unsegmented_rf.main(path, title, x_label, legend)
        except FileNotFoundError: #otherwise, redirect to templates/file-not-found.html
            return render_template('file-not-found.html')

    return render_template('results.html') #finally, display templates/results.html


if __name__ == '__main__': #run the program
    app.run(debug=True)
