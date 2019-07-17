def smicroCenterScaper(url, filename=None, writeMode='w'):
    res = requests.get(url, timeout=5)
    doc = lxml.html.fromstring(res.content)
    items = []

    for item in doc.xpath('//*[contains(@class,"product_wrapper")]'):
        tmp = {} # temp item object

        # list of attributes about this item (micro center is good about this)
        attribs = item.xpath('.//a/@data-name/..')[0].attrib

        # save any "data" attribute to our tmp item
        for key,value in attribs.iteritems():
            if key[:4] == 'data':
                tmp[key[5:]] = value

        # add temp item to list of items
        items.append(tmp)

    if filename:
        with open(filename, writeMode) as f:
            for pos, item in enumerate(items, 1):
                print(f'{pos:04}. {item["name"]} ({item["price"]})', file=f)

  # in case they get processed downstream (I assume they will be eventually)
    return items
