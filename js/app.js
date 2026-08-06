const LANGS = Object.keys(TRANSLATIONS);
const PHOTOS = ['assets/hero.webp', 'assets/hero.jpg', 'assets/hero.png'];

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

  const photo = document.getElementById('photo');
  if (photo && !photo.hidden) photo.alt = dict['a11y.photo'];

  document.querySelectorAll('[data-lang]').forEach(btn => {
    btn.setAttribute('aria-pressed', btn.dataset.lang === lang);
  });
}

function loadPhoto(el, sources) {
  if (!sources.length) return;

  const [src, ...rest] = sources;
  const probe = new Image();
  probe.src = src;
  probe.onload = () => {
    el.src = src;
    el.alt = TRANSLATIONS[document.documentElement.lang]['a11y.photo'];
    el.hidden = false;
    document.body.classList.add('has-photo');
  };
  probe.onerror = () => loadPhoto(el, rest);
}

document.querySelectorAll('[data-lang]').forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.lang));
});

setLang(document.documentElement.lang);

const photo = document.getElementById('photo');
if (photo) loadPhoto(photo, PHOTOS);
