from asyncore import dispatcher
import scrapy
from urllib.parse import urlparse
import html2text
import pandas as pd
import re
from bs4 import BeautifulSoup
from scrapy import Request
import signal
import os
from datetime import date, datetime, timedelta
import locale
import mysql.connector
from mysql.connector import errorcode

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = [
        "detik.com",
        "kompas.com",
        "tempo.co",
        "tribunnews.com"
    ]
    detik_url = []
    tribun_url = []
    kompas_url = []
    tempo_url = []
    detik_lastdate = ''
    tribun_lastdate = ''
    tempo_lastdate = ''
    kompas_lastdate = ''

    start_urls = []
    #mengambil keyword
    try:
        cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
        cursor = cnx.cursor()

        #simpan tanggal terakhir dari berita yang di scrap masing-masing situs berita
        detik_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.detik.com' AND berita_topik_id = 4)")
        cursor.execute(detik_last)
        detiklast = cursor.fetchall()
        if not detiklast:
            detik_lastdate = datetime.min
        else:
            tuplelast = detiklast[0]
            detik_lastdate = tuplelast[0]

        kompas_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.kompas.com' AND berita_topik_id = 4)")
        cursor.execute(kompas_last)
        kompaslast = cursor.fetchall()
        if not kompaslast:
            kompas_lastdate = datetime.min
        else:
            tuplelast = kompaslast[0]
            kompas_lastdate = tuplelast[0]

        tribun_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.tribunnews.com' AND berita_topik_id = 4)")
        cursor.execute(tribun_last)
        tribunlast = cursor.fetchall()
        if not tribunlast:
            tribun_lastdate = datetime.min
        else:
            tuplelast = tribunlast[0]
            tribun_lastdate = tuplelast[0]

        tempo_last = ("SELECT berita_qdate FROM berita WHERE berita_qdate IN (SELECT max(berita_qdate) FROM berita where berita_source = 'www.tempo.co' AND berita_topik_id = 4)")
        cursor.execute(tempo_last)
        tempolast = cursor.fetchall()
        if not tempolast:
            tempo_lastdate = datetime.min
        else:
            tuplelast = tempolast[0]
            tempo_lastdate = tuplelast[0]

        #topik_id = 3 (kecelakaan)
        querydetik = ("SELECT nama_keyword FROM keyword WHERE source='detik' AND topik_id=4")
        querytribun = ("SELECT nama_keyword FROM keyword WHERE source='tribun' AND topik_id=4")
        querykompas = ("SELECT nama_keyword FROM keyword WHERE source='kompas' AND topik_id=4")
        querytempo = ("SELECT nama_keyword FROM keyword WHERE source='tempo' AND topik_id=4")

        cursor.execute(querydetik)
        detik = cursor.fetchall()
        for row in detik:
            hasilstr = ''.join(row)
            hasilstr = hasilstr.replace(" ", "%20")
            detik_url.append(hasilstr)

        cursor.execute(querytribun)
        tribun = cursor.fetchall()
        for row in tribun:
            hasilstr = ''.join(row)
            tribun_url.append(hasilstr)

        cursor.execute(querykompas)
        kompas = cursor.fetchall()
        for row in kompas:
            hasilstr = ''.join(row)
            hasilstr = hasilstr.replace(" ", "%20")
            kompas_url.append(hasilstr)

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

    #memasukkan keyword ke url
    for value in detik_url:
        start_urls.append("https://www.detik.com/search/searchall?query=" + str(value)+ "&sortby=time&sorttime=3&fromdatex="+past_month + "&todatex=" + urldate)
    for value in tribun_url:
        start_urls.append("https://www.tribunnews.com/tag/" + str(value))
    for value in kompas_url:
        start_urls.append("https://www.kompas.com/tag/" + str(value) + "?sort=desc")
    for value in tempo_url:
        start_urls.append("https://www.tempo.co/search?waktu=1bulan&kanal=&subkanal=&domain=&q=" + str(value))

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
    skipped_subdomain = ["travel", "20", "finance", "inet",
                         "hot", "sport", "oto", "health", "food", "foto", "wolipop","otomotif","internasional"] #nentuinnya darimana? ini yang dari footer?
    tempo_skip_subdomain = ["seleb", "dunia", "otomotif", "travel", "bisnis", "sport", "difabel", "tekno", "www", "kolom", "gaya", "fokus", "bola","en","cantik"]
    skipped_parsed_link_path = ["seleb", "superskor", "internasional", "otomotif"]
    page_number_kompas = 2
    page_number_tribun = 2
    page_number_tempo = 2
    page_number_detik = 2

    def __init__(self, *a, **kw):
        super(NewsSpider, self).__init__(*a, **kw)
        # dispatcher.connect(self.spider_closed, signal.Signals.spider_closed)

    def preprocessing(self, berita):
        s = str(berita)
        s = s.replace('\n', ' ')
        s = s.replace('\r', ' ')
        tokens = [token for token in s.split(" ") if token != ""]

        T = [t for t in tokens]
        return ' '.join(T)

    def parse(self, response):
        parsing_url = urlparse(response.request.url)

        domain = parsing_url.netloc

        if self.current_url != response.request.url:
            self.current_url = response.request.url
            self.visited.clear()

        if (domain == "www.detik.com"):
            self.domain_detik = domain
            for article in response.css("article"):

                link = article.css("a::attr(href)").extract_first()
                newsdate = article.css("span.date::text").extract_first()
                repnewsdate = newsdate.replace(" WIB", "")
                date_format = datetime.strptime(repnewsdate, "%A, %d %b %Y %H:%M")
                parsed_link = urlparse(link)
                self.current_subdomain = parsed_link.hostname.split('.')[0]

                if(self.detik_lastdate > date_format):
                    start_url = NewsSpider.start_urls.pop()
                    yield Request(start_url, self.parse, meta=meta)
                elif (self.current_subdomain not in self.skipped_subdomain) and \
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
                        yield response.follow(link, self.parse_detik) #ngeklik linknya
            
            #pagination
            for navbutton in response.css("div.paging"):
                np = navbutton.css("img").extract()
                next_page_lastel = np[-1]
                cur_url = self.current_url
                if next_page_lastel is not None and ("Kanan" in next_page_lastel):
                    next_page = cur_url + "&page=" + str(NewsSpider.page_number_detik)
                    NewsSpider.page_number_detik += 1
                    yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)
                else:
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

            
        #tempo
        elif (domain == "www.tempo.co"):
            self.domain_tempo = domain
            cur_url = self.start_urls[0]
            stop_search = 0
            cek = response.css("h2.titlebox::text").extract()
            if ("tidak" in cek[1]):
                stop_search = 1
            for article in response.css("div.ft240"): #bisa keprint 2x
                
                link = article.css("a::attr(href)").extract_first()
                # link = urlparse(link)
                parsed_link = urlparse(link)
                self.current_subdomain = parsed_link.hostname.split('.')[0]
                article_date = article.css("h4.date::text").extract_first()
                splitdate = article_date.split(' ')
                intsplitdate = int(splitdate[0])
                if ("jam" in splitdate[1]):
                    tglartikel = datetime.now() - timedelta(hours=intsplitdate)
                elif ("hari" in splitdate[1]):
                    tglartikel = datetime.now() - timedelta(days=intsplitdate)

                if(self.tempo_lastdate > tglartikel):
                    start_url = NewsSpider.start_urls.pop()
                    yield Request(start_url, self.parse, meta=meta)
                elif (self.current_subdomain not in self.tempo_skip_subdomain) and \
                    (self.tempo_lastdate < tglartikel) and \
                    stop_search == 0:
                    yield response.follow(link, self.parse_tempo) #ngeklik linknya

            #pagination
            if (stop_search == 0):
                for navbutton in response.css("ul.pagging"):
                    np = navbutton.css("i.fa").extract_first()
                    if np is not None:
                        next_page = cur_url + "&page=" + str(NewsSpider.page_number_tempo)
                        NewsSpider.page_number_tempo += 1
                        yield scrapy.Request(next_page, callback=self.parse, headers=self.headers)
            else:
                NewsSpider.page_number_tempo = 2
                if("search" in parsing_url.path):
                    try:
                        start_url = NewsSpider.start_urls.pop()
                    except IndexError:
                        # nothing left to do
                        return
                    else:
                        meta = {'start_urls': self.start_urls}
                        yield Request(start_url, self.parse, meta=meta)

        #tribun
        elif (domain == "www.tribunnews.com"):
            self.domain_tribun = domain
            stop_page = 0
            now = datetime.now()
            currtime = now.strftime("%H:%M:%S")

            for article in response.css("ul.lsi"):
                for detailarticle in article.css("li.ptb15"):
                    for articlelink in detailarticle.css("div.fr"):
                        link_pure = articlelink.css("a::attr(href)").extract_first()
                        link = link_pure + "?page=all"
                        parsed_link = urlparse(link)
                        self.current_subdomain = parsed_link.hostname.split('.')[0]
                    for articledate in detailarticle.css("div.grey"):
                        article_date = articledate.css("time.grey::text").extract_first()
                        article_split = article_date.partition(' ')[2]
                        if("Januari" in article_split):
                            article_split = article_split.replace("Januari", "01")
                        elif("Februari" in article_split):
                            article_split = article_split.replace("Februari", "02")
                        elif("Maret" in article_split):
                            article_split = article_split.replace("Maret", "03")
                        elif("April" in article_split):
                            article_split = article_split.replace("April", "04")
                        elif("Mei" in article_split):
                            article_split = article_split.replace("Mei", "05")
                        elif("Juni" in article_split):
                            article_split = article_split.replace("Juni", "06")
                        elif("Juli" in article_split):
                            article_split = article_split.replace("Juli", "07")
                        elif("Agustus" in article_split):
                            article_split = article_split.replace("Agustus", "08")
                        elif("September" in article_split):
                            article_split = article_split.replace("September", "09")
                        elif("Oktober" in article_split):
                            article_split = article_split.replace("Oktober", "10")
                        elif("November" in article_split):
                            article_split = article_split.replace("November", "11")
                        elif("Desember" in article_split):
                            article_split = article_split.replace("Desember", "12")
                        if ("lalu" not in article_split):
                            article_rep = article_split.replace(" ", "/",2)
                            if len(article_rep) == 11:
                                trudate = article_rep[:10]
                            elif len(article_rep) < 11 :
                                trudate = "0"+ article_rep[:9]
                            tgl_str = trudate + " " + currtime
                            tgl2 = datetime.strptime(tgl_str, '%d/%m/%Y %H:%M:%S') 
                            # tgl = datetime.strptime(trudate, '%d/%m/%Y')

                            if(self.tribun_lastdate > tgl2):
                                start_url = NewsSpider.start_urls.pop()
                                yield Request(start_url, self.parse, meta=meta)
                            elif tgl2 > NewsSpider.past_month_date and stop_page == 0 and \
                                (self.current_subdomain not in self.skipped_subdomain) and \
                                (self.tribun_lastdate < tgl2) and \
                                    ("seleb" not in parsed_link.path) and \
                                        ("superskor" not in parsed_link.path) and \
                                            ("otomotif" not in parsed_link.path) and \
                                                ("nasional" not in parsed_link.path) and \
                                                    ("techno" not in parsed_link.path):

                                                yield response.follow(link, self.parse_tribun)
                            elif tgl2 < NewsSpider.past_month_date: #artikel lebih dari 1 bulan
                                stop_page = 1
                                break
                            else: #masuk di ignored subdomain
                                break
                        elif("lalu" in article_split) and \
                                (self.current_subdomain not in self.skipped_subdomain) and \
                                    ("seleb" not in parsed_link.path) and \
                                        ("superskor" not in parsed_link.path) and \
                                            ("otomotif" not in parsed_link.path) and \
                                                ("nasional" not in parsed_link.path) and \
                                                    ("techno" not in parsed_link.path):
                                                        yield response.follow(link, self.parse_tribun)
                        else:
                            break
                    if stop_page == 1:
                        break
            #pagination
            for navbutton in response.css("div.ptb10"):
                np = navbutton.css("a::text").extract()
                cur_url = self.current_url
                if "Next" in np and stop_page == 0:
                    next_page = cur_url + "?page=" + str(NewsSpider.page_number_tribun)
                    NewsSpider.page_number_tribun += 1
                    yield response.follow(next_page, callback=self.parse)
                else:
                    NewsSpider.page_number_tribun = 2
                    if(stop_page == 1):
                        try:
                            # start_url = self.start_urls.pop()
                            start_url = NewsSpider.start_urls.pop()
                        except IndexError:
                            # nothing left to do
                            return
                        else:
                            meta = {'start_urls': self.start_urls}
                            yield Request(start_url, self.parse, meta=meta) 
            
        #kompas
        elif (domain == "www.kompas.com"):
            self.domain_kompas = domain
            stop_page = 0
            for article in response.css("div.latest.ga--latest.mt2.clearfix.-newlayout"):
                for detailarticle in article.css("div.article__list"):
                    for articlelink in detailarticle.css("div.article__list__title"):
                        link_pure = articlelink.css("a::attr(href)").extract_first()
                        link = link_pure + "?page=all"
                        parsed_link = urlparse(link)
                        self.current_subdomain = parsed_link.hostname.split('.')[0]

                    for articledate in detailarticle.css("div.article__list__info"):
                        article_date = articledate.css("div.article__date::text").extract_first()
                        # tgl = article_date[0:10]
                        tgl2 = article_date[0:17]
                        tgl2_rep = tgl2.replace(",", "")
                        tgl2_time = datetime.strptime(tgl2_rep, '%d/%m/%Y %H:%M')
                        # tgl_time = datetime.strptime(tgl, '%d/%m/%Y')

                        if(self.kompas_lastdate > tgl2_time):
                            start_url = NewsSpider.start_urls.pop()
                            yield Request(start_url, self.parse, meta=meta)
                        elif tgl2_time > NewsSpider.past_month_date and \
                            (self.kompas_lastdate < tgl2_time) and \
                            stop_page == 0 and (self.current_subdomain not in self.skipped_subdomain) and \
                                ("motogp" not in parsed_link.path) and \
                                ("money" not in self.current_subdomain) and \
                                ("lifestyle" not in self.current_subdomain) and \
                                ("edukasi" not in self.current_subdomain) and \
                                ("stori" not in parsed_link.path) and \
                                ("cekfakta" not in parsed_link.path) and \
                                ("properti" not in parsed_link.path) and \
                                ("watch" not in parsed_link.path) and \
                                ("homey" not in parsed_link.path) and \
                                ("food" not in parsed_link.path) and \
                                ("hype" not in parsed_link.path) and \
                                ("edu" not in parsed_link.path) and \
                                ("tren" not in parsed_link.path) and \
                                    ("global" not in parsed_link.path): #kalo tgl sekarang belum di tanggal bulan lalu, klik linknya
                            yield response.follow(link, self.parse_kompas) #ngeklik linknya
                        elif tgl2_time < NewsSpider.past_month_date:
                            stop_page = 1
                            break
                        else:
                            break
                    if stop_page == 1:
                        break
                if stop_page == 1:
                    break 

            #pagination
            for navbutton in response.css("div.paging__wrap"):
                np = navbutton.css("a.paging__link--next").extract()
                cur_url = self.current_url
                if np is not None and stop_page == 0:
                    next_page = cur_url + "&page=" + str(NewsSpider.page_number_kompas)
                    NewsSpider.page_number_kompas += 1
                    yield response.follow(next_page, callback=self.parse)
                else:
                    NewsSpider.page_number_kompas = 2
                    if (stop_page == 1):
                        try:
                            start_url = NewsSpider.start_urls.pop() #INI
                        except IndexError:
                            # nothing left to do
                            return
                        else:
                            meta = {'start_urls': self.start_urls}
                            yield Request(start_url, self.parse, meta=meta) 

    #ngambil konten berita utamanya
    def parse_detik(self, response):
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

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
        date_format = datetime.strptime(rep_date, "%A, %d %b %Y %H:%M")

        descBody = response.css('div.detail__body-text').extract()
        description = ((self.textParser_detik(descBody[0]).replace("*", "") + " "))
        #masukin hasil scrap ke array berita[]
        if description != "" and title != "" and date != "":
            data = [str(tempTitle), str(date), str(
                description), str(self.domain_detik)]

            self.berita.append(data) 
            self.save_to_mysql(tempTitle, date, date_format, description, self.domain_detik)


    #ngambil konten berita utamanya
    def parse_tempo(self, response):
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

        title = response.css("h1.title::text").extract_first()
        date = response.css("h4.date::text").extract_first()
        tempTitle = self.preprocessing(title)
        date = date.replace(" WIB","")
        date_format = datetime.strptime(date, "%A, %d %B %Y %H:%M")
        date = datetime.strftime(date_format, "%A, %d %b %Y %H:%M")
        date = date + " WIB"

        descBody = response.css('div#isi').extract()

        description = ((self.textParser_tempo(descBody[0]).replace("*", "") + " "))
        description = description.encode("ascii","ignore")
        description = description.decode()
        fixdesc = description[2:]

        #masukin hasil scrap ke array berita[]
        if fixdesc != "" and title != "" and date != "":
            data = [str(tempTitle), str(date), str(
                fixdesc), str(self.domain_tempo)]

            self.berita.append(data)
            self.save_to_mysql(tempTitle, date, date_format, fixdesc, self.domain_tempo)


    #ngambil konten berita utamanya
    def parse_tribun(self, response):
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

        title = response.css("h1.f50::text").extract_first()
        date = response.css("time.grey::text").extract_first()

        tempTitle = self.preprocessing(title)

        date = date.replace(" WIB","")
        date_format = datetime.strptime(date, "%A, %d %B %Y %H:%M")
        date = datetime.strftime(date_format, "%A, %d %b %Y %H:%M")
        date = date + " WIB"

        descBody = response.css('div.txt-article').extract()
        description = ((self.textParser_tribun(descBody[0]).replace("*", "") + " ")) #tinggal ignore baca juga terakhir
        description = description.encode("ascii","ignore")
        description = description.decode()
        #masukin hasil scrap ke array berita[]
        if description != "" and title != "" and date != "":
            data = [str(tempTitle), str(date), str(
                description), str(self.domain_tribun)]

            self.berita.append(data)
            self.save_to_mysql(tempTitle, date, date_format, description, self.domain_tribun)

    def parse_kompas(self, response):
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
        title = response.css("h1.read__title::text").extract_first()
        date_full = response.css("div.read__time::text").extract_first()
        date = date_full.replace(' - ', '')
        daterep = date.replace(',', '').replace('WIB', '')
        date_format2 = datetime.strptime(daterep, '%d/%m/%Y %H:%M ')
        takedate = date.split(',')[0]
        taketime = date.split(',')[1]
        date_format = datetime.strptime(takedate, "%d/%m/%Y")
        day = date_format.strftime('%A, %d %b %Y')
        comb = day + taketime

        tempTitle = self.preprocessing(title)

        date = comb

        descBody = response.css('div.read__content').extract()
        description = ((self.textParser_kompas(descBody[0]).replace("*", "") + " "))
        description = description.encode("ascii","ignore")
        description = description.decode()

        #masukin hasil scrap ke array berita[]
        if description != "" and title != "" and date != "":
            data = [str(tempTitle), str(date), str(
                description), str(self.domain_kompas)]

            self.berita.append(data)
            self.save_to_mysql(tempTitle, date, date_format2, description, self.domain_kompas)
    
    def save_to_mysql(self, title, date, qdate, description, source):
        try:
            cnx = mysql.connector.connect(user = 'root', password='Password', database = 'Petakabar')
            cursor = cnx.cursor()
            add_news = ("INSERT IGNORE INTO berita "
                        "(berita_title, berita_date, berita_qdate, berita_desc, berita_source, berita_topik_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s)"
                       )
            topik = 4 #id topik kesehatan
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

    def textParser_detik(self, text):
        # return text
        soup = BeautifulSoup(text, features='lxml')
        for table in soup.find_all("table", {'class': 'linksisip'}):
            table.decompose()

        for table2 in soup.find_all("table", {'class': 'pic_artikel_sisip_table'}):
            table2.decompose()

        for divTag in soup.find_all("div", {'class': 'detail__body-tag'}):
            divTag.decompose()

        for divAd in soup.find_all("div", {'class': 'paradetail'}):
            divAd.decompose()

        for divVideo in soup.find_all("div", {'class': 'sisip_video_ds'}):
            divVideo.decompose()

        for divVideo1 in soup.find_all("div", {'class': 'newlist-double'}):
            divVideo1.decompose()

        for divVideo2 in soup.find_all("iframe", {"class": "video20detik_0"}):
            divVideo2.decompose()

        for unusedStrong in soup.find_all("strong"):
            unusedStrong.decompose()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(str(soup))
    
    def textParser_tempo(self, text):
        # return text
        soup = BeautifulSoup(text, features='lxml')
        for paralax in soup.find_all("div", {"class": "parallax-box"}):
            paralax.decompose()
        for unusedStrong in soup.find_all("strong"):
            unusedStrong.decompose()
        for unusedspan in soup.find_all("b"):
            unusedspan.decompose()
        for em in soup.find_all("em"):
            em.decompose()
        for bacajuga in soup.find_all(string=re.compile("Baca")): #cek kalo ada "baca", kalo ada dihapus
            par = bacajuga.find_parent("p")
            par.decompose()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(str(soup))

    def textParser_tribun(self, text):
        # return text
        soup = BeautifulSoup(text, features='lxml')
        for ads in soup.find_all("div", {"class": "ads-placeholder"}):
            ads.decompose()
        for p in soup.find_all("p", {"class": "baca"}):
            p.decompose()
        for ads2 in soup.find_all("div", {"class": "ads-placeholder-inside"}):
            ads2.decompose()
        for figure in soup.find_all("figure", {"class": "image"}):
            figure.decompose()
        for unusedStrong in soup.find_all("strong"):
            unusedStrong.decompose()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(str(soup))

    def textParser_kompas(self, text):
        # return text
        soup = BeautifulSoup(text, features='lxml')
        for adiframe in soup.find_all("iframe"):
            adiframe.decompose()
        for gallery in soup.find_all("div", {"class": "-gallery"}):
            gallery.decompose()
        for adspan in soup.find_all("span", {"class": "ads-on-body"}):
            adspan.decompose()
        for adspan2 in soup.find_all("span", {"class": "read__bacajuga"}):
            adspan2.decompose()
        for unusedStrong in soup.find_all("strong"):
            unusedStrong.decompose()
        for i in soup.find_all("i"):
            i.decompose()

        converter = html2text.HTML2Text()
        converter.ignore_links = True

        return converter.handle(str(soup))
