// Language of graaltv.com, the same on every page: ?lang= in the address, else the visitor's choice kept in the browser
// (localStorage "graal-lang"), else the browser's language, else French. A link with data-setlang="xx" keeps that choice.
(function () {
  var LANGS = ['fr', 'en', 'es', 'it', 'pt', 'de'];
  function known(l) { l = String(l || '').slice(0, 2).toLowerCase(); return LANGS.indexOf(l) >= 0 ? l : null; }
  function saved() { try { return localStorage.getItem('graal-lang'); } catch (e) { return null; } }
  function save(l) { if (known(l)) { try { localStorage.setItem('graal-lang', known(l)); } catch (e) {} } }
  function pick() {
    var fromUrl = null;
    try { fromUrl = new URLSearchParams(location.search).get('lang'); } catch (e) {}
    return known(fromUrl) || known(saved()) || known(navigator.language) || 'fr';
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('[data-setlang]');
    if (a) save(a.getAttribute('data-setlang'));
  });
  window.GraalLang = { LANGS: LANGS, pick: pick, save: save };
})();
