import joblib
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

class Classification:
    def __init__(self) -> None:
        # self.classification_model = joblib.load('model/naive_bayes.pkl')
        self.classification_model = joblib.load('D:/sem9/program/TA_petakabar/bencana/main/model/classification/model.pkl')
        # self.scrapped_news = pd.read_csv('result/tagging/severity_count.csv')

        #ambil dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, sev_death, sev_injury, sev_house, sev_person FROM berita where berita_topik_id = 1 AND class_classification is null")
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
            
            # for i in range(0, self.scrapped_news.shape[0]):
            #     title = self.scrapped_news.iloc[i, 0]
            #     berita = self.scrapped_news.iloc[i, 1]
            #     time = self.scrapped_news.iloc[i, 2]
            #     what = self.scrapped_news.iloc[i, 3]
            #     tanggal_asli = self.scrapped_news.iloc[i, 4]
            #     orang = self.scrapped_news.iloc[i, 5]
            #     provinsi = self.scrapped_news.iloc[i, 6]
            #     kabupaten = self.scrapped_news.iloc[i, 7]
            #     kecamatan = self.scrapped_news.iloc[i, 8]
            self.meninggal = []
            self.luka = []
            self.rumah = []
            self.orang = []
            self.idberita = []
            
            if(len(self.newsscrapped)>0):
                self.idberita, self.meninggal, self.luka, self.rumah, self.orang = zip(*self.newsscrapped)
            
            for i in range(0, len(self.newsscrapped)):
                # try:
                mati = float(self.meninggal[i])
                luka = float(self.luka[i])
                rumah = float(self.rumah[i])
                korban = float(self.orang[i])

                idberita = self.idberita[i]

                """
                Bagian ini adalah indikator yang perlu disesuaikan untuk masing - masing topik
                """
                keparahan = self.classification_model.predict([[mati,luka, rumah, korban]])

                try:
                    self.save_to_mysql(idberita, keparahan[0])
                except Exception as e:
                    print(e)
                
            #     document_result.append([title, berita, time, what, tanggal_asli, orang, provinsi, kabupaten, kecamatan, mati, luka, rumah, korban, keparahan[0]])

            # writer = pd.DataFrame(document_result, columns=[
            #                     'title', 'description', 'time', 'what', 'when', 'who', 'provinsi', 'kabupaten / kota', 'kecamatan', 'mati', 'luka', 'rumah', 'orang','klasifikasi'], index=None)
            # writer.to_csv('result/classification_res/result_final.csv', index=False, sep=',')
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
        