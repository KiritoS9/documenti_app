#!/usr/bin/env python3
"""Genera la home e le pagine in progetti/ dai dati qui sotto e da store.json.

    python3 _src/build.py           rigenera le pagine
    python3 _src/build.py --fetch   prima aggiorna store.json dall'App Store

La cartella _src non viene pubblicata: Jekyll ignora quelle che iniziano con "_".
Le privacy policy nelle altre cartelle si modificano a mano.
"""
import json
import pathlib
import sys
import urllib.request
from datetime import datetime
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE_FILE = ROOT / "_src" / "store.json"
BASE = "https://kiritos9.github.io/documenti_app/"
MONTHS = "gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre".split()

APPS = [
    {
        "key": "moodie", "slug": "moodie", "name": "Moodie", "accent": "#ff5a5f",
        "tagline": "Film e serie TV in base al mood.",
        "lede": "Scopri cosa guardare in base al mood del momento, segui le uscite in Italia e ricevi un promemoria quando escono.",
        "privacy": "moodie/", "shots": 7, "size": (700, 1522), "peek": [1, 3, 7], "wide": True,
        "shots_note": "Negli screenshot titoli, trame e locandine sono inventati.",
        "features": [
            ("Scopri per mood", "Scegli l'umore del momento e ricevi suggerimenti che imparano da quello che ti piace."),
            ("Uscite in Italia", "Tutti i film in arrivo al cinema e in digitale, in lista o in un calendario mensile."),
            ("Promemoria", "Un avviso quando esce un film o un nuovo episodio. Scegli tu quanti giorni prima e a che ora."),
            ("Dove guardarlo", "Le piattaforme su cui è disponibile in Italia, in streaming, a noleggio o in acquisto."),
            ("Scheda completa", "Trailer, cast, regia, date di uscita e voti da IMDb, Rotten Tomatoes e Metacritic."),
            ("La tua libreria", "Da vedere, Piaciuti, Visti e Scartati, senza account e con i dati sul dispositivo."),
        ],
        "changes": [
            "Riscritta da zero, nativa per iOS, con il design Liquid Glass",
            "Nuove sezioni Uscite e Promemoria",
            "Titoli da aggiungere a mano, con copertina dalle foto o dalla fotocamera",
            "Suggerimenti più pertinenti per l'Italia",
            "Ottimizzata per iPad e iPhone Duo",
        ],
        "legal": "This product uses the TMDB API but is not endorsed or certified by TMDB.",
    },
    {
        "key": "cullinglab", "slug": "culling-lab", "name": "Culling Lab", "accent": "#3fae6a",
        "tagline": "Seleziona migliaia di foto, senza perdere il controllo.",
        "lede": "L'AI ti aiuta a lavorare più in fretta su grandi quantità di scatti, ma la scelta finale resta sempre tua.",
        "privacy": "culling/", "shots": 3, "size": (1400, 875), "peek": [1], "wide": True, "mac": True,
        "features": [
            ("Navigazione veloce", "Scorri le foto senza attese, anche nei servizi più grandi."),
            ("Analisi con l'AI", "Un supporto durante la selezione, che non sceglie al posto tuo."),
            ("Scatti simili", "Raggruppa in automatico le foto simili per confrontarle meglio."),
            ("Foto da scartare", "Trova rapidamente le foto mosse o meno riuscite."),
            ("Elaborazione locale", "Le foto vengono elaborate sul Mac, per più privacy e velocità."),
            ("Senza distrazioni", "Un'interfaccia minimale, pensata per grandi servizi fotografici."),
        ],
        "audience": ["Matrimoni", "Eventi", "Sport", "Content creator", "Studi fotografici", "Freelance"],
        "changes": ["Corretto il salvataggio delle impostazioni"],
    },
    {
        "key": "gymora", "slug": "gymora-fit", "name": "Gymora Fit", "accent": "#f97316",
        "tagline": "Il tuo allenamento, la tua evoluzione.",
        "lede": "Crea routine su misura, tieni traccia di ogni serie e misura i progressi. Condividi tutto con la community.",
        "privacy": "https://kiritos9.github.io/gymora-privacy/", "shots": 4, "size": (700, 1515), "peek": [2],
        "features": [
            ("Routine drag & drop", "Crea e modifica le sessioni in pochi tap."),
            ("Tracciamento avanzato", "Serie, peso, tempo e tutto lo storico dei progressi."),
            ("Libreria di esercizi", "Demo, varianti e filtri per gruppi muscolari e attrezzature."),
            ("Community", "Pubblica le tue routine, esplora e salva quelle degli altri."),
            ("Supporto trainer", "Invia e ricevi routine tra utenti e trainer."),
            ("Statistiche", "Analisi delle performance e andamento nel tempo."),
        ],
        "changes": ["Note per ogni esercizio", "Nuovo flusso di recupero password", "Correzioni minori"],
    },
    {
        "key": "scanner", "slug": "lidar-scanner", "name": "LiDAR Scanner", "accent": "#38a3f5",
        "tagline": "Stanze e oggetti in 3D, in pochi secondi.",
        "lede": "Acquisisci scene tridimensionali con i colori reali, guardale sul dispositivo e prendi le misure direttamente nel modello.",
        "privacy": "3dscan/", "shots": 3, "size": (700, 1515), "peek": [2],
        "features": [
            ("Scansione in tempo reale", "Il modello 3D si costruisce mentre inquadri, con il sensore LiDAR."),
            ("Colori reali", "I colori della scena vengono acquisiti con la fotocamera."),
            ("Strumenti di misura", "Prendi le misure direttamente all'interno del modello."),
            ("Vertici e triangoli", "Il conteggio della mesh generata, sempre in vista."),
            ("Libreria", "Organizza le scansioni salvate e ritrovale con la ricerca."),
            ("Elaborazione locale", "Tutto viene elaborato sul dispositivo."),
        ],
        "audience": ["Rilievo di interni", "Misure di stanze", "Documentazione tecnica", "Arredamento", "Ristrutturazioni", "Prototipazione 3D"],
        "requires": "Richiede un dispositivo Apple con sensore LiDAR.",
    },
    {
        "key": "trebbiafacile", "slug": "trebbia-facile", "name": "Trebbia Facile", "accent": "#2fa84f",
        "tagline": "Il lavoro nei campi, sempre sotto controllo.",
        "lede": "Pensata per trebbiatori e operatori agricoli: clienti, lavori, mezzi e carburante, sempre con te.",
        "privacy": "trebbiaFacile/", "shots": 4, "size": (700, 1515), "peek": [1],
        "features": [
            ("Lavori", "Registra ogni intervento in pochi secondi: cliente, terreno, coltura, ore e tariffa."),
            ("Clienti e terreni", "Gestisci i clienti e calcola la superficie sul campo con il GPS del telefono."),
            ("Mezzi", "Ogni macchina della flotta, con tipologia, nome e storico di utilizzo."),
            ("Nafta", "I rifornimenti giornalieri per ogni mezzo e i consumi nel tempo."),
            ("Report PDF", "Report e preventivi pronti da inviare o stampare."),
            ("Meteo e offline", "Previsioni integrate per pianificare. Funziona anche senza connessione, senza account."),
        ],
    },
]

OTHERS = [
    {"name": "Tacito", "icon": "assets/icons/tacito.png", "accent": "#0064d2", "meta": "iPhone", "tech": "SwiftUI · SwiftData",
     "desc": "Quanto spendi in abbonamenti, quando si rinnovano e chi ti deve ancora la sua parte.",
     "links": [("privacy e assistenza", "tacito/")]},
    {"name": "SpeechBoard", "icon": "assets/icons/speechboard.png", "accent": "#3f5bf0", "meta": "iPhone", "tech": "SwiftUI · SpeechAnalyzer · Apple Intelligence",
     "desc": "Tastiera di dettatura: parli e il testo arriva già pulito in qualsiasi app, tutto sul dispositivo.",
     "links": [("privacy", "speechBoard/")]},
    {"name": "Tappig", "icon": "assets/icons/tappig.png", "accent": "#e8739a", "meta": "iOS · Android", "tech": "Godot",
     "desc": "Riporta i maiali nel recinto a colpi di tap, tra trappole, animali dispettosi e una notte di Halloween."},
    {"name": "MyClean", "icon": "assets/icons/myclean.png", "accent": "#4aa8ff", "meta": "macOS", "tech": "SwiftUI",
     "desc": "Pulizia, privacy e manutenzione per macOS. Tutto passa dal Cestino e si può ripristinare."},
    {"name": "iSync", "letter": "i", "accent": "#a78bfa", "meta": "macOS", "tech": "SwiftUI · libimobiledevice",
     "desc": "Gestisce un iPhone o iPad collegato al Mac: backup, foto, file, messaggi, contatti, musica e diagnostica."},
    {"name": "LR Scroll", "icon": "assets/icons/lrscroll.png", "accent": "#7dd3fc", "meta": "macOS", "tech": "Swift · plugin Lua",
     "desc": "In Lightroom Classic, le rotelle del mouse regolano direttamente esposizione e temperatura."},
]

SUN_MOON = (
    '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
    '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
)
APPLE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.05 12.54c-.03-2.6 2.12-3.85 2.22-3.91-1.21-1.77-3.09-2.01-3.76-2.04-1.6-.16-3.12.94-3.93.94-.81 0-2.06-.92-3.39-.89-1.74.03-3.35 1.01-4.25 2.57-1.81 3.14-.46 7.8 1.3 10.35.86 1.25 1.89 2.65 3.24 2.6 1.3-.05 1.79-.84 3.36-.84s2.01.84 3.39.81c1.4-.02 2.28-1.27 3.14-2.53.99-1.45 1.4-2.85 1.42-2.93-.03-.01-2.72-1.04-2.74-4.13zM14.47 4.9c.71-.87 1.2-2.07 1.07-3.27-1.03.04-2.28.69-3.02 1.55-.66.77-1.24 1.99-1.09 3.17 1.15.09 2.33-.58 3.04-1.45z"/></svg>'


def platform(info):
    if info["kind"] == "mac-software":
        return "Mac"
    return "iPhone e iPad" if info["ipad"] else "iPhone"


def short_platform(info):
    return "macOS" if info["kind"] == "mac-software" else "iOS"


def min_os(info):
    return f'{short_platform(info)} {info["minimumOsVersion"]}'


def date_it(value):
    d = datetime.strptime(value[:10], "%Y-%m-%d")
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def link(target, root):
    return target if target.startswith("http") else root + target


def page(title, description, body, root, url, image):
    return f"""<!DOCTYPE html>
<html lang="it" data-theme="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="theme-color" content="#08090c" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(description)}" />
  <meta property="og:url" content="{BASE}{url}" />
  <meta property="og:image" content="{BASE}{image}" />
  <link rel="canonical" href="{BASE}{url}" />
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%2308090c'/%3E%3Cpath d='M8 10l6 6-6 6' fill='none' stroke='%237dd3a8' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M16 23h8' stroke='%23eef0f4' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E" />
  <script>
    document.documentElement.classList.add("js");
    try {{ var t = localStorage.getItem("theme"); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}
  </script>
  <link rel="stylesheet" href="{root}assets/site.css" />
</head>
<body>

<header class="nav">
  <div class="wrap">
    <a class="brand" href="{root or './'}"><b>stefano</b><i>@soriano</i>:~$<span class="cursor" aria-hidden="true"></span></a>
    <nav aria-label="Principale">
      <a href="{root}#app-store">app-store</a>
      <a class="opt" href="{root}#progetti">progetti</a>
      <a href="{root}#contatti">contatti</a>
      <button class="theme" type="button" aria-label="Cambia tema">{SUN_MOON}</button>
    </nav>
  </div>
</header>

{body}

<script src="{root}assets/site.js"></script>
</body>
</html>
"""


def footer(root, legal=None):
    extra = f'<span class="legal">{escape(legal)}</span>' if legal else ""
    return f"""<footer class="foot">
  <div class="wrap">
    <span>© 2026 Stefano Soriano</span>
    <a href="mailto:stefanosoriano51@gmail.com">stefanosoriano51@gmail.com</a>
    {extra}
  </div>
</footer>"""


def home(store):
    total = len(APPS) + len(OTHERS)

    ls = ""
    for app in APPS:
        info = store[app["key"]]
        ls += (f'<a href="progetti/{app["slug"]}/"><img src="assets/apps/{app["slug"]}/icon.png" alt="" width="16" height="16" />'
               f'<span class="n">{app["slug"]}/</span><span class="v">v{info["version"]}</span><span class="p">{short_platform(info)}</span></a>\n')

    cards = ""
    for app in APPS:
        info = store[app["key"]]
        cls = ' class="wide"' if app.get("wide") else ""
        peek_class = "peek mac" if app.get("mac") else ("peek trio" if len(app["peek"]) > 1 else "peek")
        w, h = app["size"]
        imgs = "".join(
            f'<img src="assets/apps/{app["slug"]}/s{n}.jpg" alt="" width="{w}" height="{h}" loading="lazy" />' for n in app["peek"]
        )
        cards += f"""
        <li{cls}>
          <a class="card app reveal" href="progetti/{app["slug"]}/" style="--a:{app["accent"]}">
            <div class="app-head">
              <img class="icon" src="assets/apps/{app["slug"]}/icon.png" alt="" width="58" height="58" />
              <div>
                <h3>{escape(app["name"])}</h3>
                <p class="meta">v{info["version"]} · {platform(info)}</p>
              </div>
              <span class="go" aria-hidden="true">→</span>
            </div>
            <p class="desc">{escape(app["tagline"])}</p>
            <div class="{peek_class}">{imgs}</div>
          </a>
        </li>"""

    minis = ""
    for p in OTHERS:
        icon = (f'<img class="icon" src="{p["icon"]}" alt="" width="46" height="46" />' if "icon" in p
                else f'<div class="icon letter" aria-hidden="true">{p["letter"]}</div>')
        links = ""
        if p.get("links"):
            links = '<p class="links">' + " ".join(f'<a href="{t}">{escape(n)} →</a>' for n, t in p["links"]) + "</p>"
        minis += f"""
        <li>
          <article class="card mini reveal" style="--a:{p["accent"]}">
            <div class="mini-head">
              {icon}
              <div>
                <h3>{escape(p["name"])}</h3>
                <p class="meta">{escape(p["meta"])}</p>
              </div>
            </div>
            <p class="desc">{escape(p["desc"])}</p>
            <p class="tech">{escape(p["tech"])}</p>
            {links}
          </article>
        </li>"""

    body = f"""<main class="wrap">

  <section class="hero">
    <div>
      <p class="kicker">// sviluppatore iOS e macOS</p>
      <h1>Stefano<br />Soriano</h1>
      <p class="lede">Costruisco app native per iPhone e Mac, dall'idea all'App Store.</p>
      <div class="actions">
        <a class="btn primary" href="#app-store">Guarda le app</a>
        <a class="btn" href="mailto:stefanosoriano51@gmail.com">Scrivimi</a>
      </div>
      <div class="stats">
        <div><b>{len(APPS)}</b><span>app su App Store</span></div>
        <div><b>{total}</b><span>progetti in tutto</span></div>
      </div>
    </div>

    <div class="term" data-type>
      <div class="term-bar"><i></i><i></i><i></i><span>zsh — ~/progetti</span></div>
      <div class="term-body">
        <p class="cmd">ls --app-store</p>
        <div class="after">
          <div class="ls">
{ls}          </div>
          <p class="note"># {len(APPS)} pubblicate, altre {len(OTHERS)} qui sotto</p>
          <p class="cmd" aria-hidden="true"><span class="cursor"></span></p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="app-store">
    <div class="section-head">
      <h2><small>01 / app-store</small>Sull'App Store</h2>
      <p>Apri una card per vedere i dettagli.</p>
    </div>
    <ul class="bento">{cards}
    </ul>
  </section>

  <section class="section" id="progetti">
    <div class="section-head">
      <h2><small>02 / progetti</small>Altri progetti</h2>
    </div>
    <ul class="grid">{minis}
    </ul>
  </section>

  <section class="section" id="contatti">
    <div class="about">
      <div class="reveal">
        <div class="section-head" style="margin-bottom:0">
          <h2><small>03 / contatti</small>Parliamone</h2>
        </div>
        <p>Una domanda su un'app, un problema o un'idea? Scrivimi.</p>
        <div class="actions">
          <a class="btn primary" href="mailto:stefanosoriano51@gmail.com">Scrivimi una mail</a>
          <a class="btn" href="https://github.com/KiritoS9">GitHub</a>
        </div>
      </div>
      <div class="code reveal">
        <div class="term-bar"><i></i><i></i><i></i><span>Developer.swift</span></div>
<pre><code><span class="k">struct</span> <span class="t">Stefano</span>: <span class="t">Developer</span> {{
    <span class="k">let</span> platforms = [<span class="s">"iOS"</span>, <span class="s">"macOS"</span>, <span class="s">"Android"</span>]
    <span class="k">let</span> stack = [<span class="s">"Swift"</span>, <span class="s">"SwiftUI"</span>, <span class="s">"SwiftData"</span>, <span class="s">"Godot"</span>]
    <span class="k">let</span> appStore = <span class="u">{len(APPS)}</span>
    <span class="k">let</span> mail = <a class="s" href="mailto:stefanosoriano51@gmail.com">"stefanosoriano51@gmail.com"</a>
}}</code></pre>
      </div>
    </div>
  </section>

</main>

{footer("")}"""
    return page("Stefano Soriano – App per iPhone e Mac",
                "Le app per iPhone e Mac di Stefano Soriano: Moodie, Culling Lab, Gymora Fit, LiDAR Scanner, Trebbia Facile e altri progetti.",
                body, "", "", "assets/icons/tacito.png")


def detail(app, store, prev_app, next_app):
    root = "../../"
    info = store[app["key"]]
    slug = app["slug"]
    w, h = app["size"]

    def row(key, value, cls="s"):
        return f'  <span class="t">"{key}"</span>: <span class="{cls}">"{escape(value)}"</span>'

    rows = [
        row("versione", info["version"], "u"),
        row("piattaforma", platform(info)),
        row("richiede", min_os(info)),
        row("categoria", info["genres"][0]),
        row("prezzo", info["formattedPrice"]),
        row("prima uscita", date_it(info["releaseDate"])),
        row("aggiornata", date_it(info["currentVersionReleaseDate"])),
    ]
    manifest = "{\n" + ",\n".join(rows) + "\n}"

    shots = "\n".join(
        f'      <img src="{root}assets/apps/{slug}/s{n}.jpg" alt="Screenshot {n} di {escape(app["name"])}" width="{w}" height="{h}" loading="lazy" />'
        for n in range(1, app["shots"] + 1)
    )

    features = "".join(f"""
      <li><article class="card feature reveal">
        <p class="idx">{i:02d}</p>
        <h3>{escape(t)}</h3>
        <p>{escape(d)}</p>
      </article></li>""" for i, (t, d) in enumerate(app["features"], 1))

    panels = ""
    if app.get("audience"):
        chips = "".join(f"<li>{escape(a)}</li>" for a in app["audience"])
        extra = f'<p>{escape(app["requires"])}</p>' if app.get("requires") else ""
        panels += f"""
      <div class="card panel reveal">
        <h3>// perfetta per</h3>
        <ul class="chips">{chips}</ul>
        {extra}
      </div>"""
    if app.get("changes"):
        items = "".join(f"<li>{escape(c)}</li>" for c in app["changes"])
        panels += f"""
      <div class="card panel reveal">
        <h3>// novità della versione {info["version"]}</h3>
        <ul class="log">{items}</ul>
      </div>"""
    panels_html = f"""
  <section class="section" style="padding-top:0">
    <div class="split">{panels}
    </div>
  </section>""" if panels else ""

    shots_note = f'<p class="note-small">{escape(app["shots_note"])}</p>' if app.get("shots_note") else ""

    body = f"""<main class="wrap" style="--a:{app["accent"]}">

  <p class="crumb"><a href="{root}">~</a> / <a href="{root}#app-store">app-store</a> / <b>{slug}</b></p>

  <section class="detail-hero">
    <div>
      <img class="icon" src="{root}assets/apps/{slug}/icon.png" alt="" width="112" height="112" />
      <h1>{escape(app["name"])}</h1>
      <p class="lede">{escape(app["lede"])}</p>
      <div class="actions">
        <a class="btn primary" href="{info["trackViewUrl"]}">{APPLE}Scarica su App Store</a>
        <a class="btn" href="{link(app["privacy"], root)}">Privacy</a>
      </div>
    </div>
    <div class="code manifest">
      <div class="term-bar"><i></i><i></i><i></i><span>{slug}.json</span></div>
<pre><code>{manifest}</code></pre>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="section-head">
      <div>
        <h2>Screenshot</h2>
        {shots_note}
      </div>
      <div class="arrows">
        <button type="button" data-dir="-1" aria-label="Screenshot precedente">←</button>
        <button type="button" data-dir="1" aria-label="Screenshot successivo">→</button>
      </div>
    </div>
    <div class="gallery{" mac" if app.get("mac") else ""}" tabindex="0" aria-label="Screenshot di {escape(app["name"])}">
{shots}
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="section-head"><h2>Cosa fa</h2></div>
    <ul class="features">{features}
    </ul>
  </section>
{panels_html}

  <nav class="pager" aria-label="Altre app">
    <a class="card" href="{root}progetti/{prev_app["slug"]}/" style="--a:{prev_app["accent"]}">
      <img class="icon" src="{root}assets/apps/{prev_app["slug"]}/icon.png" alt="" width="44" height="44" />
      <span><small>← precedente</small><b>{escape(prev_app["name"])}</b></span>
    </a>
    <a class="card next" href="{root}progetti/{next_app["slug"]}/" style="--a:{next_app["accent"]}">
      <img class="icon" src="{root}assets/apps/{next_app["slug"]}/icon.png" alt="" width="44" height="44" />
      <span><small>successiva →</small><b>{escape(next_app["name"])}</b></span>
    </a>
  </nav>

</main>

{footer(root, app.get("legal"))}"""
    return page(f'{app["name"]} – {app["tagline"]}', app["lede"], body, root, f"progetti/{slug}/", f"assets/apps/{slug}/icon.png")


def fetch(store):
    ids = ",".join(str(v["trackId"]) for v in store.values())
    with urllib.request.urlopen(f"https://itunes.apple.com/lookup?id={ids}&country=it") as response:
        results = {r["trackId"]: r for r in json.load(response)["results"]}
    for entry in store.values():
        fresh = results.get(entry["trackId"])
        if fresh:
            for field in ("version", "formattedPrice", "genres", "minimumOsVersion", "currentVersionReleaseDate"):
                entry[field] = fresh[field]
    STORE_FILE.write_text(json.dumps(store, ensure_ascii=False, indent=1) + "\n")


def main():
    store = json.loads(STORE_FILE.read_text())
    if "--fetch" in sys.argv:
        fetch(store)
    (ROOT / "index.html").write_text(home(store))
    for i, app in enumerate(APPS):
        out = ROOT / "progetti" / app["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(detail(app, store, APPS[i - 1], APPS[(i + 1) % len(APPS)]))


if __name__ == "__main__":
    main()
