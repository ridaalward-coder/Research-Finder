from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from .db import all_opps,professors,settings,set_setting
import subprocess,sys
app=FastAPI(title='Rida Research Hunter'); templates=Jinja2Templates(directory='templates')
@app.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse('index.html',{'request':request,'opps':all_opps(),'profs':professors(),'settings':settings()})
@app.post('/refresh')
def refresh(): subprocess.Popen([sys.executable,'-m','app.pipeline']); return RedirectResponse('/',303)
@app.post('/settings')
async def save(request:Request):
    f=await request.form()
    for k in ['email_threshold','cold_email_threshold','max_ai_analyses_per_run']:
        if k in f:set_setting(k,f[k])
    return RedirectResponse('/',303)
