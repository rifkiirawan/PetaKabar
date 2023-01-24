import joblib
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

class Classification:
    def __init__(self) -> None:
        # self.classification_model = joblib.load('model/classification/model.pkl')
        self.classification_model = joblib.load('D:/sem9/program/TA_petakabar/kesehatan/main/model/classification/model.pkl')

        #ambil dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, sev_death, sev_injury FROM berita where berita_topik_id = 4 AND class_classification is null")
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

    def getClassificationValue(self):
        try:
            self.meninggal = []
            self.luka = []
            self.idberita = []
            
            if(len(self.newsscrapped)>0):
                self.idberita, self.meninggal, self.luka = zip(*self.newsscrapped)
            
            for i in range(0, len(self.newsscrapped)):
                mati = self.meninggal[i]
                sakit = self.luka[i]
                idberita = self.idberita[i]

                """
                Bagian ini adalah indikator yang perlu disesuaikan untuk masing - masing topik
                """
                keparahan = self.classification_model.predict([[mati,sakit]])
                if(keparahan[0]==1):
                    keparahan_text = 'rendah'
                elif(keparahan[0]==2):
                    keparahan_text = 'sedang'
                elif(keparahan[0]==3):
                    keparahan_text = 'parah'
                
                self.save_to_mysql(idberita, keparahan_text)
            return "success"
        except: 
            return "error"
    def save_to_mysql(self, idberita, keparahan):
        try:
            conn = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cur = conn.cursor()
            add_news = ("UPDATE berita "
                        "SET class_classification = %s "
                    "WHERE ID = %s"
                    )
            data_news = (keparahan, idberita)

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