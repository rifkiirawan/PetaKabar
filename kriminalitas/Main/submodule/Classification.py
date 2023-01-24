import joblib
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
class Classification:
    def __init__(self) -> None:
        # self.classification_model = joblib.load('model/classification/model.pkl')
        self.classification_model = joblib.load('D:/sem9/program/TA_petakabar/kriminalitas/Main/model/classification/model.pkl')

        #ambil dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, sev_death, sev_injury, sev_lost_items, sev_lost_money, sev_rape FROM berita where berita_topik_id = 5 AND class_classification is null")
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
            # document_result = []
            self.meninggal = []
            self.luka = []
            self.lost_items = []
            self.lost_money = []
            self.rape = []
            self.idberita = []

            if(len(self.newsscrapped)>0):
                self.idberita, self.meninggal, self.luka, self.lost_items, self.lost_money, self.rape = zip(*self.newsscrapped)
            
            for i in range(0, len(self.newsscrapped)):
                mati = self.meninggal[i]
                mati = float(mati)

                luka = self.luka[i]
                luka = float(luka)

                kerugianBarang = self.lost_items[i]
                kerugianBarang = float(kerugianBarang)

                kerugianUang = self.lost_money[i]
                kerugianUang = float(kerugianUang)

                pemerkosaan = self.rape[i]
                pemerkosaan = float(pemerkosaan)

                idberita = self.idberita[i]

                """
                Bagian ini adalah indikator yang perlu disesuaikan untuk masing - masing topik
                """

                keparahan = self.classification_model.predict([[mati,luka, kerugianBarang, kerugianUang, pemerkosaan]])
                self.save_to_mysql(idberita, keparahan[0])
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