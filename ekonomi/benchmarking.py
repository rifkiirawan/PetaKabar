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

import time

app = FastAPI()


@app.get('/scrap')
async def scrap():
# if __name__ == '__main__':
    try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        startTime1 = time.time()
        print('1 Step Passed')

        scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        process = Process(target=scrap.crawlNews)
        process.start()
        process.join()

        print("--- scrapping %s seconds ---" % (round(time.time() - startTime1, 2)))

        # 2 QE Expansion waht, jika hasil scraping success
        startTime2 = time.time()
        print('2 Step Passed')

        qe = QueryExpansion()
        resultQE = qe.getWhatFromText("bencana apa yang terjadi")    
        
        print("--- qe %s seconds ---" % (round(time.time() - startTime2, 2)))

        # 3 NER when, who, where, jika hasil qe success
        if (resultQE == "success"):
            startTime3 = time.time()
            print('3 Step Passed')

            ner = NER()
            resultNER = ner.getValueNER()

            print("--- ner %s seconds ---" % (round(time.time() - startTime3, 2)))

            if (resultNER == "success"):
                startTime4 = time.time()
                print('4 Step Passed')

                severity = Severity()
                resultSeverity=severity.getKeparahanVelue()

                print("--- severity %s seconds ---" % (round(time.time() - startTime4, 2)))

                if (resultSeverity == "success"):
                    startTime5 = time.time()
                    print('5 Step Passed')

                    classification = Classification()
                    resultClassification=classification.getClassificationValue()

                    print("--- classification %s seconds ---" % (round(time.time() - startTime5, 2)))

                    if (resultClassification == "success"):
                        print('6 Step Passed')
                        
                        df_w = pd.read_csv('result/classification_res/result_final.csv')

                        result_list = []

                        for i in range(0, df_w.shape[0]):
                            result = {
                                'title': str(df_w.iloc[i, 0]),
                                'kategori': 'bencana',
                                'nama_kejadian': str(df_w.iloc[i, 3]),
                                'waktu': str(df_w.iloc[i, 4]),
                                'orang_terlibat': str(df_w.iloc[i, 5]),
                                'provinsi': str(df_w.iloc[i, 6]),
                                'kabupaten': str(df_w.iloc[i, 7]),
                                'kecamatan': str(df_w.iloc[i, 8]),
                                'tingkat_keparahan': df_w.iloc[i, 13]
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