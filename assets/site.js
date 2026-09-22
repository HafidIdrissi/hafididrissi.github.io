/* Progressive enhancement: the complete portfolio is readable without JavaScript. */
const root = document.documentElement;
const themeButton = document.getElementById('theme');
const systemTheme = matchMedia('(prefers-color-scheme: dark)');
const currentTheme = () => root.dataset.theme || (systemTheme.matches ? 'dark' : 'light');
function updateThemeLabel() {
  themeButton.setAttribute('aria-label', `Switch to ${currentTheme() === 'dark' ? 'light' : 'dark'} theme`);
  document.querySelector('meta[name="theme-color"]').content = currentTheme() === 'dark' ? '#141c19' : '#f6f5f0';
}
themeButton.hidden = false;
updateThemeLabel();
systemTheme.addEventListener('change', updateThemeLabel);
themeButton.addEventListener('click', () => {
  root.dataset.theme = currentTheme() === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('hi-theme', root.dataset.theme); } catch (_) {}
  updateThemeLabel();
});

const items = [...document.querySelectorAll('.xp')];
const filters = document.getElementById('filters');
function applyFilter(key) {
  let shown = 0;
  items.forEach(item => {
    const visible = key === 'all' || (key === 'star' ? item.dataset.star === '1' : item.dataset.group === key);
    item.hidden = !visible;
    if (visible) shown++;
  });
  document.getElementById('xpcount').textContent = `${shown} / ${items.length}`;
  filters.querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.f === key)));
}
filters.hidden = false;
applyFilter('star');
filters.addEventListener('click', event => {
  const button = event.target.closest('button[data-f]');
  if (button) applyFilter(button.dataset.f);
});

// Direct links reveal entries even when a different filter is selected.
function revealExperience(hash, scroll = true) {
  if (!hash.startsWith('#xp-')) return;
  const entry = document.getElementById(hash.slice(1));
  if (!entry || !entry.classList.contains('xp')) return;
  if (entry.hidden) applyFilter('all');
  entry.querySelector('details').open = true;
  if (scroll) entry.scrollIntoView({ block: 'start' });
}
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#xp-"]');
  if (link) revealExperience(link.getAttribute('href'), false);
});
window.addEventListener('hashchange', () => revealExperience(location.hash));
revealExperience(location.hash);

// Motion preferences apply to CSS, pointer interactions and scroll entrances.
const motionButton = document.getElementById('motion');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let manualPause = root.dataset.motion === 'paused';
const motionEnabled = () => !manualPause && !reducedMotion.matches;
function updateMotion() {
  const paused = !motionEnabled();
  root.dataset.motion = paused ? 'paused' : 'running';
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.disabled = reducedMotion.matches;
  const label = reducedMotion.matches ? 'Animations disabled by your system preference' : paused ? 'Play animations' : 'Pause animations';
  motionButton.setAttribute('aria-label', label);
  motionButton.title = label;
  if (paused) document.getAnimations().forEach(animation => animation.cancel());
}
motionButton.hidden = false;
updateMotion();
motionButton.addEventListener('click', () => {
  manualPause = !manualPause;
  try { localStorage.setItem('hi-motion', manualPause ? 'paused' : 'running'); } catch (_) {}
  updateMotion();
});
reducedMotion.addEventListener('change', updateMotion);

// Elements remain visible if JavaScript or the observer is unavailable.
if ('IntersectionObserver' in window) {
  const entrances = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      if (motionEnabled()) {
        entry.target.animate([
          { opacity: 0, transform: 'translateY(20px)' },
          { opacity: 1, transform: 'translateY(0)' }
        ], { duration: 650, delay: Number(entry.target.dataset.stagger || 0), easing: 'cubic-bezier(.2,.7,.3,1)' });
      }
      entrances.unobserve(entry.target);
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section-heading,.work-card,.xp,.repo,.skills-grid article,.education').forEach((element, index) => {
    element.dataset.stagger = String((index % 3) * 65);
    entrances.observe(element);
  });
}

let progressPending = false;
function updateProgress() {
  const distance = document.documentElement.scrollHeight - innerHeight;
  root.style.setProperty('--progress', String(distance > 0 ? Math.min(1, Math.max(0, scrollY / distance)) : 0));
  progressPending = false;
}
window.addEventListener('scroll', () => {
  if (!progressPending) { progressPending = true; requestAnimationFrame(updateProgress); }
}, { passive: true });
window.addEventListener('resize', updateProgress);
document.addEventListener('toggle', updateProgress, true);
updateProgress();

const systemCard = document.querySelector('.system-card');
systemCard.addEventListener('pointermove', event => {
  if (!motionEnabled() || event.pointerType !== 'mouse') return;
  const box = systemCard.getBoundingClientRect();
  systemCard.style.setProperty('--tilt-y', `${((event.clientX - box.left) / box.width - .5) * 6}deg`);
  systemCard.style.setProperty('--tilt-x', `${((event.clientY - box.top) / box.height - .5) * -4}deg`);
});
systemCard.addEventListener('pointerleave', () => {
  systemCard.style.removeProperty('--tilt-x');
  systemCard.style.removeProperty('--tilt-y');
});
document.addEventListener('visibilitychange', () => { root.dataset.suspended = String(document.hidden); });

// Print every experience and case study, then restore the reader's view.
let printState;
window.addEventListener('beforeprint', () => {
  if (printState) return;
  printState = { items: items.map(item => ({ hidden: item.hidden, open: item.querySelector('details').open })), cases: [...document.querySelectorAll('.case-study')].map(detail => detail.open) };
  items.forEach(item => { item.hidden = false; item.querySelector('details').open = true; });
  document.querySelectorAll('.case-study').forEach(detail => { detail.open = true; });
});
window.addEventListener('afterprint', () => {
  if (!printState) return;
  items.forEach((item, index) => { item.hidden = printState.items[index].hidden; item.querySelector('details').open = printState.items[index].open; });
  document.querySelectorAll('.case-study').forEach((detail, index) => { detail.open = printState.cases[index]; });
  printState = undefined;
});
