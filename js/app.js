const LANGS = Object.keys(TRANSLATIONS);
const PHOTOS = ['assets/hero.webp', 'assets/hero.jpg', 'assets/hero.png'];

// While this is empty the page says the form opens shortly, so the invitation
// never points at a dead button.
const FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLScUxx5KTN_eaxWu33RxOMcEGtIRdr17SSTnGjAzjFXcJHi9lA/viewform';

function setLang(lang) {
  if (!LANGS.includes(lang)) lang = 'en';
  const dict = TRANSLATIONS[lang];

  document.documentElement.lang = lang;
  localStorage.setItem('lang', lang);

  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = dict[el.dataset.i18n] ?? el.textContent;
  });

  document.querySelectorAll('[data-i18n-attr]').forEach(el => {
    for (const pair of el.dataset.i18nAttr.split(',')) {
      const [attr, key] = pair.split(':');
      if (dict[key]) el.setAttribute(attr, dict[key]);
    }
  });

  document.querySelectorAll('[data-lang]').forEach(btn => {
    btn.setAttribute('aria-pressed', btn.dataset.lang === lang);
  });
}

// Shows the first source that actually exists, so a missing file just leaves
// the slot empty instead of a broken image.
function loadImage(el, sources, done) {
  if (!el || !sources.length) return;

  const [src, ...rest] = sources;
  const probe = new Image();
  probe.src = src;
  probe.onload = () => {
    el.src = src;
    el.hidden = false;
    if (done) done();
  };
  probe.onerror = () => loadImage(el, rest, done);
}

document.querySelectorAll('[data-lang]').forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.lang));
});

setLang(document.documentElement.lang);

loadImage(document.getElementById('photo'), PHOTOS,
  () => document.body.classList.add('has-photo'));

const form = document.getElementById('form');
if (form && FORM_URL) {
  form.href = FORM_URL;
  form.hidden = false;
  document.getElementById('form-soon').hidden = true;
}
