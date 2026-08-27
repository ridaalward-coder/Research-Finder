import os,re,requests,html
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def clean(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x or ''))).strip()

def adzuna(q):
    aid,key=os.getenv('ADZUNA_APP_ID'),os.getenv('ADZUNA_APP_KEY')
    if not aid or not key: return []
    u='https://api.adzuna.com/v1/api/jobs/us/search/1'
    r=requests.get(u,params={'app_id':aid,'app_key':key,'what':q,'results_per_page':50,'content-type':'application/json','sort_by':'date'},timeout=30); r.raise_for_status()
    out=[]
    for x in r.json().get('results',[]):
        out.append({'external_id':'adzuna:'+str(x.get('id')),'kind':'job','title':x.get('title',''),'organization':(x.get('company') or {}).get('display_name',''),'location':(x.get('location') or {}).get('display_name',''),'url':x.get('redirect_url',''),'description':clean(x.get('description','')),'source':'Adzuna','deadline':'','raw':str(x)})
    return out

def ddg(q):
    u='https://html.duckduckgo.com/html/?q='+quote_plus(q)
    r=requests.get(u,headers={'User-Agent':'Mozilla/5.0 (compatible; ResearchHunter/1.0)'},timeout=30); r.raise_for_status()
    s=BeautifulSoup(r.text,'html.parser'); out=[]
    for a in s.select('.result')[:8]:
        link=a.select_one('.result__a'); sn=a.select_one('.result__snippet')
        if link:
            href=link.get('href',''); title=link.get_text(' ',strip=True); desc=sn.get_text(' ',strip=True) if sn else ''
            out.append({'external_id':'web:'+href,'kind':'web','title':title,'organization':'','location':'','url':href,'description':desc,'source':'DuckDuckGo','deadline':'','raw':''})
    return out

def brave(q):
    key=os.getenv('BRAVE_SEARCH_API_KEY')
    if not key: return []
    r=requests.get('https://api.search.brave.com/res/v1/web/search',params={'q':q,'count':8},headers={'X-Subscription-Token':key,'Accept':'application/json'},timeout=30); r.raise_for_status()
    return [{'external_id':'web:'+x['url'],'kind':'web','title':x.get('title',''),'organization':'','location':'','url':x['url'],'description':x.get('description',''),'source':'Brave','deadline':'','raw':str(x)} for x in r.json().get('web',{}).get('results',[])]

def web(q):
    try:
        r=brave(q)
        return r or ddg(q)
    except Exception:
        return ddg(q)
