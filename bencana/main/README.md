### Integrated Geographical News Scrapper API

# For dataset (folder) & model (folder) content, can be downloaded here
https://itsacid-my.sharepoint.com/:f:/g/personal/syubbanfakhriya_18051_mhs_its_ac_id/EnrVKE200ClImNsoGyd42KkBMjD4H4Zrncc1PBIvDiIr2A?e=Uq1yrH

# Setup environment
1. Setup virtual env
> virtualenv venv

2. Activate virtualenv
> . venv/bin/activate

3. Install requirements
> pip install -r requirements.txt

4. Init scrapy (if not exist)
> scrapy startproject scrapper

# How to use
1. Start the server
> uvicorn main:app --reload
2. Scrap first then get result
> localhost:8000/scrap

# Configuration
1. Classification model (naive bayes, logistic regression, etc) name must be model.pkl, location in classification folder
2. Dataset for qe located in dataset/qe, the name must be look like the existing file
3. The indicator must be defined manually in Severity.py
4. Same as no 3, the indicator must be defined manually in Classification.py
5. Scrapy URL must be look like the existing example