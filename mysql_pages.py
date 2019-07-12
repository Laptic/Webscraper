import page_parser
import mysql.connector as mysql
import configparser

config_file = "config_file.txt"
config = configparser.ConfigParser()
# reads in all vars from config file
config.read(config_file)

PASSWORD = config.get('passwords', 'mysqlPassword')


def connect():
    db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = PASSWORD,
    database = "pc_parts"
    )

    return db


def newEggInput(egg_items, db, insertQuery, idNum):
    #make ram_parts
    #query = "INSERT INTO ram_parts (name,price,website,id) VALUES (%s,%s,%s,%s)"
    cursor = db.cursor()

    newEggTuples = []

    for item in egg_items:

        itemPrice = item['price'][1:]
        itemPrice = float(itemPrice)

        newEggValue = (str(item['name']),itemPrice,'newEgg',idNum)
        newEggTuples.append(newEggValue)
        idNum = idNum + 1

    cursor.executemany(insertQuery,newEggTuples)
    db.commit()


def microcenterInput(micro_items, db, insertQuery, idNum):

    cursor = db.cursor()

    microcenterTuples = []

    for item in micro_items:

        itemPrice = item['price'][1:]
        itemPrice = float(itemPrice)

        microcenterValue = (str(item['name']),itemPrice,'Microcenter',idNum)
        microcenterTuples.append(microcenterValue)
        idNum = idNum + 1

    cursor.executemany(insertQuery,microcenterTuples)
    db.commit()


def amazonInput(amazon_items, db, insertQuery, idNum):

    cursor = db.cursor()

    amazonTuples = []

    for item in amazon_items:

        #syntax error for some reason
        if item['price'] == 'null':
            itemPrice = 0.00
        else:
            itemPrice = item['price'][1:]
            itemPrice = float(itemPrice)

        amazonValue = (str(item['name']),itemPrice,'Amazon',idNum)

        amazonTuples.append(amazonValue)
        idNum = idNum + 1

    cursor.executemany(insertQuery,amazonTuples)
    db.commit()

# if __name__ == "__main__":
#     print("hello")
#
#     db = connect()
#
#     idNum = 25
#     query = "INSERT INTO ram_parts (name,price,website,id) VALUES (%s,%s,%s,%s)"
#     ramNewEggWebsite = "https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611"
#     ramMicrocenterWebsite = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=true"
#     ramAmazonWebsite = "https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1"
#     #newEggInput(db,ramNewEggWebsite,query,idNum)
#     amazonInput(db,ramAmazonWebsite,query,idNum)
#
#
#
#
#     pizza = '''
#     cursor = db.cursor()
#
#     NUM_PAGES = 1
#
#     newEggRamUrl = f"https://www.newegg.com/p/pl?Submit=StoreIM&Depa={NUM_PAGES}&Category=34"
#     print(newEggRamUrl)
#
#     newEggItems = page_parser.newEggScraper_scraper_url(newEggRamUrl)
#
#
#     num = 1;
#     newEggTuples = []
#     for item in newEggItems:
#
#         itemPrice = item['price'][1:]
#         itemPrice = float(itemPrice)
#
#         newEggValue = (str(item['name']),itemPrice,'newEgg',num)
#         newEggTuples.append(newEggValue)
#         num = num + 1
#
#     query = "INSERT INTO all_parts (name,price,website,id) VALUES (%s,%s,%s,%s)"
#
#     print(newEggTuples)
#     cursor.executemany(query,newEggTuples)
#     db.commit()
#
#
#
#     num = "$10.99"
#     num = num[1:]
#     num = float(num)
#
#
#     query = "INSERT INTO all_parts (name,price,website,id) values (%s,%s,%s,%s)"
#
#     values = ('gtx 270',num,'microcenter',2)
#
#     cursor.execute(query,values)
#     db.commit()
#
#
#     query = "select * from pet"
#     query2 = "insert into pet (name,owner,age,id) values (%s,%s,%s,%s)"
#     values = ('moe','mami',2,8)
#     cursor.execute(query2,values)
#     db.commit()
#
#     cursor.execute(query)
#     print(cursor.fetchall())
#     print(cursor.rowcount,"record inserted")
#     '''
