#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from zenlog import log

#adicionar a primeira linha com os headers do CSV

headers = [ 'institution_name',
            'id',
            'url',
            'institution_code_number',
            'institution_type',
            'beginning_of_activity',
            'state',
            'address',
            'post_code',
            'place',
            'headquarters_name',
            'headquarters_address',
            'post_code',
            'city',
            'country',
            'subscribed_capital',
            'paid_up_capital',
            'related_decisions',
            'published_accounts',
          ]

#abrir o ficheiro JSON (temos agora uma lista de dicionários)

SOURCE_FILE = "banks-info.json"
f = open(SOURCE_FILE, 'r')
contents = f.read()
jsondata = json.loads(contents)

FATHER_SOURCE_FILE = "banks.json"
f = open(FATHER_SOURCE_FILE, 'r')
contents = f.read()
fatherjsondata = json.loads(contents)

#criar uma lista vazia para armazenarmos as linhas do CSV

rows = []

headerline = ",".join(headers)
rows.append(headerline)

for item in jsondata:
    values = []
    for header in headers:
        if not item.has_key(header):
            if header == "institution_name":
                # abre o banks.json
                name = ""
                for f_item in fatherjsondata:
                    if f_item['url'] == item['url'].replace("https", "http"):
                        name = f_item['name'].replace('"', "'")
                        values.append('"%s"' % name)
                        break
                if not name:
                    log.error("Não encontrei o nome ;(")
                continue
            elif header == "institution_type":
                # abre o banks.json
                bank_type = ""
                for f_item in fatherjsondata:
                    if f_item['url'] == item['url'].replace("https", "http"):
                        bank_type = f_item['type'].replace('"', "'")
                        values.append('"%s"' % bank_type)
                        break
                if not bank_type:
                    log.error("Não encontrei o tipo ;(")
                continue
            else:
                value = ""
                values.append(value)
                continue    
        if header in ['id', 'institution_code_number', 'beginning_of_activity',
                      'subscribed_capital', 'paid_up_capital']:
            value = item[header]
        else:
            # remover aspas
            value = item[header].replace('"', "'")
            # e agora colocar
            value = '"' + value + '"'
        
        if header in ['subscribed_capital', 'paid_up_capital']:
            value = value.replace("(Euro)", "")
            value = value.replace(",", "")
            
        values.append(value)
    s = ",".join(values)
    rows.append(s)
    

import codecs
csvfile = codecs.open("out.csv", "w", "utf-8")
output = "\n".join(rows)
csvfile.write(output)
csvfile.close()
        



'''para cada dicionário na lista de dicionários
    construir um string separado por vírgulas, adicionando cada campo por ordem,
    com aspas nos strings internos  e juntá-lo à lista de strings 
      s += item['id'] + ","
      s += '"' + item['id'] + '",'
      Melhor:
      s += '%
      s,' % item['id']
      s += '"%s",' % item['id']
'''

#pegar na lista de strings e gravá-la num ficheiro .csv



