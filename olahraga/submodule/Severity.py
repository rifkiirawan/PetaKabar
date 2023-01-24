from typing import Dict, List
from xmlrpc.client import boolean
from nltk.tag import CRFTagger
import pandas as pd
from nltk import word_tokenize
import re
import random
from typing import List
import mysql.connector
from mysql.connector import errorcode


class Severity:
    def __init__(self) -> None:
        self.ct =CRFTagger()
        # self.ct.set_model_file('model/TagIndo/all_indo_man_tag_corpus_model.crf.tagger')
        self.ct.set_model_file('D:/sem9/program/TA_petakabar/olahraga/model/TagIndo/all_indo_man_tag_corpus_model.crf.tagger')
        
        #ambil data dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, berita_desc FROM berita where berita_topik_id = 6 AND class_classification is null")
            myresult = cursor.fetchall()
            for row in myresult:
                self.newsscrapped.append(row)

        except mysql.connector.Error as err:
              if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
              elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
              else:
                print(err)
        else:
            cursor.close()
            cnx.close()

    def __preprocessingKeparahan(self, berita: str):
        s = berita
        s = s.replace('\n', ' ')
        s = s.replace('\r', ' ')
        s = re.sub("\(.*?\)", "", s)
        # s = s.lower()
        tokens = word_tokenize(s)
        return (' ').join(tokens)
    

    def getKeparahanVelue(self):
        try:
            document_result = []
            self.descberita = []
            self.idberita = []

            if(len(self.newsscrapped)>0):
                self.idberita, self.descberita = zip(*self.newsscrapped)
            for i in range(0, len(self.newsscrapped)):
                berita = self.descberita[i]
                idberita = self.idberita[i]

                internasional_indeks = ['motogp', 'asian games', 'aff', 'olimpiade',
                                        'piala asia', 'bwf', 'nba', 'sea games', 'indonesia open', 'indonesia masters']
                nasional_indeks = ['pon', 'piala presiden', 'liga 2', 'liga 1', 'liga 3', 'ibl', 'proliga',
                                   'liga mahasiswa', 'liga mahasiswa', 'turnamen pramusim', 'pp pbsi', 'dbl', 'fiba']
                provkota_indeks = ['airlangga challenge', 'tiga pilar']
                kejuaraans = [internasional_indeks] + [nasional_indeks] + [provkota_indeks]

                index = []
                word = self.__preprocessingKeparahan(berita)

                inte = 0
                nasional = 0
                prov = 0

                for n in range(0, len(kejuaraans)):
                    for co in range(0, len(kejuaraans[n])):
                        if n == 0:
                            jumlah = word.count(internasional_indeks[co])
                            inte = inte + jumlah
                        if n == 1:
                            jumlah = word.count(nasional_indeks[co])
                            nasional = nasional + jumlah
                        if n == 2:
                            jumlah = word.count(provkota_indeks[co])
                            prov = prov + jumlah
                index.append([inte, nasional, prov])

                # judul = []
                # deskripsi = []
                # internasional = []
                # nasional = []
                # provkota = []
                for m in range(0, len(index)):
                    self.save_to_mysql(idberita, index[m][0], index[m][1], index[m][2])
            return "success"
        except:
            return "error"
            
    def save_to_mysql(self, idberita, internasional, nasional, provkota):
        try:
            conn = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cur = conn.cursor()
            add_news = ("UPDATE berita "
                        "SET sev_internasional = %s, sev_nasional = %s, sev_provkota = %s "
                    "WHERE ID = %s"
                    )
            data_news = (internasional, nasional, provkota, idberita)

            cur.execute(add_news, data_news)
            conn.commit()            
            cur.close()
            conn.close()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
