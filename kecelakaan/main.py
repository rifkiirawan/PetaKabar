from submodule.Classification import Classification
from submodule.NER import NER
from submodule.QueryExpansion import QueryExpansion
from submodule.ScrapProcess import ScrapProcess
from typing import Union
from fastapi import FastAPI
import pandas as pd
from fastapi import FastAPI, BackgroundTasks
from multiprocessing import Process

from submodule.Severity import Severity
from submodule.scrapper.scrapper.spiders.news_spider import NewsSpider

from twisted.internet import reactor

import mysql.connector
from mysql.connector import errorcode

app = FastAPI()


@app.get('/scrap')
async def scrap():
# if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        # print('1 Step Passed')

        scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        process = Process(target=scrap.crawlNews)
        process.start()
        process.join()

        # 2 QE Expansion waht, jika hasil scraping success
        print('2 Step Passed')

        qe = QueryExpansion()
        resultQE = qe.getWhatFromText("apa sebenarnya kejadian kecelakaan yang terjadi diberita tersebut")
        
        # 3 NER when, who, where, jika hasil qe success
        if (resultQE == "success"):
            print('3 Step Passed')

            ner = NER()
            resultNER = ner.getValueNER()

            if (resultNER == "success"):
                print('4 Step Passed')

                severity = Severity()
                resultSeverity=severity.getKeparahanVelue()

                if (resultSeverity == "success"):
                    print('5 Step Passed')

                    classification = Classification()
                    resultClassification=classification.getClassificationValue()

                    if (resultClassification == "success"):
                        print('6 Step Passed')
                        
                        df_w = pd.read_csv('result/classification_res/result_final.csv')

                        #ambil dari db
                        newsscrapped = []
                        try:
                            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
                            cursor = cnx.cursor()
                            cursor.execute("SELECT qe_what, ner_when, ner_who, ner_prov, ner_kab, ner_kec, class_classification FROM berita where berita_topik_id = 3")
                            myresult = cursor.fetchall()
                            for row in myresult:
                                newsscrapped.append(row)

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

                        #ambil dari db
                        whatberita = []
                        tglasliberita = []
                        whoberita = []
                        provinsiberita = []
                        kabupatenberita = []
                        kecamatanberita = []
                        keparahanberita = []
                        
                        whatberita, tglasliberita, whoberita, provinsiberita, kabupatenberita, kecamatanberita, keparahanberita= zip(*newsscrapped)

                        result_list = []

                        for i in range(0, len(newsscrapped)):
                            result = {
                                'title' : '',
                                'kategori' : 'kecelakaan',
                                'nama_kejadian' : whatberita[i],
                                'waktu' : tglasliberita[i],
                                'orang_terlibat' : whoberita[i],
                                'provinsi' : provinsiberita[i],
                                'kabupaten' : kabupatenberita[i],
                                'kecamatan' : kecamatanberita[i],
                                'tingkat_keparahan' : keparahanberita[i]
                            }
                            result_list.append(result)

                        return {
                            'status_code': 200,
                            'message': 'success',
                            'data': result_list
                        }

                    else:
                        return {
                            'status_code': 500,
                            'message': 'classification failed'
                        }
                else:
                    return {
                        'status_code': 500,
                        'message': 'severity failed'
                }
            else:
                return {
                    'status_code': 500,
                    'message': 'ner failed'
                }
        else:
            return {
                'status_code': 500,
                'message': 'qe failed'
            }

    except Exception as error:
        return {
            'status_code': 500,
            'message': error
        }

@app.get('/qe')
async def scrap():
# if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        # print('1 Step Passed')

        # scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        # process = Process(target=scrap.crawlNews)
        # process.start()
        # process.join()

        # 2 QE Expansion waht, jika hasil scraping success
        # print('2 Step Passed')

        qe = QueryExpansion()
        resultQE = qe.getWhatFromText("apa sebenarnya kejadian kecelakaan yang terjadi diberita tersebut")
        
        # 3 NER when, who, where, jika hasil qe success
        if (resultQE == "success"):
            print('3 Step Passed')

            # ner = NER()
            # resultNER = ner.getValueNER()

            # if (resultNER == "success"):
            #     print('4 Step Passed')

            #     severity = Severity()
            #     resultSeverity=severity.getKeparahanVelue()

            #     if (resultSeverity == "success"):
            #         print('5 Step Passed')

            #         classification = Classification()
            #         resultClassification=classification.getClassificationValue()

            #         if (resultClassification == "success"):
            #             print('6 Step Passed')
                        
            #             df_w = pd.read_csv('result/classification_res/result_final.csv')

            #             result_list = []

            #             for i in range(0, df_w.shape[0]):
            #                 result = {
            #                     'title': str(df_w.iloc[i, 0]),
            #                     'kategori': 'kesehatan',
            #                     'nama_kejadian': str(df_w.iloc[i, 3]),
            #                     'waktu': str(df_w.iloc[i, 4]),
            #                     'orang_terlibat': str(df_w.iloc[i, 5]),
            #                     'provinsi': str(df_w.iloc[i, 6]),
            #                     'kabupaten': str(df_w.iloc[i, 7]),
            #                     'kecamatan': str(df_w.iloc[i, 8]),
            #                     'tingkat_keparahan': df_w.iloc[i, 11]
            #                 }
            #                 result_list.append(result)

            #             return {
            #                 'status_code': 200,
            #                 'message': 'success',
            #                 'data': result_list
            #             }

            #         else:
            #             return {
            #                 'status_code': 500,
            #                 'message': 'classification failed'
            #             }
            #     else:
            #         return {
            #             'status_code': 500,
            #             'message': 'severity failed'
            #     }
            # else:
            #     return {
            #         'status_code': 500,
            #         'message': 'ner failed'
            #     }
        else:
            return {
                'status_code': 500,
                'message': 'qe failed'
            }

    except Exception as error:
        return {
            'status_code': 500,
            'message': error
        }

@app.get('/ner')
async def scrap():
# if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        # print('1 Step Passed')

        # scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        # process = Process(target=scrap.crawlNews)
        # process.start()
        # process.join()

        # 2 QE Expansion waht, jika hasil scraping success
        # print('2 Step Passed')

        # qe = QueryExpansion()
        # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
        # 3 NER when, who, where, jika hasil qe success
        # if (resultQE == "success"):
            # print('3 Step Passed')

            ner = NER()
            resultNER = ner.getValueNER()

            if (resultNER == "success"):
                print('4 Step Passed')

                # severity = Severity()
                # resultSeverity=severity.getKeparahanVelue()

                # if (resultSeverity == "success"):
                #     print('5 Step Passed')

                #     classification = Classification()
                #     resultClassification=classification.getClassificationValue()

                #     if (resultClassification == "success"):
                #         print('6 Step Passed')
                        
                #         df_w = pd.read_csv('result/classification_res/result_final.csv')

                #         result_list = []

                #         for i in range(0, df_w.shape[0]):
                #             result = {
                #                 'title': str(df_w.iloc[i, 0]),
                #                 'kategori': 'kesehatan',
                #                 'nama_kejadian': str(df_w.iloc[i, 3]),
                #                 'waktu': str(df_w.iloc[i, 4]),
                #                 'orang_terlibat': str(df_w.iloc[i, 5]),
                #                 'provinsi': str(df_w.iloc[i, 6]),
                #                 'kabupaten': str(df_w.iloc[i, 7]),
                #                 'kecamatan': str(df_w.iloc[i, 8]),
                #                 'tingkat_keparahan': df_w.iloc[i, 11]
                #             }
                #             result_list.append(result)

                #         return {
                #             'status_code': 200,
                #             'message': 'success',
                #             'data': result_list
                #         }

                #     else:
                #         return {
                #             'status_code': 500,
                #             'message': 'classification failed'
                #         }
                # else:
                #     return {
                #         'status_code': 500,
                #         'message': 'severity failed'
                # }
            else:
                return {
                    'status_code': 500,
                    'message': 'ner failed'
                }
        # else:
        #     return {
        #         'status_code': 500,
        #         'message': 'qe failed'
        #     }

    except Exception as error:
        return {
            'status_code': 500,
            'message': error
        }

@app.get('/sev')
async def scrap():
# if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        # print('1 Step Passed')

        # scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        # process = Process(target=scrap.crawlNews)
        # process.start()
        # process.join()

        # 2 QE Expansion waht, jika hasil scraping success
        # print('2 Step Passed')

        # qe = QueryExpansion()
        # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
        # 3 NER when, who, where, jika hasil qe success
        # if (resultQE == "success"):
            # print('3 Step Passed')

            # ner = NER()
            # resultNER = ner.getValueNER()

            # if (resultNER == "success"):
            #     print('4 Step Passed')

                severity = Severity()
                resultSeverity=severity.getKeparahanVelue()

                if (resultSeverity == "success"):
                    print('5 Step Passed')

                    # # classification = Classification()
                    # # resultClassification=classification.getClassificationValue()

                    # # if (resultClassification == "success"):
                    # #     print('6 Step Passed')
                        
                    # #     df_w = pd.read_csv('result/classification_res/result_final.csv')

                    # #     result_list = []

                    # #     for i in range(0, df_w.shape[0]):
                    # #         result = {
                    # #             'title': str(df_w.iloc[i, 0]),
                    # #             'kategori': 'kesehatan',
                    # #             'nama_kejadian': str(df_w.iloc[i, 3]),
                    # #             'waktu': str(df_w.iloc[i, 4]),
                    # #             'orang_terlibat': str(df_w.iloc[i, 5]),
                    # #             'provinsi': str(df_w.iloc[i, 6]),
                    # #             'kabupaten': str(df_w.iloc[i, 7]),
                    # #             'kecamatan': str(df_w.iloc[i, 8]),
                    # #             'tingkat_keparahan': df_w.iloc[i, 11]
                    # #         }
                    # #         result_list.append(result)

                    # #     return {
                    # #         'status_code': 200,
                    # #         'message': 'success',
                    # #         'data': result_list
                    # #     }

                    # else:
                    #     return {
                    #         'status_code': 500,
                    #         'message': 'classification failed'
                    #     }
                else:
                    return {
                        'status_code': 500,
                        'message': 'severity failed'
                }
            # else:
            #     return {
            #         'status_code': 500,
            #         'message': 'ner failed'
            #     }
        # else:
        #     return {
        #         'status_code': 500,
        #         'message': 'qe failed'
        #     }

    except Exception as error:
        return {
            'status_code': 500,
            'message': error
        }

@app.get('/class')
async def scrap():
    # if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        # print('1 Step Passed')

        # scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        # process = Process(target=scrap.crawlNews)
        # process.start()
        # process.join()

        # 2 QE Expansion waht, jika hasil scraping success
        # print('2 Step Passed')

        # qe = QueryExpansion()
        # resultQE = qe.getWhatFromText("kasus penyakit apa yang terjadi")
        
        # 3 NER when, who, where, jika hasil qe success
        # if (resultQE == "success"):
            # print('3 Step Passed')

            # ner = NER()
            # resultNER = ner.getValueNER()

            # if (resultNER == "success"):
            #     print('4 Step Passed')

                # severity = Severity()
                # resultSeverity=severity.getKeparahanVelue()

                # if (resultSeverity == "success"):
                #     print('5 Step Passed')

                    classification = Classification()
                    resultClassification=classification.getClassificationValue()

                    if (resultClassification == "success"):
                        print('6 Step Passed')
                        
                        # df_w = pd.read_csv('result/classification_res/result_final.csv')

                        #ambil dari db
                        newsscrapped = []
                        try:
                            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
                            cursor = cnx.cursor()
                            cursor.execute("SELECT qe_what, ner_when, ner_who, ner_prov, ner_kab, ner_kec, class_classification FROM berita where berita_topik_id = 4")
                            myresult = cursor.fetchall()
                            for row in myresult:
                                newsscrapped.append(row)

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

                        #ambil dari db
                        whatberita = []
                        tglasliberita = []
                        whoberita = []
                        provinsiberita = []
                        kabupatenberita = []
                        kecamatanberita = []
                        keparahanberita = []
                        
                        whatberita, tglasliberita, whoberita, provinsiberita, kabupatenberita, kecamatanberita, keparahanberita= zip(*newsscrapped)

                        result_list = []

                        for i in range(0, len(newsscrapped)):
                            result = {
                                'title' : '',
                                'kategori' : 'kesehatan',
                                'nama_kejadian' : whatberita[i],
                                'waktu' : tglasliberita[i],
                                'orang_terlibat' : whoberita[i],
                                'provinsi' : provinsiberita[i],
                                'kabupaten' : kabupatenberita[i],
                                'kecamatan' : kecamatanberita[i],
                                'tingkat_keparahan' : keparahanberita[i]
                            }
                            result_list.append(result)

                        return {
                            'status_code': 200,
                            'message': 'success',
                            'data': result_list
                        }

                    else:
                        return {
                            'status_code': 500,
                            'message': 'classification failed'
                        }
                # else:
                #     return {
                #         'status_code': 500,
                #         'message': 'severity failed'
                # }
            # else:
            #     return {
            #         'status_code': 500,
            #         'message': 'ner failed'
            #     }
        # else:
        #     return {
        #         'status_code': 500,
        #         'message': 'qe failed'
        #     }

    except Exception as error:
        return {
            'status_code': 500,
            'message': error
        }
