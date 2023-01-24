from typing import List
from numpy import NaN
from spacy import load, displacy
import pandas as pd
import joblib
import re
import time
import datetime
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode

class NER:
    def __init__(self) -> None:
        # self.listDaerah = joblib.load('model/Where/listProvKabKec.pkl')
        # self.listProvinsi = joblib.load('model/Where/provinsi.pkl')
        # self.listKabupaten = joblib.load('model/Where/kabupaten.pkl')
        # self.listKecamatan = joblib.load('model/Where/kecamatan.pkl')
        # self.loaded_model = load('model/NER_Kec_Ben_Krim_Kese_Eko/output/model-last')
        self.listDaerah = joblib.load('D:/sem9/program/TA_petakabar/bencana/main/model/Where/listProvKabKec.pkl')
        self.listProvinsi = joblib.load('D:/sem9/program/TA_petakabar/bencana/main/model/Where/provinsi.pkl')
        self.listKabupaten = joblib.load('D:/sem9/program/TA_petakabar/bencana/main/model/Where/kabupaten.pkl')
        self.listKecamatan = joblib.load('D:/sem9/program/TA_petakabar/bencana/main/model/Where/kecamatan.pkl')
        self.loaded_model = load('D:/sem9/program/TA_petakabar/bencana/main/model/NER_Kec_Ben_Krim_Kese_Eko/output/model-last')
        # self.scrapped_news = pd.read_csv('result/4w/4w_news.csv')

        #ambil dari db
        self.newsscrapped = []
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            cursor.execute("SELECT ID, berita_date, berita_desc FROM berita where berita_topik_id = 1 AND class_classification is null")
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
    
    def __preprocessingNER(self,berita: str):
        s = str(berita)
        s = s.lower()
        s = s.replace('\n', ' ')
        s = s.replace('\r', ' ')
        # tokens = [token for token in s.split(" ") if token != ""]
        return s

    def checkLocation(self,provinsi: List[str],kabupaten: List[str],kecamatan: List[str])-> List[str]:
        hasil=[]
        if(len(provinsi)>0 and len(kabupaten)>0 and len(kecamatan)>0):
            provinsi_top=provinsi[0]
            kabupaten_top=kabupaten[0]
            kecamatan_top=kecamatan[0]
            if(kecamatan_top[1]<kabupaten_top[1]<provinsi_top[1]):
                if(kabupaten_top[1]-kecamatan_top[2]<=60 and provinsi_top[1]-kabupaten_top[2]<=60):
                    hasil.append(kecamatan_top[0])
                    hasil.append(kabupaten_top[0])
                    hasil.append(provinsi_top[0])
                elif(kabupaten_top[1]-kecamatan_top[2]<=60 and provinsi_top[1]-kabupaten_top[2]>60):
                    hasil.append(kecamatan_top[0])
                    hasil.append(kabupaten_top[0])
                elif(kabupaten_top[1]-kecamatan_top[2]>60 and provinsi_top[1]-kabupaten_top[2]>60):
                    hasil.append((kecamatan_top[0]))
            elif((kecamatan_top[1]<kabupaten_top[1])and(kabupaten_top[1]>provinsi_top[1])and(kecamatan_top[1]<provinsi_top[1])):
                if(provinsi_top[1]-kecamatan_top[2]<=60):
                    hasil.append(kecamatan_top[0])
                    hasil.append(provinsi_top[0])
                elif(provinsi_top[1]-kecamatan_top[2]>60):
                    hasil.append(kecamatan_top[0])
            elif((kecamatan_top[1]>kabupaten_top[1])and(kabupaten_top[1]<provinsi_top[1])and(kecamatan_top[1]>provinsi_top[1])):
                if(provinsi_top[1]-kabupaten_top[2]<=60):
                    hasil.append(kabupaten_top[0])
                    hasil.append(provinsi_top[0])
                elif(provinsi_top[1]-kabupaten_top[2]>60):
                    hasil.append((kabupaten_top[0]))
            elif((kecamatan_top[1]>kabupaten_top[1])and(kabupaten_top[1]<provinsi_top[1])and(kecamatan_top[1]<provinsi_top[1])):
                hasil.append(kabupaten_top[0])
            elif((kecamatan_top[1]<kabupaten_top[1])and(kabupaten_top[1]>provinsi_top[1])and(kecamatan_top[1]>provinsi_top[1])):
                hasil.append(provinsi_top[0])
            elif(kecamatan_top[1]>kabupaten_top[1]>provinsi_top[1]):
                hasil.append(provinsi_top[0])
        elif(len(provinsi)>0 and len(kabupaten)>0 and len(kecamatan)==0):
            provinsi_top=provinsi[0]
            kabupaten_top=kabupaten[0]
            if(kabupaten_top[1]<provinsi_top[1]):
                if(provinsi_top[1]-kabupaten_top[2]<=60):
                    hasil.append(kabupaten_top[0])
                    hasil.append(provinsi_top[0])
                else:
                    hasil.append(kabupaten_top[0])
            elif(kabupaten_top[1]>provinsi_top[1]):
                hasil.append(provinsi_top[0])
        elif(len(provinsi)>0 and len(kabupaten)==0 and len(kecamatan)>0):
            provinsi_top=provinsi[0]
            kecamatan_top=kecamatan[0]
            if(kecamatan_top[1]<provinsi_top[1]):
                if(provinsi_top[1]-kecamatan_top[2]<=60):
                    hasil.append(kecamatan_top[0])
                    hasil.append(provinsi_top[0])
                else:
                    hasil.append(kecamatan_top[0])
            elif(kecamatan_top[1]>provinsi_top[1]):
                hasil.append(provinsi_top[0])
        elif(len(provinsi)==0 and len(kabupaten)>0 and len(kecamatan)>0):
            kabupaten_top=kabupaten[0]
            kecamatan_top=kecamatan[0]
            if(kecamatan_top[1]<kabupaten_top[1]):
                if(kabupaten_top[1]-kecamatan_top[2]<=60):
                    hasil.append(kecamatan_top[0])
                    hasil.append(kabupaten_top[0])
                else:
                    hasil.append(kecamatan_top[0])
            elif(kecamatan_top[1]>kabupaten_top[1]):
                hasil.append(kabupaten_top[0])
        elif(len(provinsi)>0 and len(kabupaten)==0 and len(kecamatan)==0):
            hasil.append(provinsi[0][0])
        elif(len(provinsi)==0 and len(kabupaten)>0 and len(kecamatan)==0):
            hasil.append(kabupaten[0][0])
        elif(len(provinsi)==0 and len(kabupaten)==0 and len(kecamatan)>0):
            hasil.append(kecamatan[0][0])
        elif(len(provinsi)==0 and len(kabupaten)==0 and len(kecamatan)==0):
            return hasil
        
        return hasil

    def compareToDatasetLocation(self,provinsi: List[str],kabupaten: List[str],kecamatan: List[str])-> List[str]:
        trueLocation= self.checkLocation(provinsi,kabupaten,kecamatan)
        if(len(trueLocation)==3):
                for i in range(0,len(self.listDaerah)):
                    if(self.listDaerah[i][0]==trueLocation[2] and self.listDaerah[i][1]==trueLocation[1] and self.listDaerah[i][2]==trueLocation[0]):
                                return trueLocation
                    
                trueLocation.insert(0,'-')
                trueLocation.insert(1,'-')
                trueLocation.insert(2,'-')
                return trueLocation

        elif(len(trueLocation)==2):
                for i in range(0,len(self.listDaerah)):
                    if(self.listDaerah[i][0]==trueLocation[1] and self.listDaerah[i][1]==trueLocation[0]):
                            trueLocation.insert(0,'-')
                            return trueLocation
                    elif(self.listDaerah[i][1]==trueLocation[1] and self.listDaerah[i][2]==trueLocation[0]):
                            trueLocation.insert(2,self.listDaerah[i][0])
                            return trueLocation
                    elif(self.listDaerah[i][0]==trueLocation[1] and self.listDaerah[i][2]==trueLocation[0]):
                            trueLocation.insert(1,self.listDaerah[i][1])
                            return trueLocation
        
                trueLocation.insert(0,'-')
                trueLocation.insert(1,'-')
                trueLocation.insert(2,'-')
                return trueLocation

        elif(len(trueLocation)==1):
                for i in range(0,len(self.listDaerah)):
                    if(self.listDaerah[i][0]==trueLocation[0] ):
                            trueLocation.insert(0,'-')
                            trueLocation.insert(1,'-')
                            return trueLocation
                    elif(self.listDaerah[i][1]==trueLocation[0] ):
                            trueLocation.insert(0,'-')
                            trueLocation.insert(2,self.listDaerah[i][0])
                            return trueLocation
                    elif(self.listDaerah[i][2]==trueLocation[0] ):
                            trueLocation.insert(1,self.listDaerah[i][1])
                            trueLocation.insert(2,self.listDaerah[i][0])
                            return trueLocation
        
                trueLocation.insert(0,'-')
                trueLocation.insert(1,'-')
                trueLocation.insert(2,'-')
                return trueLocation
                
        else:
                trueLocation.insert(0,'-')
                trueLocation.insert(1,'-')
                trueLocation.insert(2,'-')
                return trueLocation

    def getNewsTime(self,dateTime: str):
        month_to_number = {
            'jan': '1',
            'feb': '2',
            'mar': '3',
            'apr': '4',
            'mei': '5',
            'jun': '6',
            'jul': '7',
            'agu': '8',
            'sep': '9',
            'okt': '10',
            'nov': '11',
            'des': '12',
        }

        filteredDateTime = re.search("[A-Za-z]{4,6},\s[0-9]{2}\s[A-Za-z]{3}\s[0-9]{4,}\s[0-9]{2}:[0-9]{2}\s[A-Za-z]{3}", dateTime).group(0)
        
        if (filteredDateTime):
            splitted_timestamp = filteredDateTime.split(' ')
            pre_formatted_time = splitted_timestamp[1] + '/' + month_to_number[splitted_timestamp[2].lower()] + '/' + splitted_timestamp[3]

            return pre_formatted_time
        
        return ''
    
    def checkDateFormat(self, dateTime):
        pattern1 = '[A-Za-z]{4,6}\s\([0-9]{1,}\/[0-9]{1,}\/[0-9]{2,}\)'
        pattern2 = '[A-Za-z]{4,6}\s\([0-9]{1,}\/[0-9]{1,}\)'

        filteredDateTimePattern1 = re.search(pattern1, dateTime)
        filteredDateTimePattern2 = re.search(pattern2, dateTime)

        if filteredDateTimePattern1:
            return filteredDateTimePattern1.group(0)
        elif filteredDateTimePattern2:
            return filteredDateTimePattern2.group(0)
        
        return ''

    def compareDateArray(self,sortByLength,newsDate):
        year = newsDate.split('/')[2]
        timestampList = []
        def convertToTimestapms(date):
            # return int(time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()))
            conv = int(time.mktime(datetime.strptime(date, "%d/%m/%Y").timetuple()))
            return conv

        for i, tempTime in enumerate(sortByLength):
            # Find the content inside parentheses
            if(tempTime[-1:]!=')'):
                tempTime=tempTime+')'
                
            currTime = re.search(r'\((.*?)\)', tempTime)
            
            if (currTime != None):
                currTime = currTime.group(1)
                currTime = str(currTime)
                currTime=currTime.replace("\\", "")
            
            
            if (tempTime.lower() == 'kemarin' or ('kemarin' in tempTime.lower())):
                timestampList.append(convertToTimestapms(newsDate) - (24*60*60))
            
            if (currTime == None or currTime==''):
                timestampList.append(convertToTimestapms(str(newsDate)))
            else:
                # Find the year
                splitted = currTime.split('/')

                formattedDate = None
                if (len(splitted) == 3):
                    if(len(splitted[2])==2):
                        splitted[2]=year
                        currTime="/".join(splitted)
                    year = splitted[2]
                    timestampList.append(convertToTimestapms(currTime))
                elif (len(splitted) == 2):
                    formattedDate = (splitted[0] + '/' + splitted[1] + '/' + year)
                    timestampList.append(convertToTimestapms(formattedDate))
    
        return datetime.fromtimestamp(sorted(timestampList)[0]).strftime("%d/%m/%Y")

    def toOriginal(self,teks: str)-> str:
        hasil=''
        if(teks=='sulsel'):
            hasil='sulawesi selatan'
        elif(teks=='sultra'):
            hasil='sulawesi tenggara'
        elif(teks=='sulut'):
            hasil='sulawesi utara'
        elif(teks=='sulteng'):
            hasil='sulawesi tengah'
        elif(teks=='sulbar'):
            hasil='sulawesi barat'
        elif(teks=='kaltim'):
            hasil='kalimantan timur'
        elif(teks=='kaltara'):
            hasil='kalimantan utara'
        elif(teks=='kalteng'):
            hasil='kalimantan tengah'
        elif(teks=='kalsel'):
            hasil='kalimantan selatan'
        elif(teks=='kalbar'):
            hasil='kalimantan barat'
        elif(teks=='jatim'):
            hasil='jawa timur'
        elif(teks=='jateng'):
            hasil='jawa tengah'
        elif(teks=='jabar'):
            hasil='jawa barat'
        elif(teks=='diy'):
            hasil='di yogyakarta'
        elif(teks=='jakbar'):
            hasil='jakarta barat'
        elif(teks=='jaktim'):
            hasil='jakarta timur'
        elif(teks=='jaksel'):
            hasil='jakarta selatan'
        elif(teks=='jakpus'):
            hasil='jakarta pusat'
        elif(teks=='jakut'):
            hasil='jakarta utara'
        elif(teks=='nad'):
            hasil='nanggroe aceh darussalam'
        elif(teks=='sumsel'):
            hasil='sumatera selatan'
        elif(teks=='sumut'):
            hasil='sumatera utara'
        elif(teks=='sumbar'):
            hasil='sumatera barat'
        else:
            hasil=teks
        return hasil

    def can_convert_to_int(self, string):
        try:
            int(string)

            return True
        except ValueError:
            return False

    def getValueNER(self):
        try:
            # document_result = []
        
            # for i in range(0, self.scrapped_news.shape[0]):
            #     title = self.scrapped_news.iloc[i, 0]
            #     berita = self.scrapped_news.iloc[i, 1]
            #     time = self.scrapped_news.iloc[i, 2]
            #     what = self.scrapped_news.iloc[i, 3]
            self.descberita = []
            self.dateberita = []
            self.idberita = []

            if(len(self.newsscrapped)>0):
                self.idberita, self.dateberita, self.descberita= zip(*self.newsscrapped)

            for i in range(0, len(self.newsscrapped)):
                berita = self.descberita[i]
                time = self.dateberita[i]
                idberita = self.idberita[i]

                news = self.__preprocessingNER(berita)
                doc = self.loaded_model(news)

                newsDate = self.getNewsTime(time)

                provinsi = []
                kabupaten = []
                kecamatan = []
                tanggal = []
                orang = []
                visitedOrang = []
                visitedLokasi = []
                visitedTanggal = []

                tanggal_asli=''

                for ent in doc.ents:
                        if(ent.label_== 'ORANG'):
                            if(ent.text[-1:]=='.'):
                                    teks = ent.text[:-1]
                                    if (teks not in visitedOrang):
                                        orang.append(teks)
                                        visitedOrang.append(teks)
                            else:
                                    if (ent.text not in visitedOrang):
                                        orang.append(ent.text)
                                        visitedOrang.append(ent.text)
                        if(ent.label_== 'TANGGAL'):
                            if(ent.text[-1:]=='.'):
                                    teks = ent.text[:-1]
                                    if (teks not in visitedTanggal and self.checkDateFormat(teks) != ''):
                                        tanggal.append(teks)
                                        visitedTanggal.append(teks)
                            else:
                                    if (ent.text not in visitedTanggal and self.checkDateFormat(ent.text) != ''):
                                        tanggal.append(ent.text)
                                        visitedTanggal.append(ent.text)
                        elif(ent.label_== 'LOKASI'):
                            if(ent.text[-1:]=='.'):
                                    teks = ent.text[:-1]
                                    teks = self.toOriginal(teks)
                                    if ((teks in self.listProvinsi) and (teks not in visitedLokasi)):
                                        provinsi.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)
                                    elif ((teks in self.listKabupaten) and (teks not in visitedLokasi)):
                                        kabupaten.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)
                                    elif ((teks in self.listKecamatan) and (teks not in visitedLokasi)):
                                        kecamatan.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)
                            else:
                                    teks = self.toOriginal(ent.text)
                                    if ((teks in self.listProvinsi) and (teks not in visitedLokasi)):
                                        provinsi.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)
                                    elif ((teks in self.listKabupaten) and (teks not in visitedLokasi)):
                                        kabupaten.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)
                                    elif ((teks in self.listKecamatan) and (teks not in visitedLokasi)):
                                        kecamatan.append([teks,ent.start_char,ent.end_char])
                                        visitedLokasi.append(teks)

                # visited.clear()
                visitedOrang.clear()
                visitedLokasi.clear()
                visitedTanggal.clear()
            
                sortedTimes = sorted(tanggal, key=len, reverse=True)
                newsortedTimes = []

                # if(sortedTimes):
                #     tanggal_asli=self.compareDateArray(sortedTimes,newsDate)
                # else:
                #     tanggal_asli=newsDate     
                if(sortedTimes):
                    #handling typo penulisan tanggal di artikel
                    year = newsDate.split('/')[2]
                    for x in range(0, len(sortedTimes)):
                        cekformat = sortedTimes[x]
                        splitcekformat = list(cekformat.split("("))
                        cekformat = splitcekformat[1]
                        cekformat = cekformat.replace("(","")
                        cekformat = cekformat.replace(")","")
                        cekformat = cekformat.replace(":","")
                        splitted = list(cekformat.split("/"))
                        if (self.can_convert_to_int(splitted[0]) and self.can_convert_to_int(splitted[1])):
                            tanggal = int(splitted[0])
                            bulan = int(splitted[1])
                            cekdate = False
                            bulan1 = [1,3,5,7,8,10,12]
                            bulan2 = [4,6,9,11]

                            if (len(splitted) == 3): #menghandle bila penulisan tahun tidak sesuai format
                                # sortedTimes[x] = sortedTimes[x].replace(splitted[2],year)
                                rep=sortedTimes[x]
                                repsplit=splitted[2]
                                sortedTimes[x] = rep[::-1].replace(repsplit[::-1],year[::-1], 1)[::-1]
                            if (bulan <= 12):
                                if (bulan == 2 and tanggal <= 29): #handle bulan februari
                                    cekdate = True
                                else: 
                                    if (bulan in bulan2 and tanggal < 31):
                                        cekdate = True
                                    elif (bulan in bulan1 and tanggal < 32):
                                        cekdate = True
                            if (cekdate):
                                newsortedTimes.append(sortedTimes[x])
                        else:
                            continue
                    if(len(newsortedTimes)==0):
                        tanggal_asli=newsDate     
                    else:
                        tanggal_asli=self.compareDateArray(newsortedTimes,newsDate)
                else:
                    tanggal_asli=newsDate  

                if(len(orang)==0):
                    orang="-"
                lokasi_asli = self.compareToDatasetLocation(provinsi,kabupaten,kecamatan)
                self.save_to_mysql(idberita, tanggal_asli, orang, lokasi_asli[2], lokasi_asli[1], lokasi_asli[0])

            #     document_result.append([title, berita, time, what, tanggal_asli, orang, lokasi_asli[2], lokasi_asli[1], lokasi_asli[0]])

            # writer = pd.DataFrame(document_result, columns=[
            #                     'title', 'description', 'time', 'what', 'when', 'who', 'provinsi', 'kabupaten / kota', 'kecamatan'], index=None)
            # writer.to_csv('result/4w/4w_news.csv', index=False, sep=',')
            return "success"
        except:
            return "error"
    
    def save_to_mysql(self, idberita, when, who, provinsi, kabupaten, kecamatan):
        try:
            conn = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cur = conn.cursor()
            add_news = ("UPDATE berita "
                "SET ner_when = %s, ner_who = %s, ner_prov = %s, ner_kab = %s, ner_kec = %s "
            "WHERE ID = %s"
            )
            whostr = ""
            for y in range(len(who)):
                whostr = whostr + who[y]
                if y < len(who)-1:
                    whostr = whostr + ", "
            data_news = (when, whostr, provinsi, kabupaten, kecamatan, idberita)

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