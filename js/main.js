// Small progressive enhancements. The site works without JavaScript.
document.documentElement.classList.remove('no-js');

// Header background once the page scrolls
const header = document.querySelector('.site-header');
const onScroll = () => header && header.classList.toggle('scrolled', window.scrollY > 40);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Fade/slide sections in as they enter the screen
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('in'));
}

// Chapter rail: highlight the chapter you're reading and fill the progress line
const rail = document.querySelector('.rail');
if (rail) {
  const items = [...rail.querySelectorAll('li')];
  const chapters = items.map((li) => document.querySelector(li.querySelector('a').getAttribute('href')));
  const progress = rail.querySelector('.progress');
  const update = () => {
    const mid = window.innerHeight * 0.35;
    let idx = 0;
    chapters.forEach((c, i) => { if (c && c.getBoundingClientRect().top < mid) idx = i; });
    items.forEach((li, i) => { li.classList.toggle('active', i === idx); li.classList.toggle('done', i < idx); });
    if (progress && items[idx]) progress.style.height = items[idx].offsetTop + 'px';
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
}

// Gentle parallax on the workbench band
const band = document.querySelector('.band img');
if (band && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const par = () => {
    const r = band.parentElement.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
    band.style.transform = `translateY(${p * -8}%)`;
  };
  window.addEventListener('scroll', par, { passive: true });
  par();
}

// Click-to-play YouTube (doesn't load YouTube until clicked)
document.querySelectorAll('.video button[data-yt]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${btn.dataset.yt}?autoplay=1&rel=0`;
    f.title = btn.getAttribute('aria-label') || 'Video';
    f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    btn.replaceWith(f);
  });
});

// Lightbox for gallery images
const figs = [...document.querySelectorAll('.gallery figure')];
if (figs.length) {
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.innerHTML = '<button class="close" aria-label="Close">×</button><button class="prev" aria-label="Previous">‹</button><img alt=""><button class="nextb" aria-label="Next">›</button><div class="cap mono"></div>';
  document.body.appendChild(lb);
  const img = lb.querySelector('img');
  const cap = lb.querySelector('.cap');
  let cur = 0;
  const show = (i) => {
    cur = (i + figs.length) % figs.length;
    const src = figs[cur].querySelector('img');
    img.src = src.currentSrc || src.src;
    img.alt = src.alt;
    cap.textContent = figs[cur].querySelector('figcaption')?.textContent || '';
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  };
  const close = () => { lb.classList.remove('open'); document.body.style.overflow = ''; figs[cur].focus(); };
  figs.forEach((f, i) => {
    f.tabIndex = 0;
    f.addEventListener('click', () => show(i));
    f.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(i); } });
  });
  lb.querySelector('.close').onclick = close;
  lb.querySelector('.prev').onclick = (e) => { e.stopPropagation(); show(cur - 1); };
  lb.querySelector('.nextb').onclick = (e) => { e.stopPropagation(); show(cur + 1); };
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });
}

// Justified galleries: pack photos into rows of equal height that fill the width.
// The last row keeps the target height instead of stretching.
const galleries = document.querySelectorAll('.gallery');
const layoutGallery = (g) => {
  const figs = [...g.querySelectorAll('figure')];
  const W = g.clientWidth;
  if (!W || !figs.length) return;
  const gap = parseFloat(getComputedStyle(g).columnGap) || 0;
  const rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
  const single = g.classList.contains('single');
  // A lone photo fills its column inside a two-column split, but is capped elsewhere
  const target = single ? (g.closest('.split') ? Infinity : (W < 600 ? 22 * rem : 32 * rem)) : (W < 600 ? 9 * rem : 15 * rem);
  let row = [], sum = 0;
  const place = (items, h) => items.forEach(([f, r]) => { f.style.width = (r * h) + 'px'; });
  figs.forEach((f) => {
    const r = parseFloat(f.style.getPropertyValue('--r')) || 1;
    row.push([f, r]); sum += r;
    const gaps = gap * (row.length - 1);
    if (sum * target + gaps >= W) { place(row, (W - gaps) / sum); row = []; sum = 0; }
  });
  if (row.length) {
    const gaps = gap * (row.length - 1);
    place(row, Math.min(target, (W - gaps) / sum));
  }
  g.classList.add('js');
};
if (galleries.length && 'ResizeObserver' in window) {
  const ro = new ResizeObserver((entries) => entries.forEach((e) => layoutGallery(e.target)));
  galleries.forEach((g) => ro.observe(g));
}
