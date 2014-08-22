#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
from zenlog import log

SOURCE_FILE = "banks.json"

def download_page(url):
    response = urllib2.urlopen(url)
    html = response.read()
    return html

f = open(SOURCE_FILE, 'r')
contents = f.read()
jsondata = json.loads(contents)
for item in jsondata:
    # extrair o URL e o código/ID a partir do JSON
    url = item['url']
    cod = url.split('=')[-1]
    # sacar o conteúdo da página
    html = download_page(url)

    # gravar num ficheiro html
    filename = cod + ".html"
    outfile = open(filename, 'w')
    outfile.write(html)
    outfile.close()
    log.debug(u'Já saquei o ' + cod + " :D")
    
