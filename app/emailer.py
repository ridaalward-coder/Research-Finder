import os,requests

def send(subject,html):
    key=os.getenv('RESEND_API_KEY'); sender=os.getenv('RESEND_FROM'); to=os.getenv('ALERT_EMAIL')
    if not (key and sender and to): return False
    r=requests.post('https://api.resend.com/emails',headers={'Authorization':'Bearer '+key},json={'from':sender,'to':[to],'subject':subject,'html':html},timeout=30); r.raise_for_status(); return True
