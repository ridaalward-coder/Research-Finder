import sqlite3, json
from pathlib import Path
DB=Path('data/hunter.db')

def con():
    DB.parent.mkdir(exist_ok=True)
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    c.executescript('''
    CREATE TABLE IF NOT EXISTS opportunities(
      id INTEGER PRIMARY KEY, external_id TEXT UNIQUE, kind TEXT, title TEXT, organization TEXT,
      department TEXT, location TEXT, url TEXT, description TEXT, source TEXT, discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
      deadline TEXT, status TEXT DEFAULT 'new', technical_fit REAL, eligibility REAL, realistic_getability REAL,
      career_value REAL, interest_alignment REAL, overall_score REAL, eligibility_label TEXT, recommendation TEXT,
      why_fit TEXT, concerns TEXT, actions TEXT, cold_email_score REAL, cold_email_recommendation TEXT,
      professors TEXT, raw TEXT, email_sent INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS professors(
      id INTEGER PRIMARY KEY, external_id TEXT UNIQUE, name TEXT, university TEXT, department TEXT,
      lab TEXT, url TEXT, email TEXT, research TEXT, match_score REAL, cold_email_score REAL,
      cold_email_recommendation TEXT, why_match TEXT, source_url TEXT, raw TEXT
    );
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
    ''')
    for k,v in {'email_threshold':'85','cold_email_threshold':'82','max_ai_analyses_per_run':'15'}.items():
        c.execute('INSERT OR IGNORE INTO settings VALUES(?,?)',(k,v))
    c.commit(); return c

def settings():
    return {r['key']:r['value'] for r in con().execute('select * from settings')}

def set_setting(k,v):
    c=con(); c.execute('insert into settings values(?,?) on conflict(key) do update set value=excluded.value',(k,str(v))); c.commit()

def upsert(o):
    c=con(); c.execute('''INSERT INTO opportunities(external_id,kind,title,organization,department,location,url,description,source,deadline,raw)
      VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(external_id) DO UPDATE SET title=excluded.title,description=excluded.description,url=excluded.url,deadline=excluded.deadline''',
      tuple(o.get(k,'') for k in ['external_id','kind','title','organization','department','location','url','description','source','deadline','raw'])); c.commit()

def pending(n): return [dict(r) for r in con().execute('select * from opportunities where overall_score is null order by discovered_at desc limit ?', (n,))]
def update_analysis(i,a):
    c=con(); c.execute('''update opportunities set technical_fit=?,eligibility=?,realistic_getability=?,career_value=?,interest_alignment=?,overall_score=?,eligibility_label=?,recommendation=?,why_fit=?,concerns=?,actions=?,cold_email_score=?,cold_email_recommendation=?,professors=? where id=?''',
      (a['technical_fit'],a['eligibility'],a['realistic_getability'],a['career_value'],a['interest_alignment'],a['overall_score'],a['eligibility_label'],a['recommendation'],json.dumps(a['why_fit']),json.dumps(a['concerns']),json.dumps(a['actions']),a['cold_email_score'],a['cold_email_recommendation'],json.dumps(a.get('professors',[])),i)); c.commit()
def all_opps(n=300): return [dict(r) for r in con().execute('select * from opportunities order by coalesce(overall_score,0) desc, discovered_at desc limit ?', (n,))]
def upsert_prof(p):
    c=con(); c.execute('''insert into professors(external_id,name,university,department,lab,url,email,research,match_score,cold_email_score,cold_email_recommendation,why_match,source_url,raw)
      values(?,?,?,?,?,?,?,?,?,?,?,?,?,?) on conflict(external_id) do update set match_score=excluded.match_score,cold_email_score=excluded.cold_email_score''',
      tuple(p.get(k,'') for k in ['external_id','name','university','department','lab','url','email','research','match_score','cold_email_score','cold_email_recommendation','why_match','source_url','raw'])); c.commit()
def professors(n=200): return [dict(r) for r in con().execute('select * from professors order by coalesce(match_score,0) desc limit ?', (n,))]
