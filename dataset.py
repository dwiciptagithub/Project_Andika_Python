"""
    Example Controllers
"""

from project import app
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os
import csv

UPLOAD_FOLDER = './'
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(os.path.join(app.instance_path, 'excel_data'), exist_ok=True)


#route index
@app.route('/importdata', methods = ['GET'])
def importdata():
    return render_template('importdata.html')


@app.route('/uploadsuccess', methods=['POST'])
def success():
        if request.method == 'POST':
            f = request.files['upload']
            # get the file name and save it to a directory in folder "excel_data"
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            # Reading an excel file using Python 
            # Give the location of the file 
            loc= os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            # To open Workbook
            # wb = xlrd.open_workbook(loc)
            csv_data=csv.reader(open(loc))  
            return redirect(url_for('lihatdata'))  
        # return render_template('lihatdata.html')

@app.route('/lihatdata')
def lihatdata():

    datacsv = []

    with open('data.csv') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            datacsv.append(dict(row))
        
    # print(datacsv)
    # flash('You were successfully logged in')
    return render_template('lihatdata.html', datacsv=datacsv)
