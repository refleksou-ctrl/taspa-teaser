"""Build the two review pages /a/ and /b/ from index.html (they differ only in section order and the map).
Re-run after editing index.html:  python3 versions.py"""
import os, re

PIN = '<div class="pin"><svg><use href="#logo"/></svg><svg viewBox="0 0 22 20"><path d="M8.4 18.6 0.6 4.6C-.5 2.6.9 0 3.2 0h15.6c2.3 0 3.7 2.6 2.6 4.6l-7.8 14c-1.2 1.9-4 1.9-5.2 0Z"/></svg></div>'
OSM = '<a class="osm" href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">© OpenStreetMap</a>'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Spordi+8+Tapa'

LOC_A = f'''<section class="loc light" id="asukoht">
    <div class="wrap loc__row">
      <div class="loc__info">
        <h2>Asukoht</h2>
        <p>Spordi 8, 45107 Tapa</p>
        <ul class="loc__list">
          <li>Kesklinn <span>1,1 km <svg class="arrow" aria-hidden="true"><use href="#arrow"/></svg> 15 min jalgsi</span></li>
          <li>Raudtee- ja bussijaam <span>1,5 km <svg class="arrow" aria-hidden="true"><use href="#arrow"/></svg> 20 min jalgsi</span></li>
          <li>Tapa linnak <span>1,8 km <svg class="arrow" aria-hidden="true"><use href="#arrow"/></svg> 25 min jalgsi</span></li>
        </ul>
        <a class="btn" href="{MAPS}" target="_blank" rel="noopener">Ava kaardil <svg class="arrow"><use href="#arrow"/></svg></a>
      </div>
      <div class="loc__card" role="img" aria-label="Kaart: Taspa asub Tapal, Spordi 8">
        <div class="map"><img src="img/map-dark.svg" alt="" width="1440" height="700" loading="lazy" decoding="async">{PIN}</div>
        {OSM}
      </div>
    </div>
  </section>
'''
LOC_B = f'''<section class="locb" id="asukoht" aria-label="Asukoht: Spordi 8, Tapa">
    <div class="map"><img src="img/map-light.svg" alt="Kaart: Taspa asub Tapal, Spordi 8" width="1440" height="700" loading="lazy" decoding="async">{PIN}
      <p class="chip chip--jaam"><b>1,2 km</b><span>Raudteejaam</span></p>
      <p class="chip chip--linn"><b>1,1 km</b><span>Kesklinn</span></p>
      <p class="chip chip--linnak"><b>1,4 km</b><span>Tapa sõjaväelinnak</span></p>
    </div>
    {OSM}
  </section>
'''

src = open('index.html').read()
news = re.search(r'  <section class="news light">.*?</section>\n', src, re.S).group(0)
photo = re.search(r'  <figure class="photo">.*?</figure>\n', src, re.S).group(0)
assert news and photo
def rebase(html):   # pages live one folder down
    return (html.replace('href="styles.css"', 'href="../styles.css"').replace('src="motion.js"', 'src="../motion.js"')
                .replace('"img/', '"../img/').replace('href="./"', 'href="../"'))

assert news + photo in src
pages = {'a': news + photo + '  ' + LOC_A, 'b': '  ' + LOC_B + news.replace('news light', 'news dark')}  # B: dark newsletter, as in Figma
for name, mid in pages.items():
    os.makedirs(name, exist_ok=True)
    html = src.replace(news + photo, mid)
    html = re.sub(r'\s*<li><a class="btn" href="https://www.google.com/maps[^\n]*</li>', '', html, count=1)  # footer map button: the map section has its own
    open(f'{name}/index.html', 'w').write(rebase(html))
    print(name, 'ok')
