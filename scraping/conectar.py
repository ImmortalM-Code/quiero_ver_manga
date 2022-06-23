# Codigo extraido de repositorio de BastianRC  --- https://github.com/BastianRC/download-manga-tumangaonline
import re
import time
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import urllib.request


req = urllib.request
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8'}
            #'Connection': 'keep-alive'}


def ChargeWeb(url):
	
    try:
        source_code = req.Request(url, headers=hdr)

        plain_text = req.urlopen(source_code).read()
        soup = BeautifulSoup(plain_text, features="lxml")
        time.sleep(1)
    except HTTPError as ex:
        print(f"Error {ex} - {repr(ex)}")
        time.sleep(1)
    return soup