#!/usr/bin/env python
# -*- coding: utf-8 -*-

# description .tabelaSimples tr th
# value .tabelaSimples tr td

from BeautifulSoup import BeautifulSoup
from pprint import pprint
from zenlog import log
import json

HTML_DIR = "bank-details/"
OUTFILE = "banks-info.json"

def parse_file(f):
    bank = {}

    html = open(f, 'r').read()
    soup = BeautifulSoup(html)
    items_headings = soup.findAll("th")
    items = soup.findAll("td")
    item_pairs = zip(items_headings, items)

    # encontrar duplicados
    country_needs_fixing = False
    urls_need_fixing = False
    dups = set([x.text for x in items_headings if items_headings.count(x) > 1])
    if dups:
        if "Country" in dups:
            country_needs_fixing = True
        elif "Related decisions" in dups and "Published accounts" in dups:
            pass
        else:
            log.error("Campo duplicado:")
            for d in dups:
                print '        ' + d

    for name, value in item_pairs:
        name = name.text.lower().replace(' ', '_').replace('-', '_')
        if country_needs_fixing and name == "country":
            country_needs_fixing = False
            name = "city"
        if value.find("a"):
            bank[name] = value.find('a')['href']
        else:
            bank[name] = value.text

    bank_filename = f.split('/')[-1]
    bank_id = bank_filename.split('.')[0]
    bank_url = 'https://www.bportugal.pt/en-US/Supervisao/Pages/CreditInstitution.aspx?IcID=' + bank_id
    bank['id'] = bank_id
    bank['url'] = bank_url

    return bank

banks = []

import glob
files = glob.glob(HTML_DIR + "*.html")
for f in files:
    bank = parse_file(f)
    banks.append(bank)

out = open(OUTFILE, 'w')
out.write(json.dumps(banks))
out.close()
