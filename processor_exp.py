from multiprocessing import Pool
import requests
import lxml.html
import configparser
import time


session = requests.Session()
session.headers.update({"User-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"})

class connector(object,url):

    html = session.get(url,timeout=5)
    doc = lxml.html.fromstring(html.content)

    def __reduce__(self):
        return (doc, (self.progress_int,))



if __name__ == '__main__':


    urls = [connector("https://www.amazon.com/s?k=ram&i=electronics&qid=1559337571&ref=sr_pg_1"),connector("https://www.newegg.com/Desktop-Memory/SubCategory/ID-147/Page-1?Tid=7611"),
        connector("https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966965&myStore=true")]

    pizza = '''
    t1 = time.time()
    answers = []
    for url in urls:
        answers.append(connector(url))
    print(time.time()-t1)'''

#    pizza = '''
    t1 = time.time()
    p = Pool(5)
    p.map(connector,urls)
    print(time.time()-t1)
