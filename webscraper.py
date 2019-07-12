#!/bin/python

import requests
import multiprocessing
import page_parser
import mysql_pages
# import mysql.connector as mysql
import time
import lxml.html

HEADER = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
AMAZON_KEY = "amazon"
EGG_KEY = "newegg"
MICRO_KEY = "micro"
t1 = time.time()


WEBSITE_TYPE_DICT = {
    EGG_KEY: page_parser.new_egg_scraper,
    AMAZON_KEY: page_parser.amazon_scraper,
    MICRO_KEY: page_parser.micro_center_scraper
}


class CallObject(object):
    def __init__(self, website_type, url):
        self.website_type = website_type
        self.url = url


class ResultObject(object):
    def __init__(self, website_type, doc):
        self.website_type = website_type
        self.product_list = WEBSITE_TYPE_DICT[website_type](doc)

    def __str__(self):
        return str(self.product_list)


def web_call(call_object):
    session = requests.Session()
    session.headers.update(HEADER)
    html = session.get(call_object.url, timeout=5)
    doc = lxml.html.fromstring(html.content)
    result_obj = ResultObject(call_object.website_type, doc)
    return result_obj


lists = [
    "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611",
    "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611",
    "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611",
    "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-3?Tid=7611",
    "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1",
    "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_2",
    "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_3",
    "https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=1&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
    "https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=2&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
    "https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=3&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter"
]


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    call_objects = []
    for item in lists:
        if EGG_KEY in item:
            call_objects.append(CallObject(EGG_KEY, item))
        elif AMAZON_KEY in item:
            call_objects.append(CallObject(AMAZON_KEY, item))
        elif MICRO_KEY in item:
            call_objects.append(CallObject(MICRO_KEY, item))
    with multiprocessing.Pool(5) as p:
        result_objects = p.map(web_call, call_objects)
    t2 = time.time()
    print(t2 - t1)
    db = mysql_pages.connect()
    idNum = 25
    query = "INSERT INTO ram_parts (name,price,website,id) VALUES (%s,%s,%s,%s)"
    for item in result_objects:
        if item.website_type is EGG_KEY:
            mysql_pages.newEggInput(item.product_list, db, query, idNum)
        if item.website_type is AMAZON_KEY:
            mysql_pages.amazonInput(item.product_list, db, query, idNum)
        elif item.website_type is MICRO_KEY:
            mysql_pages.microcenterInput(item.product_list, db, query, idNum)

