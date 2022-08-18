
from project import app
from flask import render_template, redirect, url_for, request, send_file, flash
import pandas as pd
from sklearn_extra.cluster import KMedoids
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import io
from sklearn import metrics






@app.route('/hitungevaluasi', methods=['POST', 'GET'])
def hitungevaluasi():
    if request.method == 'GET':
         return render_template('hitungevaluasi.html')

    if request.method == 'POST':
        input_val_dari = int(request.form['dari'])
        # input_val_sampai = int(request.form['sampai'])
        # if (input_val_dari>input_val_sampai):
        #     flash("Wrong input! Try again")
        #     return render_template('hitungevaluasi.html')
        datacsv = []
        reader = pd.read_csv('data_afterTransform (normalisasi).csv')
        data1 = pd.DataFrame(reader)


        k = []
        silhouette = []
        cluster = range(1, 2)
        for i in cluster:
            labels=KMedoids(n_clusters=input_val_dari, init="k-medoids++", random_state=1000).fit(data1).labels_
            # str(i) + " is " + str(metrics.silhouette_score(data1, labels, metric="euclidean", sample_size=1000, random_state=200)))
            k.append(str(input_val_dari))
            silhouette.append(str(metrics.silhouette_score(data1, labels, metric="euclidean", sample_size=872, random_state=1000)))

        k1 = pd.DataFrame(k)
        s1 = pd.DataFrame(silhouette)
        gabung = k1.assign(
            s2 = s1,
        )
        x = pd.DataFrame(gabung)
        x.columns=['K', 'Silhouette']
        gabung1 = x.to_dict('records')
        # s2 = s1.to_dict('records')
        # k2 = k1.to_dict('records')
        
        # print(k2)
        print(gabung1)
        return render_template("hitungevaluasi.html", data = gabung1)

@app.route('/visualize', methods=['POST', 'GET'])
def visualize():
        if request.method == 'GET':
            return render_template('visualisasi.html')

        if request.method == 'POST':
            input_val_dari = int(request.form['dari'])
            input_val_sampai = int(request.form['sampai'])
            if (input_val_dari>input_val_sampai):
                flash("Wrong input! Try again")
                return render_template('visualisasi.html')
            datacsv = []
            reader = pd.read_csv('data_afterTransform (normalisasi).csv')
            data1 = pd.DataFrame(reader)

            k = []
            silhouette = []
            cluster = range(input_val_dari,input_val_sampai)
            for i in cluster :
                labels=KMedoids(n_clusters=i, init="k-medoids++", random_state=1000).fit(data1).labels_
                # str(i) + " is " + str(metrics.silhouette_score(data1, labels, metric="euclidean", sample_size=1000, random_state=200)))
                k.append(str(i))
                silhouette.append((metrics.silhouette_score(data1, labels, metric="euclidean", sample_size=872, random_state=1000)))

            fig,ax = plt.subplots(figsize=(10,7))
            ax = sns.set_style(style="darkgrid")
            ax = plt.title("Silhouete Coefficient", pad=20)
            ax = plt.xlabel("K")
            ax = plt.ylabel("Silhouette Score")
            # ax.scatter([K], [sse])
            # sns.countplot(k, silhouette)
            # plt.plot("bx-")
            plt.bar(cluster, silhouette, color ='gray', width = 0.4)
            canvas = FigureCanvas(fig)
            img = io.BytesIO()
            fig.savefig(img)
            img.seek(0)
            return send_file(img, mimetype=('img, png'))