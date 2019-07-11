#!/bin/python

import callshandlers
import page_parser
import mysql_pages
import mysql.connector as mysql
import configparser

config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)

PASSWORD = config.get('passwords', 'mysqlPassword')


db = mysql_pages.connect()

idNum = 25
query = "INSERT INTO ram_parts (name,price,website,id) VALUES (%s,%s,%s,%s)"
ramNewEggWebsite = "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611"
ramMicrocenterWebsite = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=true"
ramAmazonWebsite = "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1"