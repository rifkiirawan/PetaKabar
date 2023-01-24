### Geographical News Scrapper

# Setup environment

1. Setup virtual env

   > virtualenv venv

2. Activate virtualenv

   > . venv/Scripts/activate

3. Install requirements

   > pip install -r requirements.txt

4. Init scrapy (if not exist)
   > scrapy startproject scrapper

# How to use

1. Enter to the topic
   > cd kecelakaan
2. Start the server
   > uvicorn main:app --reload
3. Scrap first then get result
   > localhost:8000/scrap

# Configuration

1. Classification model (naive bayes, logistic regression, etc) name must be model.pkl, location in classification folder
2. Dataset for qe located in dataset/qe, the name must be look like the existing file
3. The indicator must be defined manually in Severity.py
4. Same as no 3, the indicator must be defined manually in Classification.py
5. Scrapy URL must be look like the existing example
