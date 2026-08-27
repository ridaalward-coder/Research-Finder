from .db import con,settings
from .emailer import send

def notify():
    s=settings(); threshold=float(s.get('email_threshold','85')); c=con()
    rows=c.execute('select * from opportunities where overall_score>=? and email_sent=0 order by overall_score desc',(threshold,)).fetchall()
    for j in rows:
        html=f'''<h2>🔥 {j["overall_score"]:.0f}% — {j["title"]}</h2><p><b>{j["organization"]}</b> · {j["location"]}</p><p><b>{j["eligibility_label"]}</b> · {j["recommendation"]} · cold email: {j["cold_email_recommendation"]}</p><p>{j["why_fit"]}</p><p><a href="{j["url"]}">Open opportunity</a></p>'''
        try:
            if send(f'🔥 {j["overall_score"]:.0f}% research opportunity: {j["title"]}',html): c.execute('update opportunities set email_sent=1 where id=?',(j['id'],))
        except Exception as e: print('email',e)
    c.commit()
