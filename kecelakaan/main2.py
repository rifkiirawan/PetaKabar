from submodule.Classification import Classification
from submodule.NER import NER
from submodule.QueryExpansion import QueryExpansion
from submodule.ScrapProcess import ScrapProcess
from typing import Union
from fastapi import FastAPI
import pandas as pd

from submodule.Severity import Severity

app = FastAPI()

# @app.get('/')
# def root():
#     return "hello :)"

# @app.get('/scrap')
# def scrap():
if __name__ == '__main__':
    # try:
        # 1 Proses scraping, inisiasi modul ScrapProcess
        print('1 Step Passed')

        # scrap = ScrapProcess()
        # resultScrap = scrap.crawlNews()

        # # 2 QE Expansion waht, jika hasil scraping success
        # if (resultScrap == "success"):
        print('2 Step Passed')

        qe = QueryExpansion()
        resultQE = qe.getWhatFromText("bencana apa yang terjadi")    
        
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
                        
#                             return {
#                                 'status_code': 200,
#                                 'message': 'success'
#                             }
#                         else:
#                             return {
#                                 'status_code': 500,
#                                 'message': 'severity failed'
#                             }
#                     else:
#                         return {
#                             'status_code': 500,
#                             'message': 'severity failed'
#                     }
#                 else:
#                     return {
#                         'status_code': 500,
#                         'message': 'ner failed'
#                     }
#             else:
#                 return {
#                     'status_code': 500,
#                     'message': 'qe failed'
#                 }
#         else:
#             return {
#                 'status_code': 500,
#                 'message': 'scrap failed'
#             }
#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }
    

# @app.get('/result')
# def result():
# # if __name__ == '__main__':
#     try:
#         pd_w = pd.read_csv('result/4w/result_sof4.csv')

#         result_list = []
#         for i in range(0, pd_w.shape[0]):
#             result_list.append({
#                 'title': pd_w.iloc[i, 0],
#                 'kategori':'kecelakaan',
#                 'nama_kejadian': pd_w.iloc[i, 3],
#                 'waktu': pd_w.iloc[i, 4],
#                 'orang_terlibat': pd_w.iloc[i, 5],
#                 'provinsi': pd_w.iloc[i, 6],
#                 'kabupaten': pd_w.iloc[i, 7],
#                 'kecamatan': pd_w.iloc[i, 8],
#                 'tingkat_keparahan': pd_w.iloc[i, 14],
#             })

#         return {
#             # 'status_code': 200,
#             # 'message': 'success',
#             'data': result_list
#         }

#     except Exception as error:
#         return {
#             'status_code': 500,
#             'message': error
#         }