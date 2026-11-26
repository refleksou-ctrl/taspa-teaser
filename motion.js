// Scroll reveals: elements fade up once as they enter; plates stagger.
// Reduced motion: same reveals, opacity only (CSS removes the movement).
// Without JS everything is simply visible.
(() => {
  const targets = ['.services h2', '.services .sublead', '.plates li', '.concept__text', '.smark', '.news__text', '.news .form', '.loc__info', '.loc__card', '.contact__col', '.footer__row'];
  const els = [...document.querySelectorAll(targets.join(','))];
  document.querySelectorAll('.plates li').forEach((li, i) => li.style.setProperty('--i', i % 4 + Math.floor(i / 4)));
  els.forEach(el => el.setAttribute('data-reveal', ''));
  if (!('IntersectionObserver' in window)) { els.forEach(el => el.classList.add('is-in')); return; }

  const io = new IntersectionObserver(entries => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
  els.forEach(el => io.observe(el));

  // Fast scrolls / anchor jumps can skip an element without it ever intersecting:
  // reveal anything already above the fold line.
  let ticking = false;
  const sweep = () => {
    ticking = false;
    for (const el of els) if (!el.classList.contains('is-in') && el.getBoundingClientRect().top < innerHeight) { el.classList.add('is-in'); io.unobserve(el); }
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(sweep); } }, { passive: true });

  // Endless loops (name band, sauna steam) pause while off-screen.
  const loops = new IntersectionObserver(entries => {
    for (const e of entries) e.target.classList.toggle('is-offscreen', !e.isIntersecting);
  });
  document.querySelectorAll('.band, .signset').forEach(el => loops.observe(el));
})();
