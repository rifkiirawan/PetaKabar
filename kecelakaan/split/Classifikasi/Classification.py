import joblib
# from sklearn.tree import DecisionTreeClassifier
import pandas as pd

class Classification:
    def __init__(self) -> None:
        self.classification_model = joblib.load('D:/geographical_news_scrapper/kecelakaan/split/Classifikasi/model/d_tree_kecelakaan2.pkl')
        self.scrapped_news = pd.read_csv('D:/geographical_news_scrapper/kecelakaan/split/result/Severity/SeverityResult.csv')
    
    def getClassificationValue(self):
        try:
            document_result = []
            
            for i in range(0, self.scrapped_news.shape[0]):
                title = self.scrapped_news.iloc[i, 0]
                berita = self.scrapped_news.iloc[i, 1]
                time = self.scrapped_news.iloc[i, 2]
                what = self.scrapped_news.iloc[i, 3]
                tanggal_asli = self.scrapped_news.iloc[i, 4]
                orang = self.scrapped_news.iloc[i, 5]
                provinsi = self.scrapped_news.iloc[i, 6]
                kabupaten = self.scrapped_news.iloc[i, 7]
                kecamatan = self.scrapped_news.iloc[i, 8]

                """
                Bagian ini adalah indikator yang perlu disesuaikan untuk masing - masing topik
                """
                meniggal = self.scrapped_news.iloc[i, 9] 
                luka = self.scrapped_news.iloc[i, 10] 
                hilang = self.scrapped_news.iloc[i, 11] 
                tenggelam = self.scrapped_news.iloc[i, 12]
                pesawat = self.scrapped_news.iloc[i, 13]

                keparahan = self.classification_model.predict([[meniggal,luka, hilang, tenggelam, pesawat]])
                document_result.append([title, berita, time, what, tanggal_asli, orang, provinsi, kabupaten, kecamatan, meniggal, luka, hilang, tenggelam, pesawat,keparahan[0]])

            writer = pd.DataFrame(document_result, columns=[
                                'title', 'description', 'time', 'what', 'when', 'who', 'provinsi', 'kabupaten / kota', 'kecamatan', 'meniggal', 'luka', 'hilang', 'tenggelam', 'pesawat','klasifikasi'], index=None)
            writer.to_csv('D:/geographical_news_scrapper/kecelakaan/split/result/Classification/ClassificationResult.csv', index=False, sep=',')
            return "success"
        except:
            return "error"
        