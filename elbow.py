
from project import app
from flask import render_template, redirect, url_for, request, send_file, flash
import pandas as pd
from sklearn_extra.cluster import KMedoids
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import io

@app.route('/hitungelbow', methods=['POST', 'GET'])
def hitungelbow():
    if request.method == 'GET':
        return render_template('hitungelbow.html')

    if request.method == 'POST':
        input_val_dari = int(request.form['dari'])
        input_val_sampai = int(request.form['sampai'])
        if (input_val_dari>input_val_sampai):
            flash("Wrong input! Try again")
            return render_template('hitungelbow.html')
        datacsv = []
        reader = pd.read_csv('data_afterTransform (normalisasi).csv')
        # pop  = reader.pop(0)
        # print(pop)
        sse = []
        # dari = input_val_dari
        # sampai = input_val_sampai
        # print (dari)
        # print (sampai)
        

        K = range(input_val_dari,input_val_sampai)
        for k in K:
            km = KMedoids(n_clusters=k, random_state=1125)
            km = km.fit(reader)
            sse.append(km.inertia_)
        
        # plt.plot(K, sse, 'bx-')
        # plt.xlabel('k')
        # plt.ylabel('SSE')
        # plt.title('Elbow Method For Optimal k')
        fig,ax = plt.subplots(figsize=(10,7))
        # ax = sns.set_style(style="darkgrid")
        ax = plt.title("Elbow For K Optimal", pad=20)
        ax = plt.xlabel("K")
        ax = plt.ylabel("SSE")
        plt.plot(K, sse, "-bo", label="line with marker")
        plt.legend()
        # ax.scatter([K], [sse])
        # sns.lineplot(K, sse)
        # plt.plot("bx-")
        canvas = FigureCanvas(fig)
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype=('img, png'))