#!/usr/bin/env python3
"""Lightweight no-dependency structural checker; not a browser QA replacement."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
SITE=ROOT/'site'
errors=[]
class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.links=[];self.h1=0;self.main=0;self.article=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if t=='main':self.main+=1
  if t=='article':self.article+=1
  if t in ('a','link','script','img'):
   u=d.get('href') or d.get('src')
   if u:self.links.append(u)
for f in SITE.rglob('*.html'):
 text=f.read_text(encoding='utf-8');p=Page();p.feed(text)
 # redirects are exempt from article semantics
 is_redirect='http-equiv="refresh"' in text
 is_legacy=(f.parent==SITE/'chapters' and f.stem.isdigit() and int(f.stem)>3)
 if not is_redirect and not is_legacy and f.name!='index.html' and (p.h1!=1 or p.article!=1 or p.main!=1): errors.append(f'{f}: semantic landmark mismatch')
 if not is_redirect and f.name=='index.html' and f.parent==SITE and p.h1!=1:errors.append('home: missing unique H1')
 for u in p.links:
  if re.match(r'^(https?:|mailto:|tel:|data:|#|javascript:)',u):continue
  target=(f.parent/u.split('#')[0].split('?')[0]).resolve()
  if not target.is_relative_to(SITE.resolve()):errors.append(f'{f}: escapes site: {u}')
  elif not target.exists():errors.append(f'{f}: missing {u}')
for f in (SITE/'assets/figures').glob('*.svg'):
 try:
  root=ET.parse(f).getroot();names={x.tag.split('}')[-1] for x in root.iter()}
  if 'viewBox' not in root.attrib or 'title' not in names or 'desc' not in names:errors.append(f'{f}: SVG lacks viewBox/title/desc')
 except ET.ParseError as e:errors.append(f'{f}: invalid XML {e}')
for n in range(1,29):
 if not (SITE/'chapters'/f'{n:02}.html').exists():errors.append(f'chapter {n:02} missing')
 if not (SITE/f'{n:02}.html').exists():errors.append(f'compat {n:02} missing')
for n in range(1,4):
 if not (ROOT/'content/evidence'/f'{n:02}.json').exists():errors.append(f'evidence {n:02} missing')
print('Static site verification:', 'PASS' if not errors else 'FAIL')
print('HTML:',len(list(SITE.rglob('*.html'))),'SVG:',len(list((SITE/'assets/figures').glob('*.svg'))),'issues:',len(errors))
for e in errors[:80]:print(' -',e)
sys.exit(bool(errors))
