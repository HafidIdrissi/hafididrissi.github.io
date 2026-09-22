/* Progressive enhancement: the complete portfolio is readable without JavaScript. */
const root = document.documentElement;
const themeButton = document.getElementById('theme');
const currentTheme = () => root.dataset.theme || 'dark';
function updateThemeLabel() {
  themeButton.setAttribute('aria-label', `Switch to ${currentTheme() === 'dark' ? 'light' : 'dark'} theme`);
  document.querySelector('meta[name="theme-color"]').content = currentTheme() === 'dark' ? '#101313' : '#f5f5ef';
}
themeButton.hidden = false;
updateThemeLabel();
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

// A deliberate selection, with no timer or automatic carousel to interrupt reading.
const previews = {
  pdf: { image: 'goeditpdf.jpg', name: 'GoEditPDF', domain: 'goeditpdf.com', url: 'https://goeditpdf.com/', description: 'Browser-based PDF editing & local OCR', tag: 'Your documents. Your device.', alt: 'Explore GoEditPDF: the browser-based editor with a synthetic sample document.' },
  persona: { image: 'persona.jpg', name: 'Influence Persona', domain: 'influencepersona.com', url: 'https://influencepersona.com/', description: 'An AI content studio, built end to end', tag: 'From concept to content.', alt: 'Explore Influence Persona: its public product page with AI avatar examples.' },
  tracker: { image: 'tracker.jpg', name: 'Local Time Tracker', domain: 'github.com / Time-Tracker', url: 'https://github.com/HafidIdrissi/Time-Tracker', description: 'Automatic activity tracking. Local data.', tag: 'Local data. Offline reports.', alt: 'Explore Local Time Tracker: the desktop dashboard with repository sample data.' }
};
const switcher = document.querySelector('.product-switcher');
const previewImage = document.getElementById('preview-image');
const previewLink = document.getElementById('hero-preview');
switcher.hidden = false;
let selectionVersion = 0;
switcher.addEventListener('click', async event => {
  const button = event.target.closest('button[data-preview]');
  if (!button) return;
  const version = ++selectionVersion;
  if (button.getAttribute('aria-pressed') === 'true') return;
  const product = previews[button.dataset.preview];
  const preload = new Image();
  preload.src = `assets/products/${product.image}`;
  try { await preload.decode(); } catch (_) { return; }
  if (version !== selectionVersion) return;
  previewImage.src = preload.src;
  previewImage.alt = product.alt;
  previewLink.href = product.url;
  document.getElementById('preview-domain').textContent = product.domain;
  document.getElementById('preview-caption').replaceChildren(
    Object.assign(document.createElement('strong'), { textContent: product.name }),
    Object.assign(document.createElement('span'), { textContent: product.description })
  );
  document.getElementById('preview-tag').lastChild.textContent = ` ${product.tag}`;
  document.querySelector('.product-deck').dataset.product = button.dataset.preview;
  switcher.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  if (motionEnabled()) previewImage.animate([{ opacity: .35, transform: 'scale(1.025)' }, { opacity: 1, transform: 'scale(1)' }], { duration: 420, easing: 'ease-out' });
});

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
