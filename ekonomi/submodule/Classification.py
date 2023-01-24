import joblib
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

class Classification:
    def __init__(self) -> None:
        # self.classification_model = joblib.load('model/classification/modelklasifikasi.pkl')
        self.classification_model = joblib.load('D:/sem9/program/TA_petakabar/ekonomi/model/classification/modelklasifikasi.pkl')
        # self.scrapped_news = pd.read_csv('result/tagging/severity_count.csv')

        # ambil dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, sev_moneyUSD, sev_moneyIDR, sev_persen, sev_inflasi FROM berita where berita_topik_id = 2 AND class_classification is null")
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
        document_result = []
        try:
            self.moneyUSD = []
            self.moneyIDR = []
            self.persen = []
            self.inflasi = []
            self.idberita = []
            
            if(len(self.newsscrapped)>0):
                self.idberita, self.moneyUSD, self.moneyIDR, self.persen, self.inflasi = zip(*self.newsscrapped)
            
            # for i in range(0, self.scrapped_news.shape[0]):
            #     title = self.scrapped_news.iloc[i, 0]
            #     berita = self.scrapped_news.iloc[i, 1]
            #     time = self.scrapped_news.iloc[i, 2]
            #     what = self.scrapped_news.iloc[i, 3]
            #     tanggal_asli = self.scrapped_news.iloc[i, 4]
            #     orang = self.scrapped_news.iloc[i, 5]
            #     negara = self.scrapped_news.iloc[i, 6]
            #     provinsi = self.scrapped_news.iloc[i, 7]
            #     kabupaten = self.scrapped_news.iloc[i, 8]
            #     kecamatan = self.scrapped_news.iloc[i, 9]

            for i in range(0, len(self.newsscrapped)):
                idberita = self.idberita[i]

                moneyUSD = self.moneyUSD[i]
                moneyUSD = float(moneyUSD)

                moneyIDR = self.moneyIDR[i]
                moneyIDR = float(moneyIDR)

                persen = self.persen[i]
                persen = float(persen)

                inflasi = self.inflasi[i]
                inflasi = float(inflasi)


                """
                Bagian ini adalah indikator yang perlu disesuaikan untuk masing - masing topik
                """
                keparahan = self.classification_model.predict([[moneyUSD,moneyIDR, persen, inflasi]])
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