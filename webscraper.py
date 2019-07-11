#!/bin/python

import callshandlers
import page_parser
import mysql_pages
import mysql.connector as mysql
import configparser
import time
config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)
t1 = time.time()
pool = callshandlers.SubprocessPool(10)


lists = ["curl -ss https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611","curl -ss https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611",
"curl -ss https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-2?Tid=7611","curl -ss https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-3?Tid=7611",
"curl -ss https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1","curl -ss https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_2",
"curl -ss https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_3","curl -ss https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=1&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
"curl -ss https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=2&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter",
"curl -ss https://www.microcenter.com/search/search_results.aspx?N=4294966965&NTK=all&NR=&sku_list=&page=3&cat=Desktop-Memory/RAM-:-Computer-Memory-:-Computer-Parts-:-MicroCenter"]

for item in lists:
    pool.subprocess(item)

pool.execute()
print(time.time()-t1)

# needs to be populated with all the urls called
