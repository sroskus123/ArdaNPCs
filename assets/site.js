(() => {
  'use strict';
  const ui = JSON.parse(document.getElementById('ui-data').textContent);
  const search = document.getElementById('search');
  const results = document.getElementById('search-results');
  const links = document.getElementById('search-links');
  const status = document.getElementById('search-status');
  let searchIndex, generation = 0;
  const normal = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  async function showSearch() {
    const turn = ++generation;
    const query = normal(search.value.trim());
    if (!query) { results.hidden = true; return; }
    try {
      searchIndex ??= fetch('search-index.json').then(response => {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      });
      const entries = await searchIndex;
      if (turn !== generation) return;
      const words = query.split(/\s+/);
      const matches = entries.map(entry => {
        const title = normal(entry.title), text = normal(entry.page + ' ' + entry.text);
        return { entry, score: words.every(word => (title + ' ' + text).includes(word)) ? words.reduce((score, word) => score + (title.includes(word) ? 10 : 1), 0) : 0 };
      }).filter(item => item.score).sort((a, b) => b.score - a.score).slice(0, 12);
      links.replaceChildren();
      status.textContent = matches.length ? `${ui.results} · ${matches.length}` : ui.empty;
      matches.forEach(({entry}) => {
        const link = document.createElement('a'); link.href = entry.url;
        const title = document.createElement('strong'); title.textContent = entry.title;
        const page = document.createElement('small'); page.textContent = entry.page;
        const excerpt = document.createElement('p');
        const at = normal(entry.text).indexOf(words[0]);
        const start = Math.max(0, at - 45);
        excerpt.textContent = (start ? '…' : '') + entry.text.slice(start, start + 160) + (entry.text.length > start + 160 ? '…' : '');
        link.append(page, title, excerpt); links.append(link);
      });
      results.hidden = false;
    } catch {
      searchIndex = undefined;
      if (turn !== generation) return;
      links.replaceChildren();
      status.textContent = document.documentElement.lang === 'cs' ? 'Hledání se nepodařilo načíst. Kapitoly jsou dostupné v navigaci.' : 'Search could not load. Use the chapter navigation.';
      results.hidden = false;
    }
  }
  search.addEventListener('input', showSearch);
  search.addEventListener('focus', () => { if (search.value.trim()) showSearch(); });
  search.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' && !results.hidden) { event.preventDefault(); links.querySelector('a')?.focus(); }
  });
  document.getElementById('close-search').addEventListener('click', () => { generation++; results.hidden = true; search.value = ''; search.focus(); });
  document.addEventListener('click', event => { if (!event.target.closest('.search-wrap')) { generation++; results.hidden = true; } });
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !event.ctrlKey && !event.metaKey && !['INPUT','TEXTAREA'].includes(event.target.tagName) && !event.target.isContentEditable) { event.preventDefault(); search.focus(); }
    if (event.key === 'Escape') { generation++; results.hidden = true; document.getElementById('sidebar').classList.remove('open'); document.querySelector('.mobile-menu').setAttribute('aria-expanded', 'false'); search.blur(); }
  });
  document.querySelector('.mobile-menu').addEventListener('click', event => {
    const open = document.getElementById('sidebar').classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('.prose pre').forEach(pre => {
    const wrapper = document.createElement('div'); wrapper.className = 'code-wrap';
    pre.before(wrapper); wrapper.append(pre);
    const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-code'; button.textContent = ui.copy;
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(pre.textContent.trim()); button.textContent = ui.copied; }
      catch { const range = document.createRange(); range.selectNodeContents(pre); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); button.textContent = ui.selected; }
      setTimeout(() => { button.textContent = ui.copy; }, 2200);
    });
    wrapper.append(button);
  });
})();
