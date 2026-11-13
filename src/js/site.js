// Small enhancements only. All content is visible without this file.
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
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
