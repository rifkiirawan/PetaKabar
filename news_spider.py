from .parsed_news_model import ParsedNewsModel
import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import html2text
import logging
import pandas as pd
from scrapy import signals
from pydispatch import dispatcher
import re
from bs4 import BeautifulSoup
from scrapy import Request
from datetime import date, datetime, timedelta
import locale
import mysql.connector
from mysql.connector import errorcode
# from scrapy.spiders import Rule
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class NewsSpider(scrapy.Spider):
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )        

    name = "news"
    allowed_domains = [
        "detik.com",
        "kompas.com",
        "tribunnews.com"
    ]
    detik_url = []
    tribun_url = []
    kompas_url = []
    tempo_url = []
    # added_url = []
    detik_lastdate = ''
    tribun_lastdate = ''
    tempo_lastdate = ''
    kompas_lastdate = ''
    start_urls = [
        # "https://www.detik.com/tag/gempa",
        # "https://www.detik.com/tag/banjir",
        # "https://www.detik.com/tag/kekeringan",
        # "https://www.detik.com/tag/gempa-bumi",
        # "https://www.detik.com/tag/longsor",
        # "https://www.detik.com/tag/angin-kencang",
        # "https://www.detik.com/tag/puting-beliung",
        # "https://www.detik.com/tag/pergerakan-tanah",
        # "https://www.detik.com/tag/kebakaran",
        # "https://www.detik.com/tag/erosi",
        # "https://www.detik.com/tag/abrasi",
    ]
    try:
        cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
        cursor = cnx.cursor()

        #simpan tanggal terakhir dari berita yang di scrap masing-masing situs berita
        detik_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.detik.com' AND berita_topik_id = 3)")
        cursor.execute(detik_last)
        detiklast = cursor.fetchall()
        # kalau db masih kosong, maka tanggal scrap berita terakhir = 0
        if not detiklast:
            detik_lastdate = datetime.min
            print('detiklastdate',detik_lastdate)
        else:
            tuplelast = detiklast[0]
            detik_lastdate = tuplelast[0]
            print("detik_lastdate", detik_lastdate)

        kompas_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.kompas.com' AND berita_topik_id = 3)")
        cursor.execute(kompas_last)
        kompaslast = cursor.fetchall()
        if not kompaslast:
            kompas_lastdate = datetime.min
            print('kompaslastdate',kompas_lastdate)
        else:
            tuplelast = kompaslast[0]
            kompas_lastdate = tuplelast[0]
            print("kompas_lastdate", kompas_lastdate)

        tribun_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.tribunnews.com' AND berita_topik_id = 3)")
        cursor.execute(tribun_last)
        tribunlast = cursor.fetchall()
        if not tribunlast:
            tribun_lastdate = datetime.min
            print('tribunlastdate',tribun_lastdate)
        else:
            tuplelast = tribunlast[0]
            tribun_lastdate = tuplelast[0]
            print("tribun_lastdate", tribun_lastdate)

        tempo_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.tempo.co' AND berita_topik_id = 3)")
        cursor.execute(tempo_last)
        tempolast = cursor.fetchall()
        if not tempolast:
            tempo_lastdate = datetime.min
            print('tempolastdate',tempo_lastdate)
        else:
            tuplelast = tempolast[0]
            tempo_lastdate = tuplelast[0]
            print("tempo_lastdate", tempo_lastdate)
        #topik_id = 3 (kecelakaan)
        # querydetik = ("SELECT nama_keyword FROM keyword WHERE source='detik' AND nama_keyword='tertabrak' AND topik_id=3")
        # querytribun = ("SELECT nama_keyword FROM keyword WHERE source='tribun' AND topik_id=3")
        # querykompas = ("SELECT nama_keyword FROM keyword WHERE source='kompas' AND topik_id=3")
        querytempo = ("SELECT nama_keyword FROM keyword WHERE source='tempo' AND topik_id=3")

        # cursor.execute(querydetik)
        # detik = cursor.fetchall()
        # for row in detik:
        #     hasilstr = ''.join(row)
        #     hasilstr = hasilstr.replace(" ", "%20")
        #     detik_url.append(hasilstr)

        # cursor.execute(querytribun)
        # tribun = cursor.fetchall()
        # for row in tribun:
        #     hasilstr = ''.join(row)
        #     tribun_url.append(hasilstr)

        # cursor.execute(querykompas)
        # kompas = cursor.fetchall()
        # for row in kompas:
        #     hasilstr = ''.join(row)
        #     hasilstr = hasilstr.replace(" ", "%20")
        #     kompas_url.append(hasilstr)

        cursor.execute(querytempo)
        tempo = cursor.fetchall()
        for row in tempo:
            hasilstr = ''.join(row)
            hasilstr = hasilstr.replace(" ", "+")
            tempo_url.append(hasilstr)

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

    countdup = 0
    #masukin tanggal di link detik
    now = datetime.now()
    date_format = '%d/%m/%Y'
    urldate = now.strftime(date_format)
    past_month_date = now - timedelta(days=31)
    past_month = datetime.strftime(past_month_date,date_format)
    # print ("urldate = ",urldate)

    #memasukkan keyword ke url
    for value in detik_url:
        start_urls.append("https://www.detik.com/search/searchall?query=" + str(value)+ "&sortby=time&sorttime=3&fromdatex="+past_month + "&todatex=" + urldate)
    for value in tribun_url:
        start_urls.append("https://www.tribunnews.com/tag/" + str(value))
    for value in kompas_url:
        start_urls.append("https://www.kompas.com/tag/" + str(value) + "?sort=desc")
    for value in tempo_url:
        start_urls.append("https://www.tempo.co/search?waktu=1bulan&kanal=&subkanal=&domain=&q=" + str(value))
    print("GABUNGAN=",start_urls)

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    interator = 0
    current_domain = ""
    current_subdomain = ""
    current_url = ""
    berita = []
    visited = []
    skipped_subdomain = ["travel", "20", "finance", "inet", "hot", "sport", "oto", "health", "food", "foto", "wolipop","otomotif","internasional"]
    tempo_skip_subdomain = ["seleb", "dunia", "otomotif", "travel", "bisnis", "sport", "difabel", "tekno", "www", "kolom", "gaya", "fokus", "bola"]
    skipped_parsed_link_path = ["seleb", "superskor", "internasional", "otomotif"]
    page_number_kompas = 2
    page_number_tribun = 2
    page_number_tempo = 2
    page_number_detik = 2

    def __init__(self, *a, **kw):
        super(NewsSpider, self).__init__(*a, **kw)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def preprocessing(self, berita):
        s = str(berita)
        s = s.replace('\n', ' ')
        s = s.replace('\r', ' ')
        tokens = [token for token in s.split(" ") if token != ""]
        
        T = [t for t in tokens]
        return ' '.join(T)

    def parse(self, response):
        print("masuk parse")
        parsing_url = urlparse(response.request.url)
        # if ("searchall" in parsing_url.path):
        #     try:
        #         start_url = self.start_urls.pop()
        #     except IndexError:
        #         # nothing left to do
        #         return
        #     else:
        #         meta = {'start_urls': self.start_urls}
        #         yield Request(start_url, self.parse, meta=meta)

        domain = parsing_url.netloc

        if self.current_url != response.request.url:
            self.current_url = response.request.url
            self.visited.clear()

        if (domain == "www.detik.com"):
            print("masuk detik")
            locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
            self.domain_detik = domain
            for article in response.css("article"):

                link = article.css("a::attr(href)").extract_first()

                newsdate = article.css("span.date::text").extract_first()

                repnewsdate = newsdate.replace(" WIB", "")

                date_format = datetime.strptime(repnewsdate, "%A, %d %b %Y %H:%M")

                parsed_link = urlparse(link)
                self.current_subdomain = parsed_link.hostname.split('.')[0]

                if (self.current_subdomain not in self.skipped_subdomain) and \
                    (self.detik_lastdate < date_format) and \
                    ("edu" not in parsed_link.path) and \
                    ("bisnis" not in parsed_link.path) and \
                    ("dw" not in parsed_link.path) and \
                    ("berita-ekonomi-bisnis" not in parsed_link.path) and \
                    ("internasional" not in parsed_link.path) and \
                    ("internasional-utama" not in parsed_link.path) and \
                    ("budaya" not in parsed_link.path) and \
                    ("foto-news" not in parsed_link.path)and \
                    ("detikflash" not in parsed_link.path)and \
                    ("detiktv" not in parsed_link.path)and \
                    ("bbc-world" not in parsed_link.path)and \
                    ("adv-nhl-detikcom" not in parsed_link.path):
                        yield response.follow(link, self.parse_detik)

            #PAGING
            for navbutton in response.css("div.paging"):
                # print("masuk for")
                np = navbutton.css("img").extract()
                next_page_lastel = np[-1]
                # print("nex", next_page_lastel)
                cur_url = self.current_url
                # print("CUR URL",cur_url)
                if next_page_lastel is not None and ("Kanan" in next_page_lastel):
                    # print("ada nextpage")
                    next_page = cur_url + "&page=" + str(NewsSpider.page_number_detik)
                    NewsSpider.page_number_detik += 1
                    # print("ADDED CUR URL", next_page)
                    # print("PAGE NUM", NewsSpider.page_number_detik)
                    # yield response.follow(next_page, callback=self.parse)
                    yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)
                else:
                    # print("gaada nextpage")
                    # print("SELF START URL", self.start_urls)
                    NewsSpider.page_number_detik = 2
                    if ("searchall" in parsing_url.path):
                        try:
                            start_url = NewsSpider.start_urls.pop()
                        except IndexError:
                            # nothing left to do
                            return
                        else:
                            meta = {'start_urls': self.start_urls}
                            yield Request(start_url, self.parse, meta=meta)

            # for navbutton in response.css('div.paging'):

            #     currentIndexView = navbutton.css("a::text").extract_first()

            #     if currentIndexView != None:
            #         if (currentIndexView.isnumeric() and (currentIndexView not in self.visited)):
            #             self.visited.append(currentIndexView)
            #             next_page = navbutton.css("a::attr(href)").extract_first()
                        
            #             if next_page is not None and ("tv." not in next_page):
            #                 next_page = response.urljoin(next_page)
            #                 yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)

            #     elif "next" in navbutton.css("a::attr(onclick)").extract_first():    
            #         next_page = navbutton.css("a::attr(href)").extract_first()
            #         if next_page is not None and ("tv." not in next_page):
            #             self.interator += 1
            #             next_page = response.urljoin(next_page)
            #         yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)


    def parse_detik(self, response):
        print("masuk parse_detik")
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
            
        # author = response.css("div.detail__author::text").extract_first()
        
        # desc = ""

        title = response.css("h1.detail__title::text").extract_first()

        if title != None:
            date = response.css("div.detail__date::text").extract_first()
        else:
            title = response.css("h1.mt5::text").extract_first()
            date = response.css("div.date::text").extract_first()
            
        tempTitle = self.preprocessing(title)

        if("Views" in date):
            date = date.split("|")[1]

        date = date
        date = date

        rep_date = date.replace(" WIB","")
        # print("rep_date", rep_date)
        date_format = datetime.strptime(rep_date, "%A, %d %b %Y %H:%M")
        # print("date_format", date_format)
 
        descBody = response.css('div.detail__body-text').extract()
        description = ((self.textParser_Detik(descBody[0]).replace("*","") + " "))
        
        if description != "" and title != "" and date != "":
            data = [str(tempTitle), str(date), str(description), str(self.current_domain)]

            self.berita.append(data)
            self.save_to_mysql(tempTitle, date, date_format, description, self.domain_detik)


    def spider_closed(self, spider):
        writer = pd.DataFrame(self.berita, columns=['title', 'date', 'description', 'source'])
        writer.to_csv('scrapped_news.csv', index=False, sep=',')

    def textParser_Detik(self, text):
        # return text
        soup = BeautifulSoup(text, features='lxml')
        for table in soup.find_all("table", {'class':'linksisip'}): 
            table.decompose()
        
        for table2 in soup.find_all("table", {'class': 'pic_artikel_sisip_table'}):
            table2.decompose()

        for divTag in soup.find_all("div", {'class':'detail__body-tag'}): 
            divTag.decompose()

        for divAd in soup.find_all("div", {'class': 'paradetail'}):
            divAd.decompose()

        for divVideo in soup.find_all("div", {'class':'sisip_video_ds'}): 
            divVideo.decompose()

        for divVideo1 in soup.find_all("div", {'class':'newlist-double'}):
            divVideo1.decompose()

        for divVideo2 in soup.find_all("iframe", {"class":"video20detik_0"}):
            divVideo2.decompose()

        for unusedStrong in soup.find_all("strong"):
            unusedStrong.decompose()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(str(soup))

    def save_to_mysql(self, title, date, qdate, description, source):
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            add_news = ("INSERT IGNORE INTO berita "
                        "(berita_title, berita_date, berita_qdate, berita_desc, berita_source, berita_topik_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s)"
                       )
            topik = 1 #id topik bencana
            data_news = (title, date, qdate, description, source, topik)
            cursor.execute(add_news, data_news)
            cnx.commit()            
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:
              if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
              elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
              else:
                print(err)
