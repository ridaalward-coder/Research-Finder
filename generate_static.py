import sqlite3,html
from pathlib import Path
DB=Path('data/hunter.db'); OUT=Path('docs/index.html')
if not DB.exists(): OUT.write_text('<h1>Rida Research Hunter</h1><p>No scan yet.</p>'); raise SystemExit
c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
opps=[dict(x) for x in c.execute('select * from opportunities order by coalesce(overall_score,0) desc, discovered_at desc limit 250')]
profs=[dict(x) for x in c.execute('select * from professors order by coalesce(match_score,0) desc limit 100')]
def e(x): return html.escape(str(x or ''))
cs=[]
for o in opps:
 s=o['overall_score'] or 0; cls='high' if s>=85 else 'good' if s>=75 else 'reach'
 cs.append(f'<article class="card {cls}"><div class="score">{s:.0f}% — {e(o["title"])}</div><h3>{e(o["organization"])}</h3><div class="muted">{e(o["location"])} · {e(o["source"])} · {e(o["kind"])}</div><p><span class="tag">Eligibility: {e(o["eligibility_label"])}</span><span class="tag">Technical: {(o["technical_fit"] or 0):.0f}%</span><span class="tag">Getability: {(o["realistic_getability"] or 0):.0f}%</span><span class="tag">Cold email: {e(o["cold_email_recommendation"])}</span></p><p><b>{e(o["recommendation"] or "Awaiting analysis")}</b></p><a class="btn" href="{e(o["url"])}" target="_blank">Open opportunity</a></article>')
ps=[]
for p in profs:
 ps.append(f'<article class="card"><div class="score">{(p["match_score"] or 0):.0f}% research match</div><h3>{e(p["name"])}</h3><div class="muted">{e(p["university"])} · {e(p["department"])} · {e(p["lab"])}</div><p><span class="tag">Cold email: {(p["cold_email_score"] or 0):.0f}%</span> {e(p["cold_email_recommendation"])}</p><p>{e(p["why_match"])}</p><a class="btn" href="{e(p["url"] or p["source_url"])}" target="_blank">View faculty/lab page</a></article>')
html_doc=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="600"><title>Rida Research Hunter</title><style>body{{font-family:system-ui;max-width:1200px;margin:auto;padding:24px;background:#f6f7fb;color:#17202a}}.card{{background:#fff;border:1px solid #e1e5ea;border-radius:14px;padding:18px;margin:14px 0}}.high{{border-left:6px solid #16834b}}.good{{border-left:6px solid #3278d9}}.reach{{border-left:6px solid #e29b19}}.score{{font-size:26px;font-weight:800}}.muted{{color:#66727e}}.tag{{display:inline-block;background:#eef1f5;border-radius:999px;padding:4px 8px;margin:3px}}.btn{{display:inline-block;background:#17202a;color:#fff;padding:9px 12px;border-radius:8px;text-decoration:none}}</style></head><body><h1>Rida Research Hunter</h1><p>Summer 2027 · U.S. nationwide · research programs, internships and PI/lab matches. Refresh the page after each scheduled scan.</p><h2>Opportunities</h2>{''.join(cs)}<h2>Professor / Lab targets</h2>{''.join(ps)}</body></html>'''
OUT.write_text(html_doc,encoding='utf-8')
