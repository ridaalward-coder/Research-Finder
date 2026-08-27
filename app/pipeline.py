import os,json,re
from dotenv import load_dotenv
from .db import upsert,pending,update_analysis,settings,upsert_prof
from .search import adzuna,web
from .ai import analyze,professor_match,extract_professors
from .crawl import extract
load_dotenv()
ROOT=os.path.dirname(os.path.dirname(__file__))
CFG=json.load(open(os.path.join(ROOT,'config.json')))

def collect():
    seen=0
    for q in CFG['search']['job_queries']:
        try:
            for x in adzuna(q):
                text=(x['title']+' '+x['description']).lower()
                if any(k in text for k in ['intern','undergraduate','research','summer','co-op','student']): upsert(x); seen+=1
        except Exception as e: print('adzuna',e)
    for q in CFG['search']['university_queries']:
        try:
            for x in web(q): upsert(x); seen+=1
        except Exception as e: print('web',e)
    return seen

def analyze_pending():
    n=int(settings().get('max_ai_analyses_per_run','15')); out=[]
    for o in pending(n):
        try:
            a=analyze(o); update_analysis(o['id'],a); out.append((o,a))
        except Exception as e: print('analysis',e)
    return out

def discover_professors():
    from .db import all_opps
    count=0; seen_urls=set(); calls=0
    for o in all_opps(30):
        if not o.get('overall_score') or o['overall_score'] < 78: continue
        q=f"{o.get('organization','')} faculty professor lab {o.get('title','')} robotics medical soft microrobotics MEMS biomedical imaging"
        try:
            for r in web(q)[:3]:
                if r['url'] in seen_urls: continue
                seen_urls.add(r['url']); text,links=extract(r['url'])
                if len(text)<500: continue
                calls+=1
                for p in extract_professors(text,r['url'],o.get('organization','')):
                    p['external_id']='prof:'+p.get('name','')+':'+p.get('url','')
                    p['university']=p.get('university') or o.get('organization','')
                    try:
                        a=professor_match(p); p.update(a); p['raw']=text[:3000]; p['source_url']=r['url']; upsert_prof(p); count+=1
                    except Exception as e: print('prof match',e)
                if calls>=6: return count
        except Exception as e: print('prof web',e)
    return count

def run():
    print('Collected',collect()); an=analyze_pending(); print('Analyzed',len(an)); print('Professor candidates',discover_professors());
    try:
        from .notify import notify; notify()
    except Exception as e: print('notify',e)
if __name__=='__main__': run()
