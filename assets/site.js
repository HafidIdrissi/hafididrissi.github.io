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

// Print every experience, then restore the reader's selected view.
let printState;
window.addEventListener('beforeprint', () => {
  printState = items.map(item => ({ hidden: item.hidden, open: item.querySelector('details').open }));
  items.forEach(item => { item.hidden = false; item.querySelector('details').open = true; });
});
window.addEventListener('afterprint', () => {
  if (!printState) return;
  items.forEach((item, index) => { item.hidden = printState[index].hidden; item.querySelector('details').open = printState[index].open; });
  printState = undefined;
});
