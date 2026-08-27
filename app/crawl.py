import requests,re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch(url):
    r=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; ResearchHunter/1.0)'},timeout=20); r.raise_for_status(); return r.text

def extract(url):
    try:
        s=BeautifulSoup(fetch(url),'html.parser')
        for x in s(['script','style','noscript']): x.decompose()
        text=re.sub(r'\s+',' ',s.get_text(' ',strip=True))[:12000]
        links=[]
        for a in s.find_all('a',href=True):
            t=a.get_text(' ',strip=True).lower(); h=urljoin(url,a['href'])
            if any(k in t for k in ['faculty','professor','lab','research','people','team']): links.append((t,h))
        return text,links[:40]
    except Exception as e: return '',[]
