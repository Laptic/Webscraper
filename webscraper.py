#!/bin/python

import callshandlers
import requests
import multiprocessing
import page_parser
# import mysql.connector as mysql
import configparser
import time
import lxml.html

HEADER = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)
t1 = time.time()
pool = callshandlers.SubprocessPool(10)


def web_call(website):
    session = requests.Session()
    session.headers.update(HEADER)
    html = session.get(website, timeout=5)
    #doc = lxml.html.fromstring(html.content)
    return html.content

lists = ["https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611","https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611",
"https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611","https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-3?Tid=7611",
"https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1","https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_2",
"https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_3","https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=1&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
"https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=2&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
"https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=3&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter"]


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    with multiprocessing.Pool(5) as p:
        print(p.map(web_call, lists))
    t2 = time.time()
    print(t2 - t1)
