import requests
import lxml.html
import configparser
from time import sleep

config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)
# gets new egg url from config file
NEW_EGG = config.get('urls', 'new-egg')

session = requests.Session()
session.headers.update({"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})

#scapper for amazon
def amazonScraper(url,filename,writeMode):

    html = session.get(url,timeout=5)
    doc = lxml.html.fromstring(html.content)

    #gets the products
    #looking for a way to make shorter
    #products = doc.xpath('//div[contains(@class,"sg-row") and contains(@class,"s-result-list")]/div/div/..')
    #CORRECT RIGHT BELOW
    products = doc.xpath('//div[contains(@class,"sg-row") and contains(@class,"s-result-list")]/div[@data-asin!=""]/div/..')

    with open("amazonUrl.xml", mode='wb') as localfile:
         localfile.write(html.content)

    file = open(filename,writeMode)

    for product in products:

        #if name (without the [0].text_content()) is an empty list, check for it
        #before doing anything else
        #fix this because of the spaces
        name = product.xpath('.//span[contains(@class,"a-size-medium") and contains(@class,"a-color-base") and contains(@class, "a-text-normal")]')[0].text_content()
        #name = product.xpath('.//span[contains(@class,"a-size-medium a-color-base a-text-normal")]')[0].text_content()

        price = product.xpath('.//span[contains(@class,"a-offscreen")]')

        #sometimes there wont be a price, therefore the html tag to store
        #the price wont be available
        if len(price) < 1:
            price = "null"
        else:
            price = price[0].text_content()

        print(f'{name}, {price}',file=file)
        print(file=file)

    file.close()

def amazon_scraper_url(url):

    html = session.get(url,timeout=5)
    doc = lxml.html.fromstring(html.content)

    products = doc.xpath('//div[contains(@class,"sg-row") and contains(@class,"s-result-list")]/div[@data-asin!=""]/div/..')

    product_list = []

    for product in products:

        temp = amazon_scraper_item(product)

        product_list.append(temp)

    return product_list

def amazon_scraper_item(lxml):

    name_xpath = './/span[contains(@class,"a-size-medium") and contains(@class,"a-color-base") and contains(@class, "a-text-normal")]'
    price_xpath = './/span[contains(@class,"a-offscreen")]'

    name = lxml.xpath(name_xpath)[0].text_content()
    price = lxml.xpath(price_xpath)


    if len(price) < 1:
        price = "null"
    else:
        price = price[0].text_content()

    item = {}

    item['name'] = name

    item['price'] = price

    return item



#scapper for newEgg using https://www.newegg.com/p/pl?d=ram&N=-1&isNodeId=1&Submit=ENE&DEPA=0&Order=BESTMATCH
#doesnt get the first three items from the first page and does not scraper the first item from every page after
#every scrape includes the first item of the next page as the last item of the current page
#fix above later
#takes a url and a filename (both strings)
#some names may have commas, so we have to replace them

def newEggScaper_file(url,filename,writeMode):

    html = requests.get(url,timeout = 5)
    doc = lxml.html.fromstring(html.content)

    #holds an array of html elements that contains a product
    item_blocks = doc.xpath('.//div[@class="item-container   "]')

    #writes all ram values to a text file
    file = open(filename,writeMode)

    #number the individual products
    position = 1
    for item in item_blocks:
        #add an if statement for missing prices
        #for example https://www.newegg.com/p/pl?Submit=ENE&N=100007709&IsNodeId=1&bop=And&ActiveSearchResult=True&SrchInDesc=ASUS&Page=1&PageSize=36&order=BESTMATCH
        #has a missing price
        file.write(str(position)+". ")
        file.write(item.xpath('.//a[@class="item-title"]')[0].text_content() + ",")
        file.write(item.xpath('.//li[@class="price-current"]')[0].text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0] +"\r\n")
        position = position + 1

    file.close()

def newEggScraper_scraper_url(url):

    html = session.get(url,timeout=5)
    doc = lxml.html.fromstring(html.content)

    #holds an array of html elements that contains a product
    product_blocks = doc.xpath('.//div[@class="item-container   "]')
#
    product_list = []

    for product in product_blocks:


        temp = newEgg_scraper_item(product)

        product_list.append(temp)

    return product_list

def newEgg_scraper_item(lxml):

    name_xpath = './/a[@class="item-title"]'
    price_xpath = './/li[@class="price-current"]'

    name = lxml.xpath(name_xpath)[0].text_content()
    price = lxml.xpath(price_xpath)[0].text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0]

    item = {}

    item['name'] = name

    item['price'] = price

    return item

#scrapes for product information from microcenter
#takes a url(from microcenter), a filename to write to and a writemode for the file
#some names may have commas, so we gotta take that into account
#some names (ram for example) have extra words attached to the name, we we gotta take those out
def microCenterScaper_file(url,filename,writeMode):


    #html = requests.get(url,timeout = 5,headers=headers)
    html = session.get(url,timeout=5)
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

#scrapes a whole page off of microcenter and returns a dictionary
#containing the products and prices(possibly more)
def microCenter_scraper_url(url):

    html = session.get(url,timeout=5)
    doc = lxml.html.fromstring(html.content)

    #holds a list of html objects
    product_blocks = doc.xpath('.//li[@class="product_wrapper"]')

    with open("microCenter_contents.xml", mode='wb') as localfile:
         localfile.write(html.content)

    list_of_products = []

    #goes through a list of html objects
    #and creates a dictionary and adds it to list_of_products
    for product in product_blocks:

        temp = microCenter_scraper_item(product)
        list_of_products.append(temp)

    return list_of_products

#lxml must already be a product container
def microCenter_scraper_item(lxml):

    xpath_exp = './/a[@data-name]'

    attribs = lxml.xpath(xpath_exp)[0].attrib

    item = {}

    item['name'] = f'{attribs["data-brand"]} {attribs["data-name"]}'

    item['price'] = f'{attribs["data-price"]}'

    return item

if __name__ == "__main__":
    print("hello")

    newEggRamUrl = "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611"
    newEggGraphicsUrl = "https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48/Page-1?Tid=7709"
    url = "https://www.newegg.com/p/pl?Submit=ENE&N=100007709&IsNodeId=1&bop=And&ActiveSearchResult=True&SrchInDesc=ASUS&Page=1&PageSize=36&order=BESTMATCH"
    #newEggScaper(newEggGraphicsUrl,"graphicsCards.txt","w")
    microCenterRamUrl = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=true"
    microCenterGraphicsUrl = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966937&myStore=false"
    #microCenterScaper_file(microCenterRamUrl,"microRam.txt","w+")
    url = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=true"
    #stuff = microCenter_scraper_url(url)
    #stuff = newEggScraper_scraper_url(newEggRamUrl)
    amazonRamUrl= "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1"
    stuff = amazon_scraper_url(amazonRamUrl)
    for item in stuff:
        print(item)
        print()


    #amazonScraper(amazonRamUrl,"amazonRam.txt","w")
    #a = newEggPageScraper("zam.txt",2)
    #price.text_content().replace('\r\n',' ').replace('\t', ' ').replace('|', ' ').split()[0]
