"""Build the bilingual ArdaNPCs wiki using Python's standard library."""
from pathlib import Path
import json, re, html
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
ORDER = ['getting-started', 'npc-editor', 'appearance', 'quests', 'scripts', 'scripted-objects', 'services', 'troubleshooting']
SITE = 'https://sroskus123.github.io/ArdaNPCs/'
CF = 'https://www.curseforge.com/minecraft/mc-mods/ardanpcs'
REPO = 'https://github.com/sroskus123/ArdaNPCs'
UI = {
 'cs': dict(home='Přehled', docs='Příručka', search='Hledat v celé wiki…', skip='Přejít na obsah', toc='Na této stránce', menu='Navigace', download='Stáhnout mod', copy='Kopírovat', copied='Zkopírováno', selected='Označeno — zkopíruj text', empty='Nic nenalezeno. Zkus kratší výraz.', results='Výsledky hledání', close='Zavřít', next='Další kapitola', prev='Předchozí kapitola', footer='Dokumentace pro ArdaNPCs 1.1.0 · Fabric 1.21.8', top='Zpět nahoru', updated='Aktualizováno 7. 11. 2026', guide='Návod', home_title='Dej svému světu příběh.', home_desc='Od prvního NPC po vlastní quest, skript a živé město. Praktická příručka pro tvůrce map i správce serverů.', start='Vytvořit první NPC', browse='Vybrat kapitolu', chapters='Všechno na jednom místě', chapter_desc='Začni od základů, nebo otevři přesně to, co teď potřebuješ.', tip_title='Modely z jiných modů?', tip='Ano, lze vybrat entity z nainstalovaných modů. Jejich vzhled závisí na rendereru; vlastní animace ověř ve svém modpacku. NPC si zachovává systémy ArdaNPCs.', tip_link='Jak funguje výběr modelu', flow='Tři kroky k vlastnímu příběhu', steps=[('Vytvoř postavu','Jméno, vzhled, výbava a chování.','npc-editor'),('Přidej důvod k rozhovoru','Dialogy, cíle a odměny za splnění.','quests'),('Oživ interakce','Skripty, obchod, pošta a společníci.','scripts')], version_note='Tato wiki popisuje verzi 1.1.0. Pro starší verze se nabídky a dostupné funkce mohou lišit.', issue='Nahlásit chybu v návodu'),
 'en': dict(home='Overview', docs='Documentation', search='Search the whole wiki…', skip='Skip to content', toc='On this page', menu='Navigation', download='Download mod', copy='Copy', copied='Copied', selected='Selected — copy the text', empty='No results. Try a shorter search.', results='Search results', close='Close', next='Next chapter', prev='Previous chapter', footer='Documentation for ArdaNPCs 1.1.0 · Fabric 1.21.8', top='Back to top', updated='Updated 7 November 2026', guide='Guide', home_title='Give your world a story.', home_desc='From your first NPC to custom quests, scripts and a lively town. A practical guide for map makers and server admins.', start='Create your first NPC', browse='Browse the guide', chapters='Everything in one place', chapter_desc='Start with the basics or jump to the system you need.', tip_title='Models from other mods?', tip='You can choose entities from installed mods. Appearance depends on their renderer; test custom animations in your modpack. The NPC keeps the systems of ArdaNPCs.', tip_link='How model selection works', flow='Three steps to your own story', steps=[('Create a character','Name, appearance, equipment and behaviour.','npc-editor'),('Give players a reason to talk','Dialogues, objectives and quest rewards.','quests'),('Bring interactions to life','Scripts, trading, mail and companions.','scripts')], version_note='This wiki describes version 1.1.0. Menus and available features may differ in older versions.', issue='Report a documentation issue')
}

class PlainText(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self, data): self.parts.append(data)
def plain(source):
 p=PlainText(); p.feed(source); return ' '.join(' '.join(p.parts).split())
def esc(text): return html.escape(str(text), quote=True)
def icon():
 return '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 28V12l11-8 11 8v16h-7V17h-8v11Z" fill="currentColor"/><path d="M3 28h26M12 10h8" fill="none" stroke="currentColor" stroke-width="2"/></svg>'

pages=[]
for slug in ORDER:
 path=ROOT/'content'/f'{slug}.json'
 if not path.exists(): raise SystemExit(f'Missing chapter: {path.name}')
 p=json.loads(path.read_text(encoding='utf-8-sig'))
 assert p['slug']==slug
 for lang in UI:
  assert all(p[lang].get(k) for k in ['title','description','body'])
  assert not re.search(r'<(?:script|iframe)|\son\w+=|javascript:', p[lang]['body'], re.I), slug
 pages.append(p)

def shell(lang, slug, title, description, body, headings=()):
 u=UI[lang]; other='en' if lang=='cs' else 'cs'
 nav=f'<a class="nav-home" href="index.html"'+(' aria-current="page"' if slug=='index' else '')+f'>{u["home"]}</a>'
 for i,p in enumerate(pages,1):
  active=' aria-current="page"' if p['slug']==slug else ''
  nav+=f'<a href="{p["slug"]}.html"{active}><span>{i:02}</span>{esc(p[lang]["title"])}</a>'
 toc=''.join(f'<a href="#{ident}">{esc(plain(text))}</a>' for ident,text in headings)
 return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#153e35"><meta name="description" content="{esc(description)}"><title>{esc(title)} — ArdaNPCs Wiki</title><link rel="icon" href="../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../assets/style.css"><link rel="canonical" href="{SITE}{lang}/{slug}.html"><link rel="alternate" hreflang="{other}" href="{SITE}{other}/{slug}.html"><script src="../assets/site.js" defer></script></head>
<body id="top" data-lang="{lang}"><a class="skip" href="#main">{u['skip']}</a>
<header class="topbar"><a class="brand" href="index.html"><span class="brand-icon">{icon()}</span><span>ArdaNPCs <small>WIKI & GUIDES</small></span></a><div class="search-wrap"><label class="sr-only" for="search">{u['search']}</label><input id="search" type="search" autocomplete="off" placeholder="{u['search']}" aria-controls="search-results"><kbd>/</kbd><section id="search-results" aria-label="{u['results']}" hidden><p id="search-status" aria-live="polite"></p><div id="search-links"></div><button type="button" id="close-search">{u['close']}</button></section></div><nav class="toplinks" aria-label="Links"><a class="language" href="../{other}/{slug}.html" lang="{other}" hreflang="{other}">{'EN' if lang=='cs' else 'CS'}</a><a class="download" href="{CF}">{u['download']} <span aria-hidden="true">↗</span></a></nav><button class="mobile-menu" type="button" aria-expanded="false" aria-controls="sidebar">{u['menu']}</button></header>
<div class="layout"><aside id="sidebar"><div class="sidebar-label">{u['docs']}</div><nav aria-label="{u['docs']}">{nav}</nav><div class="version"><span class="version-dot"></span>ArdaNPCs <strong>1.1.0</strong><small>Minecraft 1.21.8 · Fabric</small></div><a class="repo-link" href="{REPO}">GitHub <span aria-hidden="true">↗</span></a></aside><main id="main" tabindex="-1">{body}<footer><p>{u['footer']}<br><span>{u['updated']}</span></p><a href="{REPO}/issues">{u['issue']} ↗</a><a href="#top">{u['top']} ↑</a></footer></main><aside class="page-toc">{('<div class="sidebar-label">'+u['toc']+'</div><nav aria-label="'+u['toc']+'">'+toc+'</nav>') if toc else ''}</aside></div>
<script id="ui-data" type="application/json">{json.dumps({k:u[k] for k in ['copy','copied','selected','empty','results']}, ensure_ascii=False)}</script></body></html>'''

for lang in UI:
 folder=ROOT/lang; folder.mkdir(exist_ok=True); u=UI[lang]
 cards=''
 for i,p in enumerate(pages,1):
  cards+=f'<a class="chapter-card" href="{p["slug"]}.html"><span class="chapter-number">{i:02}</span><h3>{esc(p[lang]["title"])}</h3><p>{esc(p[lang]["description"])}</p><span class="card-arrow" aria-hidden="true">↗</span></a>'
 steps=''.join(f'<a href="{s}.html"><span>{i:02}</span><h3>{t}</h3><p>{d}</p></a>' for i,(t,d,s) in enumerate(u['steps'],1))
 home=f'''<section class="hero"><div class="eyebrow">ARDANPCS 1.1.0 <span>FABRIC 1.21.8</span></div><h1>{u['home_title']}</h1><p>{u['home_desc']}</p><div class="hero-actions"><a class="primary" href="getting-started.html">{u['start']} <span aria-hidden="true">→</span></a><a href="#chapters">{u['browse']} ↓</a></div><div class="hero-art" aria-hidden="true">{icon()}<span>BUILD YOUR STORY</span></div></section><section class="home-section" id="chapters"><div class="section-heading"><span>01 / {u['docs'].upper()}</span><h2>{u['chapters']}</h2><p>{u['chapter_desc']}</p></div><div class="chapters">{cards}</div></section><section class="compat-note"><span class="note-symbol" aria-hidden="true">◇</span><div><h2>{u['tip_title']}</h2><p>{u['tip']}</p><a href="appearance.html">{u['tip_link']} →</a></div></section><section class="home-section"><div class="section-heading"><span>02 / WORKFLOW</span><h2>{u['flow']}</h2></div><div class="steps-grid">{steps}</div></section><p class="version-note">{u['version_note']}</p>'''
 (folder/'index.html').write_text(shell(lang,'index',u['home'],u['home_desc'],home),encoding='utf-8')
 index=[]
 for i,p in enumerate(pages):
  article=p[lang]; slug=p['slug']
  headings=re.findall(r'<h2\s+id="([^"]+)"[^>]*>(.*?)</h2>',article['body'],re.S)
  body=re.sub(r'(<table\b.*?</table>)',r'<div class="table-scroll" tabindex="0">\1</div>',article['body'],flags=re.S)
  pager='<nav class="pager" aria-label="'+u['docs']+'">'
  if i: pager+=f'<a href="{pages[i-1]["slug"]}.html"><small>← {u["prev"]}</small>{esc(pages[i-1][lang]["title"])}</a>'
  if i+1<len(pages): pager+=f'<a href="{pages[i+1]["slug"]}.html"><small>{u["next"]} →</small>{esc(pages[i+1][lang]["title"])}</a>'
  pager+='</nav>'
  content=f'<div class="article-header"><div class="eyebrow">{u["guide"]} {i+1:02} <span>1.1.0</span></div><h1>{esc(article["title"])}</h1><p>{esc(article["description"])}</p></div><article class="prose">{body}</article>{pager}'
  (folder/f'{slug}.html').write_text(shell(lang,slug,article['title'],article['description'],content,headings),encoding='utf-8')
  segments=re.split(r'(<h2\s+id="[^"]+"[^>]*>.*?</h2>)',article['body'],flags=re.S)
  index.append(dict(title=article['title'],text=article['description'],url=f'{slug}.html',page=article['title']))
  for j in range(1,len(segments),2):
   h=re.search(r'id="([^"]+)"[^>]*>(.*?)</h2>',segments[j],re.S)
   index.append(dict(title=plain(h[2]),text=plain(segments[j+1]),url=f'{slug}.html#{h[1]}',page=article['title']))
 (folder/'search-index.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf-8')

def redirect(path, target):
 (ROOT/path).write_text(f'<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{SITE}{target}"><title>ArdaNPCs Wiki</title></head><body><h1>ArdaNPCs Wiki</h1><p><a href="{target}">Otevřít příručku / Open the guide</a></p><p><a href="en/index.html">English</a></p></body></html>',encoding='utf-8')
redirect('index.html','cs/index.html')
redirect('ARDANPCS_QUEST_MANUAL_CS.html','cs/quests.html')
(ROOT/'.nojekyll').write_text('',encoding='utf-8')
print(f'Built {len(pages)*2+2} documentation pages, 2 redirects and 2 search indexes.')
