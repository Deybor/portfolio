/* Shared image viewer for the portfolio and standalone specification pages. */
(() => {
  if (document.getElementById('portfolio-image-dialog')) return;
  const dialog = document.createElement('dialog');
  dialog.id = 'portfolio-image-dialog';
  dialog.className = 'portfolio-image-dialog';
  dialog.setAttribute('aria-labelledby', 'portfolio-image-title');
  dialog.innerHTML = `<div class="portfolio-image-toolbar">
    <h2 id="portfolio-image-title">Image preview</h2>
    <div class="portfolio-image-actions">
      <button type="button" data-zoom aria-pressed="false">Zoom in</button>
      <a data-download download>Download</a>
      <button type="button" data-close autofocus aria-label="Close image preview">Close ×</button>
    </div>
  </div>
  <div class="portfolio-image-stage"><img alt="" draggable="false"></div>
  <nav class="portfolio-image-navigation" aria-label="Image navigation">
    <button type="button" data-previous aria-label="Previous image">←</button>
    <span data-counter aria-live="polite"></span>
    <button type="button" data-next aria-label="Next image">→</button>
  </nav>
  <p class="portfolio-image-status" role="status" hidden>Loading image…</p>`;
  document.body.append(dialog);
  const image = dialog.querySelector('img');
  const stage = dialog.querySelector('.portfolio-image-stage');
  const zoom = dialog.querySelector('[data-zoom]');
  const status = dialog.querySelector('[role=status]');
  const navigation = dialog.querySelector('.portfolio-image-navigation');
  let gallery = [];
  let index = 0;
  let opener = null;
  let previousOverflow = '';
  function resetZoom() {
    dialog.classList.remove('is-zoomed');
    zoom.textContent = 'Zoom in';
    zoom.setAttribute('aria-pressed', 'false');
    stage.scrollTo(0, 0);
  }
  function close() { if (dialog.open) { dialog.close(); cleanup(); } }
  function showImage(nextIndex) {
    index = (nextIndex + gallery.length) % gallery.length;
    const item = gallery[index];
    resetZoom();
    dialog.querySelector('#portfolio-image-title').textContent = item.title;
    image.alt = item.title;
    status.textContent = 'Loading image…';
    status.hidden = false;
    zoom.disabled = true;
    const download = dialog.querySelector('[data-download]');
    download.href = item.href;
    download.setAttribute('download', decodeURIComponent(new URL(item.href).pathname.split('/').pop()));
    dialog.querySelector('[data-counter]').textContent = `${index + 1} / ${gallery.length}`;
    navigation.hidden = gallery.length < 2;
    image.src = item.href;
  }
  dialog.querySelector('[data-previous]').addEventListener('click', () => showImage(index - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => showImage(index + 1));
  dialog.addEventListener('keydown', (event) => {
    if (gallery.length < 2 || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    showImage(index + (event.key === 'ArrowLeft' ? -1 : 1));
  });
  dialog.querySelector('[data-close]').addEventListener('click', close);
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) close();
  });
  function cleanup() {
    if (!opener) return;
    document.body.style.overflow = previousOverflow;
    resetZoom();
    image.removeAttribute('src');
    if (opener?.isConnected) opener.focus({ preventScroll: true });
    opener = null;
    gallery = [];
  }
  dialog.addEventListener('close', () => { if (!dialog.open) cleanup(); });
  dialog.addEventListener('cancel', (event) => { event.preventDefault(); close(); });
  zoom.addEventListener('click', () => {
    const enlarged = dialog.classList.toggle('is-zoomed');
    zoom.textContent = enlarged ? 'Fit to screen' : 'Zoom in';
    zoom.setAttribute('aria-pressed', String(enlarged));
    stage.scrollTo(0, 0);
  });
  image.addEventListener('load', () => { status.hidden = true; zoom.disabled = false; });
  image.addEventListener('error', () => {
    status.textContent = 'This image could not load. You can still download it.';
    status.hidden = false;
    zoom.disabled = true;
  });
  window.addEventListener('popstate', close);
  document.addEventListener('click', (event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!(event.target instanceof Element)) return;
    const link = event.target.closest('a[href]');
    if (!link || link.hasAttribute('download') || dialog.contains(link)) return;
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin || !/\.(svg|png|jpe?g|webp|avif|gif)$/i.test(url.pathname)) return;
    event.preventDefault();
    const figure = link.closest('figure');
    const preview = link.querySelector('img') || figure?.querySelector('img');
    const title = preview?.alt || link.getAttribute('aria-label') || figure?.querySelector('figcaption')?.textContent?.trim() || 'Image preview';
    opener = link;
    gallery = [];
    if (link.dataset.previewGallery) {
      try {
        gallery = JSON.parse(link.dataset.previewGallery).filter((item) => {
          const asset = new URL(item.href, location.href);
          return asset.origin === location.origin && /\.(svg|png|jpe?g|webp|avif|gif)$/i.test(asset.pathname);
        }).map((item) => ({ href: new URL(item.href, location.href).href, title: item.title || title }));
      } catch { gallery = []; }
    } else {
      const group = link.closest('[data-preview-group], .amara-direction-gallery, .amara-beauty-gallery, .award-sketch-grid, .technical-drawings') || link.closest('main');
      const seen = new Set();
      gallery = Array.from(group?.querySelectorAll('a[href]') || []).flatMap((candidate) => {
        const asset = new URL(candidate.href, location.href);
        if (candidate.hasAttribute('download') || asset.origin !== location.origin || !/\.(svg|png|jpe?g|webp|avif|gif)$/i.test(asset.pathname) || seen.has(asset.href)) return [];
        seen.add(asset.href);
        const figure = candidate.closest('figure, .drawing-sheet, .labelled-model, .amara-direction-card, section');
        return [{ href: asset.href, title: candidate.querySelector('figcaption')?.textContent?.trim() || figure?.querySelector('h2,h3')?.textContent?.trim() || candidate.querySelector('img')?.alt || figure?.querySelector('img')?.alt || candidate.getAttribute('aria-label') || candidate.textContent.trim() || 'Image preview' }];
      });
    }
    index = gallery.findIndex((item) => item.href === url.href);
    if (index < 0) { gallery = [{ href: url.href, title }]; index = 0; }
    previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    showImage(index);
    dialog.showModal();
  }, true);
})();
