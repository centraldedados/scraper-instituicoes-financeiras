#!/usr/bin/env python
# -*- coding: utf-8 -*-

import selenium
from selenium import webdriver
import selenium.webdriver.support.ui as UI
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC 
import contextlib
from zenlog import log
import json

from pprint import pprint

#driver = webdriver.PhantomJS()
driver = webdriver.Firefox()
driver.get("http://www.bportugal.pt/en-US/Supervisao/Pages/Instituicoesautorizadas.aspx")

# Get the institutions listed in the table, one per row
# click the number to go to the next page -- .MudarPagina strong + a
# every 10 pages click in the > arrow to advance -- .MudarPagina strong + span > a

bank_list = []

pagecount = 1
while True:
    log.debug("Novo loop, pagecount eh " + str(pagecount))
    wait = UI.WebDriverWait(driver, 10)
    
    links = driver.find_elements_by_css_selector(".AreaResultados td a")
    log.debug("Encontrei %d links..." % len(links))
    if len(links) == 0:
        from time import sleep
        sleep(3)
        links = driver.find_elements_by_css_selector(".AreaResultados td a")
        if len(links) == 0:
            log.error("Não há links, snif")
        else:
            log.debug("Iupi, %d links!" % len(links))
    rows = driver.find_elements_by_css_selector(".AreaResultados tbody tr")
    
    # skip first row
    first = True
    for row in rows:
        if first:
            first = False
            continue
        bank_name = row.find_element_by_css_selector("a")
        bank_type = row.find_element_by_css_selector("span")
        bank = { "name": bank_name.text, 
                 "url": bank_name.get_attribute("href"),
                 "type": bank_type.text
               }
        log.debug("Banco: " + bank['name'] + ", " + bank['type'])
        bank_list.append(bank)

    if pagecount % 10:
        # não é múltiplo de 10
        log.debug("À espera que o link fique clicável...")
        try:
            next_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.MudarPagina strong + a')))
        except selenium.common.exceptions.TimeoutException:
            break

        log.debug("Click click <3")
        next_link.click() 
    else:
        log.debug("Chegamos a " + str(pagecount) + ", à espera que fique clicável...")
        try:
            next_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.MudarPagina strong + span > a')))
        except selenium.common.exceptions.TimeoutException:
            break
        log.debug("Click click <3")
        next_link.click() 
    pagecount += 1

f = open("banks.json", "w")
jsondata = json.dumps(bank_list)
f.write(jsondata)
f.close()

driver.quit
