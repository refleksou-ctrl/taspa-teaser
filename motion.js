// Scroll reveals. Elements fade up once as they enter; plates stagger.
// Without JS (or with reduced motion) everything is simply visible.
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const targets = [
    '.services h2', '.services .sublead', '.plates li',
    '.concept__text', '.smark',
    '.signset', '.sauna__text',
    '.footer__row'
  ];
  const els = document.querySelectorAll(targets.join(','));
  document.querySelectorAll('.plates li').forEach((li, i) => li.style.setProperty('--i', i % 4 + Math.floor(i / 4)));
  els.forEach(el => el.setAttribute('data-reveal', ''));
  if (reduce || !('IntersectionObserver' in window)) { els.forEach(el => el.classList.add('is-in')); return; }
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
})();
