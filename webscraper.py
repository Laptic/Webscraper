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

pool = callshandlers.SubprocessPool(10)
# needs to be populated with all the urls called