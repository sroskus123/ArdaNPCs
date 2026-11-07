"""Check generated navigation, fragments, search entries and public file hygiene."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re

ROOT=Path(__file__).resolve().parent
class Document(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=True); self.ids=set(); self.links=[]; self.headings=0; self.lang=None; self.duplicates=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='html': self.lang=a.get('lang')
  if tag=='h1': self.headings+=1
  if a.get('id'):
   if a['id'] in self.ids: self.duplicates.append(a['id'])
   self.ids.add(a['id'])
  for name in ['href','src']:
   if name in a: self.links.append(a[name])
docs={}
for p in [*ROOT.glob('*.html'),*ROOT.glob('cs/*.html'),*ROOT.glob('en/*.html')]:
 d=Document(); d.feed(p.read_text(encoding='utf-8')); docs[p.resolve()]=d
 assert d.headings==1,(p.name,'Expected one H1')
 assert not d.duplicates,(p.name,d.duplicates)
 if p.parent.name in ['cs','en']: assert d.lang==p.parent.name
count=0
for p,d in docs.items():
 for link in d.links:
  u=urlsplit(link)
  if u.scheme or u.netloc: continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert target.is_relative_to(ROOT),(p,link,'Outside project')
  assert target.exists(),(p,link,'Missing target')
  if u.fragment and target in docs: assert unquote(u.fragment) in docs[target].ids,(p,link,'Missing fragment')
  count+=1
for lang in ['cs','en']:
 entries=json.loads((ROOT/lang/'search-index.json').read_text(encoding='utf-8'))
 assert len(entries)>20
 for entry in entries:
  u=urlsplit(entry['url']); target=(ROOT/lang/u.path).resolve()
  assert target in docs,entry
  if u.fragment: assert u.fragment in docs[target].ids,entry
for p in (ROOT/'content').glob('*.json'):
 text=p.read_text(encoding='utf-8-sig'); chapter=json.loads(text)
 assert not re.search(r'[A-Z]:\\|users[/\\]|BEGIN .*PRIVATE KEY|github_pat_|ghp_',text,re.I),p
 for lang in ['cs','en']:
  assert re.search(r'<h2 id="[a-z0-9-]+">',chapter[lang]['body']),p
print(f'PASS: {len(docs)} pages, {count} local links/assets, bilingual search indexes and public-content hygiene.')
