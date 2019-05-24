import requests
import lxml.html
import configparser
import os
from time import sleep

config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)
# gets new egg url from config file
NEW_EGG = config.get('urls', 'new-egg')



#scapper for amazon using https://www.amazon.com/s?k=RAM&i=electronics&qid=1558543022&ref=sr_pg_1

def amazonScaper(url):

    return 0
#scapper for newEgg using https://www.newegg.com/p/pl?d=ram&N=-1&isNodeId=1&Submit=ENE&DEPA=0&Order=BESTMATCH
#doesnt get the first three items from the first page and does not scraper the first item from every page after
#every scrape includes the first item of the next page as the last item of the current page
#fix above later
#takes a url and a filename (both strings)
def newEggScaper(url,filename,writeMode):

    html = requests.get(url,timeout = 5)
    doc = lxml.html.fromstring(html.content)


    item_blocks = doc.xpath('.//div[@class="item-container   "]')

    #writes all ram values to a text file
    file = open(filename,writeMode)

    for item in item_blocks:

        file.write(item.xpath('.//a[@class="item-title"]')[0].text_content() + ",")
        file.write(item.xpath('.//li[@class="price-current"]')[0].text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0] +"\r\n")


    file.close()
    return 0

def newEggPageScraper(filename,numOfPages):

    urlname = "https://www.newegg.com/p/pl?Submit=ENE&N=-1&IsNodeId=1&d=ram&bop=And&Page=2&PageSize=36&order=BESTMATCH"
    num = 1


    while num <= numOfPages:

        a = newEggScaper(urlname,filename,"a+")

        url = "https://www.newegg.com/p/pl?Submit=ENE&N=-1&IsNodeId=1&d=ram&bop=And&Page=%d&PageSize=36&order=BESTMATCH" % num
        print("sleeping...")
        sleep(5)
        num = num + 1

    return 0


if __name__ == "__main__":
    print("hello")
    #item_blocks = doc.xpath('.//div[@class="item-container   "]')
    #items = doc.xpath('//div[@class="items-view is-grid"]')
    #gets the nanes directly
    #block.xpath('.//a[@class="item-title"]')[0].text_content()
    #item_names = new_releases.xpath('.//a[@class="item-title"]')
    #price_items = html_block.xpath('.//li[@class="price-current"]'/text())
    #stuff = newEggScaper(newEggurl,"ram.txt","w+")
    a = newEggPageScraper("bam.txt",2)
    #price.text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0]
