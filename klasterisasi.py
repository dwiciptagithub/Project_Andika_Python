from project import app
from flask import render_template, redirect, url_for, request, send_file
import pandas as pd
from sklearn_extra.cluster import KMedoids
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np
import io





@app.route('/hitungcluster', methods=['POST', 'GET'])
def hitungcluster():
    if request.method == 'GET':
        return render_template('hitungcluster.html')

    if request.method == 'POST':
        input_val = int(request.form['jumlah_klaster'])
        # contacts = pd.read_csv('data_afterTransform (normalisasi).csv')
        # contacts = np.array(reader)
        with open('data_afterTransform (normalisasi).csv') as data:
            contacts = np.loadtxt(data, delimiter=",", dtype='float')

        kmedoids = KMedoids(n_clusters=input_val, random_state=1125)
        kmedoids.fit(contacts)
        
        dnama = []
        with open('nama.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                dnama.append(dict(row))
        dnama2 = pd.DataFrame(dnama)
        data = pd.DataFrame(contacts)
        x = data.assign(
            cluster1 = kmedoids.predict(contacts),
            dnama3 = dnama2,
            # cluster2 = kmedoids2.predict(contacs),
        )
        y = pd.DataFrame(x)
        y.columns = ['Jumlah Mahasiswa', 'Jumlah Dosen', 'Jumlah Program Studi', 'Fasilitas Olahraga', 'Wisma/Asrama/Hotel', 'Teknologi Informasi', 'Public Area', 'PERS Mahasiswa', 'Asuransi', 'Gedung Pertemuan', 'Laboratorium', 'Poliklinik', 'Bus Kampus', 'Kalender Pendidikan', 'Pusat Pelatihan Bahasa', 'Perpustakaan', 'Sarana Ibadah', 'Free Hotspot', 'Jumlah Fasilitas', 'Bus Umum', 'Restaurant', 'Tempat Ibadah', 'Kos/Asrama/Hotel', 'Terminal Bus', 'Cafe', 'Tempat Olahraga', 'Bandara', 'Mall', 'Rumah Sakit', 'Stasiun Kereta', 'Supermarket', 'Apotek', 'Jumlah Tempat Umum Terdekat', 'Akreditasi', 'Ranking Nasional', 'Cluster', 'Nama Perguruan Tinggi']
        datacsv = y.to_dict('records')
        return render_template("hitungcluster.html", data=datacsv)


# def piecluster():
    # new_list = list(y.items())

    # fig = plt.figure(figsize =(10, 7))
    # ax = plt.title("Results Cluster", pad=20)
    # plt.pie(new_list, labels = y.columns)
    # img = io.BytesIO()
    # fig.savefig(img)
    # img.seek(0)
    # return send_file(img, mimetype=('img, png'))


@app.route('/lihatcluster', methods=['POST', 'GET'])
def lihatcluster():
    if request.method == 'GET':
        return render_template('lihatcluster.html')

    if request.method == 'POST':
        input_val = int(request.form['jumlah_klaster'])
        # contacts = pd.read_csv('data_afterTransform (normalisasi).csv')
        # contacts = np.array(reader)
        with open('data_afterTransform (normalisasi).csv') as data:
            contacts = np.loadtxt(data, delimiter=",", dtype='float')

        kmedoids = KMedoids(n_clusters=input_val, random_state=1125)
        kmedoids.fit(contacts)
        
        dnama = []
        with open('nama.csv') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                dnama.append(dict(row))
        dnama2 = pd.DataFrame(dnama)
        data = pd.DataFrame(contacts)
        x = data.assign(
            cluster1 = kmedoids.predict(contacts),
            dnama3 = dnama2,
            # cluster2 = kmedoids2.predict(contacs),
        )
        y = pd.DataFrame(x)
        y.columns = ['Jumlah Mahasiswa', 'Jumlah Dosen', 'Jumlah Program Studi', 'Fasilitas Olahraga', 'Wisma/Asrama/Hotel', 'Teknologi Informasi', 'Public Area', 'PERS Mahasiswa', 'Asuransi', 'Gedung Pertemuan', 'Laboratorium', 'Poliklinik', 'Bus Kampus', 'Kalender Pendidikan', 'Pusat Pelatihan Bahasa', 'Perpustakaan', 'Sarana Ibadah', 'Free Hotspot', 'Jumlah Fasilitas', 'Bus Umum', 'Restaurant', 'Tempat Ibadah', 'Kos/Asrama/Hotel', 'Terminal Bus', 'Cafe', 'Tempat Olahraga', 'Bandara', 'Mall', 'Rumah Sakit', 'Stasiun Kereta', 'Supermarket', 'Apotek', 'Jumlah Tempat Umum Terdekat', 'Akreditasi', 'Ranking Nasional', 'Cluster', 'Nama Perguruan Tinggi']
        datacsv = y.to_dict('records')

        # otomatis
        c = []
        b = []
        mylabels = []
        for i in range(input_val):
            c.append(y[y['Cluster'] == i]['Nama Perguruan Tinggi'].count())
            if (input_val==4):
                mylabels = ["Kurang Diminati", "Cukup Diminati", "Sangat Diminati", "Tidak Diminati"]
            if (input_val==2):
                mylabels = ["Sangat Diminati", "Tidak Diminati"]
            if (input_val==3):
                mylabels = ["Diminati", "Tidak Diminati", "Sangat Diminati"]
            b.append("cluster" + str(i) + str(":") + str(mylabels[i]))

        # datacsv = a.to_dict('records')
        fig,ax = plt.subplots(figsize=(10,7))
        ax = plt.title("Persentase & interpretasi hasil cluster Perguruan Tinggi Swasta", pad=20)
        plt.pie(c, labels=b, autopct='%2.1f%%')
        plt.legend()
        img = io.BytesIO()
        fig.savefig(img)
        img.seek(0)
        return send_file(img, mimetype=('img, png'))