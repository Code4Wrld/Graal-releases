#!/usr/bin/env python3
"""Assemble les pages légales autonomes de graaltv.com : en-tête, CSS et pied communs + corps, en six langues.

Sources : <page>.html (français, qui fait foi) et <page>.<langue>.html (traductions), au même format :
ligne 1 = titre, ligne 2 = description, puis le corps. La version française est écrite dans la page (lue sans
JavaScript) ; les autres sont dans des <template> : ../lang.js choisit la langue (?lang=, puis le choix gardé
« graal-lang », puis le navigateur) et le script de la page met la bonne version à la place, sans id en double.
"""
import re, sys, pathlib

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1])

PAGES = ["cgv", "confidentialite", "mentions-legales"]
LANGS = ["fr", "en", "es", "it", "pt", "de"]

# Textes communs, les mêmes que ceux du pied de page de l'accueil (index.html, clés foot.*).
UI = {
    "fr": dict(names=["Conditions de vente", "Confidentialité", "Mentions légales"], nav="Pages légales", lang="Langue",
               contact="Contact", notice=None, readfr=None,
               legal="Graal est un lecteur multimédia. Il ne fournit, n'héberge, ne vend ni ne recommande aucune chaîne, playlist ou contenu audiovisuel. Chaque utilisateur est seul responsable des sources qu'il y ajoute et doit avoir le droit de les lire."),
    "en": dict(names=["Terms of sale", "Privacy", "Legal notice"], nav="Legal pages", lang="Language", contact="Contact",
               notice="Translation provided for information only; only the French version is legally binding.", readfr="Read the French version",
               legal="Graal is a media player. It does not provide, host, sell or recommend any channel, playlist or audiovisual content. Each user is solely responsible for the sources they add and must have the right to play them."),
    "es": dict(names=["Condiciones de venta", "Privacidad", "Aviso legal"], nav="Páginas legales", lang="Idioma", contact="Contacto",
               notice="Traducción a título informativo; solo la versión francesa da fe.", readfr="Leer la versión francesa",
               legal="Graal es un reproductor multimedia. No proporciona, aloja, vende ni recomienda ningún canal, lista ni contenido audiovisual. Cada usuario es el único responsable de las fuentes que añade y debe tener derecho a reproducirlas."),
    "it": dict(names=["Condizioni di vendita", "Privacy", "Note legali"], nav="Pagine legali", lang="Lingua", contact="Contatto",
               notice="Traduzione a titolo informativo; fa fede solo la versione francese.", readfr="Leggi la versione francese",
               legal="Graal è un lettore multimediale. Non fornisce, ospita, vende né consiglia alcun canale, playlist o contenuto audiovisivo. Ogni utente è l'unico responsabile delle fonti che aggiunge e deve avere il diritto di riprodurle."),
    "pt": dict(names=["Condições de venda", "Privacidade", "Aviso legal"], nav="Páginas legais", lang="Idioma", contact="Contacto",
               notice="Tradução para informação; só a versão francesa faz fé.", readfr="Ler a versão francesa",
               legal="O Graal é um leitor multimédia. Não fornece, aloja, vende nem recomenda qualquer canal, lista ou conteúdo audiovisual. Cada utilizador é o único responsável pelas fontes que adiciona e deve ter o direito de as reproduzir."),
    "de": dict(names=["Verkaufsbedingungen", "Datenschutz", "Impressum"], nav="Rechtliche Seiten", lang="Sprache", contact="Kontakt",
               notice="Übersetzung zur Information; maßgeblich ist allein die französische Fassung.", readfr="Französische Fassung lesen",
               legal="Graal ist ein Mediaplayer. Er stellt keine Sender, Playlists oder audiovisuellen Inhalte bereit, hostet, verkauft oder empfiehlt sie nicht. Jeder Nutzer ist allein für die hinzugefügten Quellen verantwortlich und muss das Recht haben, sie abzuspielen."),
}

CSS = """
/* Pages légales de graaltv.com : une colonne lisible sur tout écran, l'aspect sombre de Graal. */
:root { color-scheme: dark; --bg: #0B081B; --panel: #17142B; --panel2: #1F1B38; --border: #343050; --text: #ECECF4; --dim: #B4B4CE; --faint: #8A8AA8; --accent: #B79BFF; --todo: #F5C518; --check: #7FD4FF; }
* { box-sizing: border-box; }
html { background: var(--bg); scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
body { margin: 0; color: var(--text); font: 17px/1.65 system-ui, "Segoe UI", Roboto, sans-serif; padding: 24px 16px 64px; overflow-wrap: break-word; }
main, .top, .foot { max-width: 780px; margin: 0 auto; }
a { color: var(--accent); overflow-wrap: anywhere; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.top { display: flex; flex-wrap: wrap; gap: 6px 14px; align-items: center; margin-bottom: 28px; font-size: 15px; }
.top .home { font-weight: 700; text-decoration: none; margin-right: auto; }
.top a:not(.home) { color: var(--faint); text-decoration: none; }
.top a[aria-current] { color: var(--text); font-weight: 700; }
.langs { display: flex; flex-wrap: wrap; gap: 4px; width: 100%; justify-content: flex-end; }
.top .langs a { color: var(--faint); font-size: 13px; font-weight: 700; letter-spacing: .4px; padding: 3px 8px; border: 1px solid var(--border); border-radius: 8px; }
.top .langs a[aria-current] { color: var(--text); border-color: var(--accent); background: var(--panel2); }
.translated { font-size: 15px; }
html.swap #page { visibility: hidden; }
h1 { font-size: clamp(26px, 5vw, 36px); line-height: 1.15; margin: 0 0 8px; text-wrap: balance; }
.date { color: var(--faint); margin: 0 0 24px; font-size: 15px; }
h2 { font-size: 21px; line-height: 1.3; margin: 40px 0 10px; scroll-margin-top: 16px; }
h3 { font-size: 17px; margin: 22px 0 6px; color: var(--text); }
p, li, td { color: var(--dim); }
p b, li b, td b, p strong { color: var(--text); }
ul, ol { padding-left: 22px; }
li { margin: 4px 0; }
.box { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 14px 20px; margin: 16px 0; }
.box p { margin: 6px 0; }
.box.key { border-color: #5b4a99; background: var(--panel2); }
.toc { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 12px 20px; margin: 20px 0 8px; font-size: 15px; }
.toc b { display: block; margin-bottom: 4px; }
.toc ol { margin: 0; padding-left: 22px; columns: 2 260px; column-gap: 28px; }
.toc li { margin: 2px 0; break-inside: avoid; }
.toc a { text-decoration: none; }
.tablewrap { margin: 14px 0; }
table { width: 100%; border-collapse: collapse; font-size: 15px; line-height: 1.5; }
th, td { text-align: left; vertical-align: top; padding: 9px 10px; border-bottom: 1px solid var(--border); }
th { color: var(--text); background: var(--panel); font-weight: 700; }
.todo { background: rgba(245, 197, 24, .15); color: var(--todo); border-radius: 6px; padding: 1px 6px; font-weight: 700; }
.check { background: rgba(127, 212, 255, .13); color: var(--check); border-radius: 6px; padding: 1px 6px; font-weight: 700; }
.form { background: var(--panel); border: 1px dashed var(--border); border-radius: 12px; padding: 12px 18px; }
.foot { margin-top: 56px; padding-top: 22px; border-top: 1px solid var(--border); color: var(--faint); font-size: 14px; }
.foot nav { display: flex; flex-wrap: wrap; gap: 6px 16px; margin-bottom: 12px; }
.foot nav a { color: var(--dim); }
.foot p { color: var(--faint); margin: 6px 0; }
@media (max-width: 600px) {
  body { font-size: 16px; padding-top: 18px; }
  h2 { font-size: 19px; }
  .top .home { width: 100%; }
  .langs { justify-content: flex-start; }
  /* Tableaux en fiches empilées : chaque cellule porte le nom de sa colonne. */
  table, thead, tbody, tr, th, td { display: block; }
  thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  tr { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; margin: 10px 0; padding: 4px 12px; }
  td { border: 0; padding: 6px 0; }
  td + td { border-top: 1px solid var(--border); }
  td[data-label]::before { content: attr(data-label); display: block; color: var(--text); font-weight: 700; font-size: 13px; }
}
@media print {
  :root { color-scheme: light; --bg: #fff; --panel: #f4f4f8; --panel2: #f4f4f8; --border: #ccc; --text: #000; --dim: #222; --faint: #444; --accent: #2a2a8a; }
  body { padding: 0; }
  .top, .toc, .langs { display: none; }
}
"""


def label_tables(html: str) -> str:
    """Donne à chaque cellule le nom de sa colonne (affiché en fiche sur petit écran)."""
    def one(m):
        table = m.group(0)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)]
        def row(r):
            i = [0]
            def cell(c):
                k = i[0]; i[0] += 1
                lab = heads[k] if k < len(heads) else ""
                return f'<td data-label="{lab}"' if lab else "<td"
            return re.sub(r"<td(?=[\s>])", cell, r.group(0))
        body = re.sub(r"<tr>.*?</tr>", row, table.split("</thead>", 1)[1], flags=re.S)
        return '<div class="tablewrap">' + table.split("</thead>", 1)[0] + "</thead>" + body + "</div>"
    return re.sub(r"<table>.*?</table>", one, html, flags=re.S)



def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def with_lang(html: str, lang: str) -> str:
    """Les liens vers les autres pages du site gardent la langue affichée : ../cgv/#x → ../cgv/?lang=xx#x."""
    return re.sub(r'href="\.\./([^"#?]*)(#[^"]*)?"', lambda m: f'href="../{m.group(1)}?lang={lang}{m.group(2) or ""}"', html)


def version(slug: str, lang: str):
    """Une version complète (menu, sélecteur de langue, texte, pied) de la page dans une langue."""
    src = SRC / (f"{slug}.html" if lang == "fr" else f"{slug}.{lang}.html")
    title, desc, body = src.read_text(encoding="utf-8").split("\n", 2)
    ui = UI[lang]
    names = dict(zip(PAGES, ui["names"]))
    top = " ".join(f'<a href="../{s}/"' + (' aria-current="page"' if s == slug else "") + f">{names[s]}</a>" for s in PAGES)
    langs = " ".join(
        f'<a href="?lang={l}" hreflang="{l}" lang="{l}" data-setlang="{l}"' + (' aria-current="true"' if l == lang else "") + f">{l.upper()}</a>"
        for l in LANGS
    )
    foot = " ".join(f'<a href="../{s}/">{names[s]}</a>' for s in PAGES)
    notice = ""
    if ui["notice"]:
        notice = f'<p class="box translated" lang="{lang}">{ui["notice"]} <a href="?lang=fr" hreflang="fr" lang="fr">{ui["readfr"]}</a></p>\n'
    html = f"""<nav class="top" aria-label="{ui['nav']}"><a class="home" href="../">‹ Graal – IPTV Player</a> {top}
<span class="langs" role="group" aria-label="{ui['lang']}">{langs}</span></nav>
<main>
{notice}{label_tables(body).strip()}
</main>
<footer class="foot">
  <nav aria-label="{ui['nav']}">{foot}</nav>
  <p>{ui['legal']}</p>
  <p>{ui['contact']} : <a href="mailto:contact@graaltv.com">contact@graaltv.com</a> · © 2026 Graal</p>
</footer>"""
    if lang != "fr":
        html = html.replace(f"{ui['contact']} : ", f"{ui['contact']}: ")
    return title, desc, with_lang(html, lang)


SCRIPT = """
// Shows the version in the visitor's language (see ../lang.js); French stays in the page for readers without JavaScript.
(function () {
  var root = document.documentElement, lang = root.lang;
  var tpl = lang !== 'fr' && document.querySelector('template[data-lang="' + lang + '"]');
  if (tpl) {
    var page = document.getElementById('page');
    page.replaceChildren(tpl.content.cloneNode(true));
    document.title = tpl.dataset.title;
    document.querySelector('meta[name="description"]').content = tpl.dataset.desc;
  } else root.lang = 'fr';
  root.classList.remove('swap');
  var target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (tpl && target) target.scrollIntoView();
})();
"""

for slug in PAGES:
    title, desc, fr = version(slug, "fr")
    templates = []
    for lang in LANGS[1:]:
        t, d, html = version(slug, lang)
        templates.append(f'<template data-lang="{lang}" data-title="{esc(t)}" data-desc="{esc(d)}">\n{html}\n</template>')
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{CSS}</style>
<script src="../lang.js"></script>
<script>(function () {{ var l = window.GraalLang ? GraalLang.pick() : 'fr'; document.documentElement.lang = l; if (l !== 'fr') document.documentElement.classList.add('swap'); }})();</script>
</head>
<body>
<div id="page">
{fr}
</div>
{chr(10).join(templates)}
<script>{SCRIPT}</script>
</body>
</html>
"""
    (OUT / slug).mkdir(parents=True, exist_ok=True)
    (OUT / slug / "index.html").write_text(page, encoding="utf-8")
    print("ok", slug)
