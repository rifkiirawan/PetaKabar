# from bencana.main.submodule.Classification import Classification
# from bencana.main.submodule.NER import NER 
# from bencana.main.submodule.QueryExpansion import QueryExpansion 
# from bencana.main.submodule.ScrapProcess import ScrapProcess 
# from bencana.main.submodule.Severity import Severity

from bencana.main.submodule.Classification import Classification as bencana_Classification
from bencana.main.submodule.NER import NER as bencana_NER
from bencana.main.submodule.QueryExpansion import QueryExpansion as bencana_QueryExpansion
from bencana.main.submodule.ScrapProcess import ScrapProcess as bencana_ScrapProcess
from bencana.main.submodule.Severity import Severity as bencana_Severity

from ekonomi.submodule.Classification import Classification as ekonomi_Classification
from ekonomi.submodule.NER import NER as ekonomi_NER
from ekonomi.submodule.QueryExpansion import QueryExpansion as ekonomi_QueryExpansion
from ekonomi.submodule.ScrapProcess import ScrapProcess as ekonomi_ScrapProcess
from ekonomi.submodule.Severity import Severity as ekonomi_Severity

from kecelakaan.submodule.Classification import Classification as kecelakaan_Classification
from kecelakaan.submodule.NER import NER as kecelakaan_NER
from kecelakaan.submodule.QueryExpansion import QueryExpansion as kecelakaan_QueryExpansion
from kecelakaan.submodule.ScrapProcess import ScrapProcess as kecelakaan_ScrapProcess
from kecelakaan.submodule.Severity import Severity as kecelakaan_Severity

from kesehatan.main.submodule.Classification import Classification as kesehatan_Classification
from kesehatan.main.submodule.NER import NER as kesehatan_NER
from kesehatan.main.submodule.QueryExpansion import QueryExpansion as kesehatan_QueryExpansion
from kesehatan.main.submodule.ScrapProcess import ScrapProcess as kesehatan_ScrapProcess
from kesehatan.main.submodule.Severity import Severity as kesehatan_Severity

from kriminalitas.Main.submodule.Classification import Classification as kriminalitas_Classification
from kriminalitas.Main.submodule.NER import NER as kriminalitas_NER
from kriminalitas.Main.submodule.QueryExpansion import QueryExpansion as kriminalitas_QueryExpansion
from kriminalitas.Main.submodule.ScrapProcess import ScrapProcess as kriminalitas_ScrapProcess
from kriminalitas.Main.submodule.Severity import Severity as kriminalitas_Severity

from olahraga.submodule.Classification import Classification as olahraga_Classification
from olahraga.submodule.NER import NER as olahraga_NER
from olahraga.submodule.QueryExpansion import QueryExpansion as olahraga_QueryExpansion
from olahraga.submodule.ScrapProcess import ScrapProcess as olahraga_ScrapProcess
from olahraga.submodule.Severity import Severity as olahraga_Severity

from typing import Union
# from fastapi import FastAPI
import pandas as pd
# from fastapi import FastAPI, BackgroundTasks
from multiprocessing import Process



from twisted.internet import reactor
import mysql.connector
from mysql.connector import errorcode

# app = FastAPI()


# @app.get('/scrap')
# async def scrap():
# # if __name__ == '__main__':
#     try:
#         # 1 Proses scraping, inisiasi modul ScrapProcess
#         # print('1 Step Passed')

#         scrap = ScrapProcess()
#         # resultScrap = scrap.crawlNews()

#         process = Process(target=scrap.crawlNews)
#         process.start()
#         process.join()

#         # 2 QE Expansion waht, jika hasil scraping success
#         print('2 Step Passed')

#         qe = QueryExpansion()
#         resultQE = qe.getWhatFromText("bencana apa yang terjadi")
        
#         # 3 NER when, who, where, jika hasil qe success
#         if (resultQE == "success"):
#             print('3 Step Passed')

#             ner = NER()
#             resultNER = ner.getValueNER()

#             if (resultNER == "success"):
#                 print('4 Step Passed')

#                 severity = Severity()
#                 resultSeverity=severity.getKeparahanVelue()

#                 if (resultSeverity == "success"):
#                     print('5 Step Passed')

#                     classification = Classification()
#                     resultClassification=classification.getClassificationValue()

#                     if (resultClassification == "success"):
#                         print('6 Step Passed')
                        
#                         # df_w = pd.read_csv('result/classification_res/result_final.csv')
#                          #ambil dari db
#                         newsscrapped = []
#                         try:
#                             cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
#                             cursor = cnx.cursor()
#                             cursor.execute("SELECT qe_what, ner_when, ner_who, ner_prov, ner_kab, ner_kec, class_classification FROM berita where berita_topik_id = 1")
#                             myresult = cursor.fetchall()
#                             for row in myresult:
#                                 newsscrapped.append(row)

#                         except mysql.connector.Error as err:
#                             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#                                 print("Something is wrong with your user name or password")
#                             elif err.errno == errorcode.ER_BAD_DB_ERROR:
#                                 print("Database does not exist")
#                             else:
#                                 print(err)
#                         else:
#                             cursor.close()
#                             cnx.close()

#                         #ambil dari db
#                         whatberita = []
#                         tglasliberita = []
#                         whoberita = []
#                         provinsiberita = []
#                         kabupatenberita = []
#                         kecamatanberita = []
#                         keparahanberita = []
                        
#                         whatberita, tglasliberita, whoberita, provinsiberita, kabupatenberita, kecamatanberita, keparahanberita= zip(*newsscrapped)

#                         result_list = []

#                         for i in range(0, len(newsscrapped)):
#                             result = {
#                                 'title' : '',
#                                 'kategori' : 'bencana',
#                                 'nama_kejadian' : whatberita[i],
#                                 'waktu' : tglasliberita[i],
#                                 'orang_terlibat' : whoberita[i],
#                                 'provinsi' : provinsiberita[i],
#                                 'kabupaten' : kabupatenberita[i],
#                                 'kecamatan' : kecamatanberita[i],
#                                 'tingkat_keparahan' : keparahanberita[i]
#                             }
#                             result_list.append(result)

#                         # for i in range(0, df_w.shape[0]):
#                         #     result = {
#                         #         'title': str(df_w.iloc[i, 0]),
#                         #         'kategori': 'bencana',
#                         #         'nama_kejadian': str(df_w.iloc[i, 3]),
#                         #         'waktu': str(df_w.iloc[i, 4]),
#                         #         'orang_terlibat': str(df_w.iloc[i, 5]),
#                         #         'provinsi': str(df_w.iloc[i, 6]),
#                         #         'kabupaten': str(df_w.iloc[i, 7]),
#                         #         'kecamatan': str(df_w.iloc[i, 8]),
#                         #         'tingkat_keparahan': df_w.iloc[i, 13]
#                         #     }
#                         #     result_list.append(result)

#                         return {
#                             'status_code': 200,
#                             'message': 'success',
#                             'data': result_list
#                         }

#                     else:
#                         return {
#                             'status_code': 500,
#                             'message': 'classification failed'
#                         }
#                 else:
#                     return {
#                         'status_code': 500,
#                         'message': 'severity failed'
#                 }
#             else:
#                 return {
#                     'status_code': 500,
#                     'message': 'ner failed'
#                 }
#         else:
#             return {
#                 'status_code': 500,
#                 'message': 'qe failed'
#             }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }


# @app.get('/scrap')
# async def scrap():
# if __name__ == '__main__':
    # try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
if __name__ == '__main__':    

    bencana_scrap = bencana_ScrapProcess()
    bencana_process = Process(target=bencana_scrap.crawlNews)
    bencana_process.start()
    bencana_process.join()

    ekonomi_scrap = ekonomi_ScrapProcess()
    ekonomi_process = Process(target=ekonomi_scrap.crawlNews)
    ekonomi_process.start()
    ekonomi_process.join()

    kecelakaan_scrap = kecelakaan_ScrapProcess()
    kecelakaan_process = Process(target=kecelakaan_scrap.crawlNews)
    kecelakaan_process.start()
    kecelakaan_process.join()


    kesehatan_scrap = kesehatan_ScrapProcess()
    kesehatan_process = Process(target=kesehatan_scrap.crawlNews)
    kesehatan_process.start()
    kesehatan_process.join()

    kriminalitas_scrap = kriminalitas_ScrapProcess()
    kriminalitas_process = Process(target=kriminalitas_scrap.crawlNews)
    kriminalitas_process.start()
    kriminalitas_process.join()

    olahraga_scrap = olahraga_ScrapProcess()
    olahraga_process = Process(target=olahraga_scrap.crawlNews)
    olahraga_process.start()
    olahraga_process.join()

    # 2 QE Expansion waht, jika hasil scraping success
    # print('2 Step Passed')

    bencana_qe = bencana_QueryExpansion()
    bencana_resultQE = bencana_qe.getWhatFromText("bencana apa yang terjadi")

    ekonomi_qe = ekonomi_QueryExpansion()
    ekonomi_resultQE = ekonomi_qe.getWhatFromText("apa isi berita tersebut")

    kecelakaan_qe = kecelakaan_QueryExpansion()
    kecelakaan_resultQE = kecelakaan_qe.getWhatFromText("apa sebenarnya kejadian kecelakaan yang terjadi diberita tersebut")

    kesehatan_qe = kesehatan_QueryExpansion()
    kesehatan_resultQE = kesehatan_qe.getWhatFromText("kasus penyakit apa yang terjadi")

    kriminalitas_qe = kriminalitas_QueryExpansion()
    kriminalitas_resultQE = kriminalitas_qe.getWhatFromText("kriminalitas apa yang terjadi")

    olahraga_qe = olahraga_QueryExpansion()
    olahraga_resultQE = olahraga_qe.getWhatFromText("olahraga apa yang terjadi diberita tersebut")

    # 3 NER when, who, where, jika hasil qe success
    if (bencana_resultQE == "success" and ekonomi_resultQE == "success" and kecelakaan_resultQE == "success" and kesehatan_resultQE == "success" and kriminalitas_resultQE == "success" and olahraga_resultQE == "success"):
        # print('3 Step Passed')

        bencana_ner = bencana_NER()
        bencana_resultNER = bencana_ner.getValueNER()

        ekonomi_ner = ekonomi_NER()
        ekonomi_resultNER = ekonomi_ner.getValueNER()

        kecelakaan_ner = kecelakaan_NER()
        kecelakaan_resultNER = kecelakaan_ner.getValueNER()

        kesehatan_ner = kesehatan_NER()
        kesehatan_resultNER = kesehatan_ner.getValueNER()

        kriminalitas_ner = kriminalitas_NER()
        kriminalitas_resultNER = kriminalitas_ner.getValueNER()

        olahraga_ner = olahraga_NER()
        olahraga_resultNER = olahraga_ner.getValueNER()

        if (bencana_resultNER == "success" and ekonomi_resultNER == "success" and kecelakaan_resultNER == "success" and kesehatan_resultNER == "success" and kriminalitas_resultNER == "success" and olahraga_resultNER == "success"):
            # print('4 Step Passed')

            bencana_severity = bencana_Severity()
            bencana_resultSeverity=bencana_severity.getKeparahanVelue()

            ekonomi_severity = ekonomi_Severity()
            ekonomi_resultSeverity=ekonomi_severity.getKeparahanVelue()

            kecelakaan_severity = kecelakaan_Severity()
            kecelakaan_resultSeverity=kecelakaan_severity.getKeparahanVelue()

            kesehatan_severity = kesehatan_Severity()
            kesehatan_resultSeverity=kesehatan_severity.getKeparahanVelue()

            kriminalitas_severity = kriminalitas_Severity()
            kriminalitas_resultSeverity=kriminalitas_severity.getKeparahanVelue()

            olahraga_severity = olahraga_Severity()
            olahraga_resultSeverity=olahraga_severity.getKeparahanVelue()

            if (bencana_resultSeverity == "success" and ekonomi_resultSeverity == "success" and kecelakaan_resultSeverity == "success" and kesehatan_resultSeverity == "success" and kriminalitas_resultSeverity == "success" and olahraga_resultSeverity == "success"):
                # print('5 Step Passed')

                bencana_classification = bencana_Classification()
                bencana_resultClassification=bencana_classification.getClassificationValue()

                ekonomi_classification = ekonomi_Classification()
                ekonomi_resultClassification=ekonomi_classification.getClassificationValue()

                kecelakaan_classification = kecelakaan_Classification()
                kecelakaan_resultClassification=kecelakaan_classification.getClassificationValue()

                kesehatan_classification = kesehatan_Classification()
                kesehatan_resultClassification=kesehatan_classification.getClassificationValue()

                kriminalitas_classification = kriminalitas_Classification()
                kriminalitas_resultClassification=kriminalitas_classification.getClassificationValue()

                olahraga_classification = olahraga_Classification()
                olahraga_resultClassification=olahraga_classification.getClassificationValue()

                if (bencana_resultClassification == "success" and ekonomi_resultClassification == "success" and kecelakaan_resultClassification == "success" and kesehatan_resultClassification == "success" and kriminalitas_resultClassification == "success" and olahraga_resultClassification == "success"):
                    # print('6 Step Passed')
                    
                    # df_w = pd.read_csv('result/classification_res/result_final.csv')
                        #ambil dari db
                    # newsscrapped = []
                    # try:
                    #     cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
                    #     cursor = cnx.cursor()
                    #     cursor.execute("SELECT qe_what, ner_when, ner_who, ner_prov, ner_kab, ner_kec, class_classification FROM berita where (berita_qdate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) OR berita_qdate = curdate())")
                    #     myresult = cursor.fetchall()
                    #     for row in myresult:
                    #         newsscrapped.append(row)

                    # except mysql.connector.Error as err:
                    #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    #         print("Something is wrong with your user name or password")
                    #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    #         print("Database does not exist")
                    #     else:
                    #         print(err)
                    # else:
                    #     cursor.close()
                    #     cnx.close()

                    # #ambil dari db
                    # whatberita = []
                    # tglasliberita = []
                    # whoberita = []
                    # provinsiberita = []
                    # kabupatenberita = []
                    # kecamatanberita = []
                    # keparahanberita = []
                    
                    # whatberita, tglasliberita, whoberita, provinsiberita, kabupatenberita, kecamatanberita, keparahanberita= zip(*newsscrapped)

                    # result_list = []

                    # for i in range(0, len(newsscrapped)):
                    #     result = {
                    #         'title' : '',
                    #         'kategori' : 'bencana',
                    #         'nama_kejadian' : whatberita[i],
                    #         'waktu' : tglasliberita[i],
                    #         'orang_terlibat' : whoberita[i],
                    #         'provinsi' : provinsiberita[i],
                    #         'kabupaten' : kabupatenberita[i],
                    #         'kecamatan' : kecamatanberita[i],
                    #         'tingkat_keparahan' : keparahanberita[i]
                    #     }
                    #     result_list.append(result)
                    
                    print("success")
                    # return {
                    #     'status_code': 200,
                    #     'message': 'success',
                    #     'data': result_list
                    # }

                else:
                    print("classification failed")
                    # return {
                    #     'status_code': 500,
                    #     'message': 'classification failed'
                    # }
            else:
                print("severity failed")
            #     return {
            #         'status_code': 500,
            #         'message': 'severity failed'
            # }
        else:
            print("ner failed")
            # return {
            #     'status_code': 500,
            #     'message': 'ner failed'
            # }
    else:
        print("qe failed")
        # return {
        #     'status_code': 500,
        #     'message': 'qe failed'
        # }

        # except Exception as error:
        #     return {
        #         'status_code': 500,
        #         'message': error
        #     }

# @app.get('/qe')
# async def scrap():
# # if __name__ == '__main__':
#     try:
#         # 1 Proses scraping, inisiasi modul ScrapProcess
#         # print('1 Step Passed')

#         # scrap = ScrapProcess()
#         # resultScrap = scrap.crawlNews()

#         # process = Process(target=scrap.crawlNews)
#         # process.start()
#         # process.join()

#         # 2 QE Expansion waht, jika hasil scraping success
#         # print('2 Step Passed')

#         qe = QueryExpansion()
#         resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
#         # 3 NER when, who, where, jika hasil qe success
#         if (resultQE == "success"):
#             print('3 Step Passed')

#             # ner = NER()
#             # resultNER = ner.getValueNER()

#             # if (resultNER == "success"):
#             #     print('4 Step Passed')

#             #     severity = Severity()
#             #     resultSeverity=severity.getKeparahanVelue()

#             #     if (resultSeverity == "success"):
#             #         print('5 Step Passed')

#             #         classification = Classification()
#             #         resultClassification=classification.getClassificationValue()

#             #         if (resultClassification == "success"):
#             #             print('6 Step Passed')
                        
#             #             df_w = pd.read_csv('result/classification_res/result_final.csv')

#             #             result_list = []

#             #             for i in range(0, df_w.shape[0]):
#             #                 result = {
#             #                     'title': str(df_w.iloc[i, 0]),
#             #                     'kategori': 'kesehatan',
#             #                     'nama_kejadian': str(df_w.iloc[i, 3]),
#             #                     'waktu': str(df_w.iloc[i, 4]),
#             #                     'orang_terlibat': str(df_w.iloc[i, 5]),
#             #                     'provinsi': str(df_w.iloc[i, 6]),
#             #                     'kabupaten': str(df_w.iloc[i, 7]),
#             #                     'kecamatan': str(df_w.iloc[i, 8]),
#             #                     'tingkat_keparahan': df_w.iloc[i, 11]
#             #                 }
#             #                 result_list.append(result)

#             #             return {
#             #                 'status_code': 200,
#             #                 'message': 'success',
#             #                 'data': result_list
#             #             }

#             #         else:
#             #             return {
#             #                 'status_code': 500,
#             #                 'message': 'classification failed'
#             #             }
#             #     else:
#             #         return {
#             #             'status_code': 500,
#             #             'message': 'severity failed'
#             #     }
#             # else:
#             #     return {
#             #         'status_code': 500,
#             #         'message': 'ner failed'
#             #     }
#         else:
#             return {
#                 'status_code': 500,
#                 'message': 'qe failed'
#             }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }

# @app.get('/ner')
# async def scrap():
# # if __name__ == '__main__':
#     try:
#         # 1 Proses scraping, inisiasi modul ScrapProcess
#         # print('1 Step Passed')

#         # scrap = ScrapProcess()
#         # resultScrap = scrap.crawlNews()

#         # process = Process(target=scrap.crawlNews)
#         # process.start()
#         # process.join()

#         # 2 QE Expansion waht, jika hasil scraping success
#         # print('2 Step Passed')

#         # qe = QueryExpansion()
#         # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
#         # 3 NER when, who, where, jika hasil qe success
#         # if (resultQE == "success"):
#             # print('3 Step Passed')

#             ner = NER()
#             resultNER = ner.getValueNER()

#             if (resultNER == "success"):
#                 print('4 Step Passed')

#                 # severity = Severity()
#                 # resultSeverity=severity.getKeparahanVelue()

#                 # if (resultSeverity == "success"):
#                 #     print('5 Step Passed')

#                 #     classification = Classification()
#                 #     resultClassification=classification.getClassificationValue()

#                 #     if (resultClassification == "success"):
#                 #         print('6 Step Passed')
                        
#                 #         df_w = pd.read_csv('result/classification_res/result_final.csv')

#                 #         result_list = []

#                 #         for i in range(0, df_w.shape[0]):
#                 #             result = {
#                 #                 'title': str(df_w.iloc[i, 0]),
#                 #                 'kategori': 'kesehatan',
#                 #                 'nama_kejadian': str(df_w.iloc[i, 3]),
#                 #                 'waktu': str(df_w.iloc[i, 4]),
#                 #                 'orang_terlibat': str(df_w.iloc[i, 5]),
#                 #                 'provinsi': str(df_w.iloc[i, 6]),
#                 #                 'kabupaten': str(df_w.iloc[i, 7]),
#                 #                 'kecamatan': str(df_w.iloc[i, 8]),
#                 #                 'tingkat_keparahan': df_w.iloc[i, 11]
#                 #             }
#                 #             result_list.append(result)

#                 #         return {
#                 #             'status_code': 200,
#                 #             'message': 'success',
#                 #             'data': result_list
#                 #         }

#                 #     else:
#                 #         return {
#                 #             'status_code': 500,
#                 #             'message': 'classification failed'
#                 #         }
#                 # else:
#                 #     return {
#                 #         'status_code': 500,
#                 #         'message': 'severity failed'
#                 # }
#             else:
#                 return {
#                     'status_code': 500,
#                     'message': 'ner failed'
#                 }
#         # else:
#         #     return {
#         #         'status_code': 500,
#         #         'message': 'qe failed'
#         #     }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }

# @app.get('/sev')
# async def scrap():
# # if __name__ == '__main__':
#     try:
#         # 1 Proses scraping, inisiasi modul ScrapProcess
#         # print('1 Step Passed')

#         # scrap = ScrapProcess()
#         # resultScrap = scrap.crawlNews()

#         # process = Process(target=scrap.crawlNews)
#         # process.start()
#         # process.join()

#         # 2 QE Expansion waht, jika hasil scraping success
#         # print('2 Step Passed')

#         # qe = QueryExpansion()
#         # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
#         # 3 NER when, who, where, jika hasil qe success
#         # if (resultQE == "success"):
#             # print('3 Step Passed')

#             # ner = NER()
#             # resultNER = ner.getValueNER()

#             # if (resultNER == "success"):
#             #     print('4 Step Passed')

#                 severity = Severity()
#                 resultSeverity=severity.getKeparahanVelue()

#                 if (resultSeverity == "success"):
#                     print('5 Step Passed')

#                     # # classification = Classification()
#                     # # resultClassification=classification.getClassificationValue()

#                     # # if (resultClassification == "success"):
#                     # #     print('6 Step Passed')
                        
#                     # #     df_w = pd.read_csv('result/classification_res/result_final.csv')

#                     # #     result_list = []

#                     # #     for i in range(0, df_w.shape[0]):
#                     # #         result = {
#                     # #             'title': str(df_w.iloc[i, 0]),
#                     # #             'kategori': 'kesehatan',
#                     # #             'nama_kejadian': str(df_w.iloc[i, 3]),
#                     # #             'waktu': str(df_w.iloc[i, 4]),
#                     # #             'orang_terlibat': str(df_w.iloc[i, 5]),
#                     # #             'provinsi': str(df_w.iloc[i, 6]),
#                     # #             'kabupaten': str(df_w.iloc[i, 7]),
#                     # #             'kecamatan': str(df_w.iloc[i, 8]),
#                     # #             'tingkat_keparahan': df_w.iloc[i, 11]
#                     # #         }
#                     # #         result_list.append(result)

#                     # #     return {
#                     # #         'status_code': 200,
#                     # #         'message': 'success',
#                     # #         'data': result_list
#                     # #     }

#                     # else:
#                     #     return {
#                     #         'status_code': 500,
#                     #         'message': 'classification failed'
#                     #     }
#                 else:
#                     return {
#                         'status_code': 500,
#                         'message': 'severity failed'
#                 }
#             # else:
#             #     return {
#             #         'status_code': 500,
#             #         'message': 'ner failed'
#             #     }
#         # else:
#         #     return {
#         #         'status_code': 500,
#         #         'message': 'qe failed'
#         #     }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }

# @app.get('/class')
# async def scrap():
# # if __name__ == '__main__':
#     try:
#         # 1 Proses scraping, inisiasi modul ScrapProcess
#         # print('1 Step Passed')

#         # scrap = ScrapProcess()
#         # resultScrap = scrap.crawlNews()

#         # process = Process(target=scrap.crawlNews)
#         # process.start()
#         # process.join()

#         # 2 QE Expansion waht, jika hasil scraping success
#         # print('2 Step Passed')

#         # qe = QueryExpansion()
#         # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
#         # 3 NER when, who, where, jika hasil qe success
#         # if (resultQE == "success"):
#             # print('3 Step Passed')

#             # ner = NER()
#             # resultNER = ner.getValueNER()

#             # if (resultNER == "success"):
#             #     print('4 Step Passed')

#                 # severity = Severity()
#                 # resultSeverity=severity.getKeparahanVelue()

#                 # if (resultSeverity == "success"):
#                 #     print('5 Step Passed')

#                     classification = Classification()
#                     resultClassification=classification.getClassificationValue()

#                     if (resultClassification == "success"):
#                         print('6 Step Passed')
                        
#                         # df_w = pd.read_csv('result/classification_res/result_final.csv')

#                         #ambil dari db
#                         newsscrapped = []
#                         try:
#                             cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
#                             cursor = cnx.cursor()
#                             cursor.execute("SELECT qe_what, ner_when, ner_who, ner_prov, ner_kab, ner_kec, class_classification FROM berita where berita_topik_id = 4")
#                             myresult = cursor.fetchall()
#                             for row in myresult:
#                                 newsscrapped.append(row)

#                         except mysql.connector.Error as err:
#                             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#                                 print("Something is wrong with your user name or password")
#                             elif err.errno == errorcode.ER_BAD_DB_ERROR:
#                                 print("Database does not exist")
#                             else:
#                                 print(err)
#                         else:
#                             cursor.close()
#                             cnx.close()

#                         #ambil dari db
#                         whatberita = []
#                         tglasliberita = []
#                         whoberita = []
#                         provinsiberita = []
#                         kabupatenberita = []
#                         kecamatanberita = []
#                         keparahanberita = []
                        
#                         whatberita, tglasliberita, whoberita, provinsiberita, kabupatenberita, kecamatanberita, keparahanberita= zip(*newsscrapped)

#                         result_list = []

#                         for i in range(0, len(newsscrapped)):
#                             result = {
#                                 'title' : '',
#                                 'kategori' : 'kesehatan',
#                                 'nama_kejadian' : whatberita[i],
#                                 'waktu' : tglasliberita[i],
#                                 'orang_terlibat' : whoberita[i],
#                                 'provinsi' : provinsiberita[i],
#                                 'kabupaten' : kabupatenberita[i],
#                                 'kecamatan' : kecamatanberita[i],
#                                 'tingkat_keparahan' : keparahanberita[i]
#                             }
#                             result_list.append(result)

#                         return {
#                             'status_code': 200,
#                             'message': 'success',
#                             'data': result_list
#                         }

#                     else:
#                         return {
#                             'status_code': 500,
#                             'message': 'classification failed'
#                         }
#                 # else:
#                 #     return {
#                 #         'status_code': 500,
#                 #         'message': 'severity failed'
#                 # }
#             # else:
#             #     return {
#             #         'status_code': 500,
#             #         'message': 'ner failed'
#             #     }
#         # else:
#         #     return {
#         #         'status_code': 500,
#         #         'message': 'qe failed'
#         #     }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }
