// Small enhancements only. All content is visible without this file.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  // Menu on narrow screens (DESIGN.md section 7): the three-line button turns into a cross; the page behind is dimmed.
  // Escape, a click on the dimmed page, or choosing an item closes it.
  if (toggle && nav) {
    var scrim = null;
    var setOpen = function (open) {
      nav.classList.toggle('open', open);
      document.documentElement.classList.toggle('menu-open', open);
      var header = document.querySelector('.site-header');
      if (header) document.documentElement.style.setProperty('--nav-top', header.getBoundingClientRect().bottom + 'px');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open && !scrim) {
        scrim = document.createElement('div');
        scrim.className = 'nav-scrim';
        scrim.addEventListener('click', function () { setOpen(false); });
        document.body.appendChild(scrim);
      } else if (!open && scrim) {
        scrim.remove();
        scrim = null;
      }
    };
    toggle.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1000 && nav.classList.contains('open')) { setOpen(false); } });
  }

  // Filters: buttons with data-filter act on elements with data-tags inside the same [data-filter-scope]
  document.querySelectorAll('[data-filter-scope]').forEach(function (scope) {
    var buttons = scope.querySelectorAll('.filters button');
    var targets = scope.querySelectorAll('[data-tags]');
    var groups = scope.querySelectorAll('[data-group]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = btn.getAttribute('data-filter');
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
        targets.forEach(function (t) {
          var tags = t.getAttribute('data-tags').split(' ');
          t.hidden = !(f === 'all' || tags.indexOf(f) !== -1);
        });
        groups.forEach(function (g) {
          g.hidden = !g.querySelector('[data-tags]:not([hidden])');
        });
        var status = scope.querySelector('[data-count]');
        if (status) {
          status.textContent = scope.querySelectorAll('[data-tags]:not([hidden])').length + ' shown';
        }
      });
    });
  });
})();
