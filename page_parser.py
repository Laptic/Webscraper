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
#some names may have commas, so we have to replace them

def newEggScaper(url,filename,writeMode):

    html = requests.get(url,timeout = 5)
    doc = lxml.html.fromstring(html.content)

    #holds an array of html elements that contains a product
    item_blocks = doc.xpath('.//div[@class="item-container   "]')

    #writes all ram values to a text file
    file = open(filename,writeMode)

    #number the individual products
    position = 1
    for item in item_blocks:
        #add a way to differentiate between a new file and an old file
        #using this:https://stackoverflow.com/questions/20432912/writing-to-a-new-file-if-it-doesnt-exist-and-appending-to-a-file-if-it-does
        file.write(str(position)+". ")
        file.write(item.xpath('.//a[@class="item-title"]')[0].text_content() + ",")
        file.write(item.xpath('.//li[@class="price-current"]')[0].text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0] +"\r\n")
        position = position + 1

    file.close()

#scrapes for product information from microcenter
#takes a url(from microcenter), a filename to write to and a writemode for the file
#some names may have commas, so we gotta take that into account
#some names (ram for example) have extra words attached to the name, we we gotta take those out
def microCenterScaper(url,filename,writeMode):

#dont worry about for now, in progress
#------------------------------------------------------------------------------------
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    headers = {'User-Agent': user_agent}

    #proxies = {
    #"http": 'http://1.20.100.8:9050',
    #"https": 'http://1.20.100.8.39:9050'
    #}

    #html = requests.get(url,timeout = 5,headers=headers,proxies=proxies)

    #------------------------------------------------------------------------------------
    html = requests.get(url,timeout = 5,headers=headers)
    doc = lxml.html.fromstring(html.content)
    #I use name and brand blocks because the name does not include the brand of the product
    product_blocks = doc.xpath('.//li[@class="product_wrapper"]')
    file = open(filename,writeMode)
    position = 1
    for item in product_blocks:

        attribs = item.xpath('.//a[@data-name]')[0].attrib
        #add condition for if price is empty
        print(f'{position}. {attribs["data-brand"]} {attribs["data-name"]}, ${attribs["data-price"]}',file=file)
        print(file=file)
        #file.write(brand_blocks[pos] + " " + name_blocks[pos])
        #file.write(doc.xpath('.//li[@class="product_wrapper"]/div[@class="result_right"]/div[@class="details"]/div[@class="price_wrapper"]/div[@class="price"]/span[@class="price"]').text_content()  + "\r\n")
        position = position + 1

    file.close()


if __name__ == "__main__":
    print("hello")
    #item_blocks = doc.xpath('.//div[@class="item-container   "]')
    #items = doc.xpath('//div[@class="items-view is-grid"]')
    #gets the nanes directly
    #block.xpath('.//a[@class="item-title"]')[0].text_content()
    #item_names = new_releases.xpath('.//a[@class="item-title"]')
    #price_items = html_block.xpath('.//li[@class="price-current"]'/text())
    newEggRamUrl = "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611"
    newEggGraphicsUrl = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-1?Tid=7709"
    #stuff = newEggScaper(newEggGraphicsurl,"graphicsCards.txt","a+")
    microCenterRamUrl = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=false"
    microCenterGraphicsUrl = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966937&myStore=false"
    microCenterScaper(microCenterGraphicsUrl,"microRam.txt","w+")

    #a = newEggPageScraper("zam.txt",2)
    #price.text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0]
