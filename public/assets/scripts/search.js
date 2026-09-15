// Native module: Pagefind is generated after Astro's build and loaded only on request.
const form = document.querySelector('#site-search');
const query = document.querySelector('#search-query');
const agency = document.querySelector('#search-agency');
const section = document.querySelector('#search-section');
const documentType = document.querySelector('#search-type');
const status = document.querySelector('#search-status');
const list = document.querySelector('#search-results');
const pagination = document.querySelector('#search-pagination');
const initial = new URLSearchParams(location.search);
query.value = initial.get('q') || '';
let enginePromise, request = 0, timer;

function loadEngine() {
  if (!enginePromise) enginePromise = import('/pagefind/pagefind.js').then(async engine => {
    const filters = await engine.filters();
    for (const [key, select] of [['Agency', agency], ['Section', section], ['Document type', documentType]]) {
      while (select.options.length > 1) select.remove(1);
      for (const value of Object.keys(filters[key] || {}).sort()) {
        const option = document.createElement('option');
        option.value = value; option.textContent = value; select.append(option);
      }
    }
    agency.value = initial.get('agency') || '';
    section.value = initial.get('section') || '';
    documentType.value = initial.get('type') || '';
    document.querySelector('#search-filters').hidden = false;
    return engine;
  });
  return enginePromise;
}

async function search(page = 0) {
  const current = ++request, term = query.value.trim();
  if (!term) {
    list.replaceChildren(); pagination.replaceChildren();
    status.textContent = 'Enter a term, or browse the document library below.';
    history.replaceState(null, '', location.pathname); return;
  }
  status.textContent = 'Searching the public record…';
  try {
    const engine = await loadEngine(), filters = {};
    if (agency.value) filters.Agency = agency.value;
    if (section.value) filters.Section = section.value;
    if (documentType.value) filters['Document type'] = documentType.value;
    const result = await engine.search(term, {filters});
    const results = await Promise.all(result.results.slice(page * 10, page * 10 + 10).map(r => r.data()));
    if (current !== request) return;
    list.replaceChildren();
    for (const result of results) {
      const item = document.createElement('li'), heading = document.createElement('h2');
      const link = document.createElement('a'), excerpt = document.createElement('p');
      link.href = result.url; link.textContent = result.meta.title || result.url;
      heading.append(link);
      // Pagefind escapes source text and adds only its own highlighting markup.
      excerpt.innerHTML = result.excerpt;
      item.append(heading, excerpt); list.append(item);
    }
    status.textContent = result.results.length
      ? `${result.results.length} result${result.results.length===1?'':'s'} for “${term}”. Showing ${page * 10 + 1}–${Math.min(page * 10 + 10, result.results.length)}.`
      : `No results for “${term}”. Try fewer words or reset the filters.`;
    pagination.replaceChildren();
    for (const [label, next] of [['Previous', page - 1], ['Next', page + 1]]) {
      if (next < 0 || next * 10 >= result.results.length) continue;
      const button = document.createElement('button'); button.textContent = label;
      button.addEventListener('click', () => search(next)); pagination.append(button);
    }
    const params = new URLSearchParams({q: term});
    if (agency.value) params.set('agency', agency.value);
    if (section.value) params.set('section', section.value);
    if (documentType.value) params.set('type', documentType.value);
    history.replaceState(null, '', `${location.pathname}?${params}`);
  } catch {
    if (current === request) {
      status.textContent = 'Search could not load. Browse the document library below, or try again.';
      enginePromise = undefined;
    }
  }
}
form.addEventListener('submit', event => {event.preventDefault(); clearTimeout(timer); search();});
query.addEventListener('input', () => {clearTimeout(timer); timer = setTimeout(() => search(), 250);});
agency.addEventListener('change', () => search());
section.addEventListener('change', () => search());
documentType.addEventListener('change', () => search());
if (query.value) search();
