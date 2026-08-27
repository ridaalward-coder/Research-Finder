import os,json,re
from openai import OpenAI
from pathlib import Path
PROFILE=json.loads(Path('profile.json').read_text())
SYSTEM='''You are Rida's conservative research-opportunity analyst. Evaluate U.S. Summer 2027 undergraduate research programs, internships, faculty/lab opportunities and related postings. Rida is a sophomore mechanical engineering student at Vanderbilt and an international student studying in the U.S. Primary interests: medical/surgical/miniature/soft robotics and microrobotics. Secondary: medical devices, mechatronics, electromechanical systems, microfabrication, microelectronics, MEMS, flexible electronics, sensors/actuators, nanotechnology. Computational: image analysis, computer vision, signal processing, Fourier analysis, biomedical imaging, acoustic/sound analysis. His Dong Lab experience can be considered relevant to miniature robotics, micro-scale fabrication, soldering/electronics, fabrication and analysis of miniature electronic parts/chips, electromechanical systems, magnetic actuation and experimental prototyping, but never invent a specific task. Never assume citizenship, sponsorship, clearance or work authorization. If unclear, label eligibility uncertain. REU programs often have citizenship/residency restrictions; inspect the actual posting when possible. Search should not be Vanderbilt-only; nationwide U.S. universities are the target.'''

def client(): return OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def analyze(o):
    prompt=f'''CANDIDATE PROFILE:\n{json.dumps(PROFILE,indent=2)}\n\nOPPORTUNITY:\n{json.dumps(o,indent=2)}\n\nReturn ONLY JSON with exactly these keys: technical_fit, eligibility, realistic_getability, career_value, interest_alignment, overall_score, eligibility_label, recommendation, why_fit, concerns, actions, cold_email_score, cold_email_recommendation, professors. Scores 0-100. recommendation must be one of HIGH PRIORITY, APPLY, REACH, MONITOR, DO NOT APPLY. eligibility_label must be ELIGIBLE, LIKELY ELIGIBLE, UNCERTAIN, or INELIGIBLE. cold_email_recommendation must be STRONGLY RECOMMENDED, POTENTIALLY USEFUL, or NOT USEFUL. professors is an array of objects with name, reason, and suggested_contact_action only if the source text identifies a professor; otherwise empty. Overall should reflect the weighted values and should be 0 if eligibility is clearly ineligible. Assess how realistic it is for a sophomore to get the position, not how prestigious it is. Explain why a cold email would or would not help based on program structure; do not invent a policy.'''
    r=client().responses.create(model=os.getenv('OPENAI_MODEL','gpt-5.6-luna'),input=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}],max_output_tokens=1800)
    return json.loads(re.sub(r'^```json\s*|\s*```$','',r.output_text.strip()))

def extract_professors(page_text, source_url, university_hint=''):
    prompt=f'''CANDIDATE: {json.dumps(PROFILE)}\nUNIVERSITY HINT: {university_hint}\nSOURCE URL: {source_url}\nPAGE TEXT: {page_text[:10000]}\n\nExtract up to 5 actual professors/faculty/lab leaders explicitly identifiable from this page whose research could relate to the candidate. Return ONLY a JSON array. Each item must have name, department, lab, url, email, research. If no actual professor is identifiable, return []. Never invent a person or email.'''
    r=client().responses.create(model=os.getenv('OPENAI_MODEL','gpt-5.6-luna'),input=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}],max_output_tokens=1200)
    return json.loads(re.sub(r'^```json\s*|\s*```$','',r.output_text.strip()))

def professor_match(prof):
    prompt=f'''CANDIDATE:\n{json.dumps(PROFILE)}\n\nPROFESSOR/LAB:\n{json.dumps(prof)}\n\nReturn JSON: match_score (0-100), cold_email_score (0-100), cold_email_recommendation (STRONGLY RECOMMENDED/POTENTIALLY USEFUL/NOT USEFUL), why_match (3-5 concrete points). Never invent research.'''
    r=client().responses.create(model=os.getenv('OPENAI_MODEL','gpt-5.6-luna'),input=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}],max_output_tokens=700)
    return json.loads(re.sub(r'^```json\s*|\s*```$','',r.output_text.strip()))
