# Codigo sacado del repositorio de BastianRC  --- https://github.com/BastianRC/download-manga-tumangaonline
from bs4 import BeautifulSoup
import urllib.request


req = urllib.request
hdr = {}


def ChargeWeb(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://cssspritegenerator.com',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
		
    source_code = req.Request(url, headers=hdr)

    plain_text = req.urlopen(source_code, timeout=20).read()
    soup = BeautifulSoup(plain_text, features="lxml")
        
    return soup