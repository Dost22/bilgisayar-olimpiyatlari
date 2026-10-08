/* ==========================================================================
   Sekme yönlendirmesi (hash tabanlı) + küçük yardımcılar.
   Bağımlılık yok; çerçevesiz (framework-free) çalışır.
   ========================================================================== */
(function () {
  'use strict';

  var DEFAULT_TAB = 'genel-bakis';
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  var panels = {};

  tabs.forEach(function (tab) {
    panels[tab.dataset.panel] = document.getElementById('panel-' + tab.dataset.panel);
  });

  function activate(name, silent) {
    if (!panels[name]) { name = DEFAULT_TAB; }

    tabs.forEach(function (tab) {
      var isOn = tab.dataset.panel === name;
      tab.setAttribute('aria-selected', isOn ? 'true' : 'false');
      tab.setAttribute('tabindex', isOn ? '0' : '-1');
      var panel = panels[tab.dataset.panel];
      panel.classList.toggle('is-active', isOn);
      if (isOn) { panel.removeAttribute('hidden'); } else { panel.setAttribute('hidden', ''); }
    });

    if (!silent) {
      window.scrollTo({ top: 0, behavior: 'auto' });
    }
  }

  function fromHash() {
    var name = (window.location.hash || '').replace(/^#/, '');
    return name || DEFAULT_TAB;
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var name = tab.dataset.panel;
      if (fromHash() === name) { activate(name); } else { window.location.hash = name; }
    });

    tab.addEventListener('keydown', function (ev) {
      var i = tabs.indexOf(tab);
      var next = null;
      if (ev.key === 'ArrowRight') { next = tabs[(i + 1) % tabs.length]; }
      else if (ev.key === 'ArrowLeft') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
      else if (ev.key === 'Home') { next = tabs[0]; }
      else if (ev.key === 'End') { next = tabs[tabs.length - 1]; }
      if (next) { ev.preventDefault(); next.focus(); next.click(); }
    });
  });

  /* Sayfa içi bağlantılar (ör. "İçindekilere göz at") sekme değiştirsin. */
  document.addEventListener('click', function (ev) {
    var link = ev.target.closest ? ev.target.closest('a[href^="#"]') : null;
    if (!link) { return; }
    var name = link.getAttribute('href').slice(1);
    if (panels[name]) {
      ev.preventDefault();
      if (fromHash() === name) { activate(name); } else { window.location.hash = name; }
    }
  });

  window.addEventListener('hashchange', function () { activate(fromHash()); });

  /* İletişim: adresi panoya kopyala. */
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest ? ev.target.closest('[data-copy]') : null;
    if (!btn) { return; }
    var value = btn.getAttribute('data-copy');
    var done = function () {
      var old = btn.textContent;
      btn.textContent = 'Kopyalandı ✓';
      setTimeout(function () { btn.textContent = old; }, 1800);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(done, function () {});
    } else {
      var input = document.createElement('textarea');
      input.value = value;
      document.body.appendChild(input);
      input.select();
      try { document.execCommand('copy'); done(); } catch (e) {}
      document.body.removeChild(input);
    }
  });

  /* Sayfa, belirli bir sekmeye bağlantıyla açıldıysa içindekiler
     kısımlarını açık başlatmak için: #icindekiler → ilk kısım açık. */
  if (fromHash() === 'icindekiler') {
    var firstPart = document.querySelector('.toc-part');
    if (firstPart) { firstPart.open = true; }
  }

  activate(fromHash(), true);
})();