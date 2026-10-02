/* Interaction checks for the shared reviewer popup in the existing smoke runner. */
export async function checkReviewerViewer(page, category) {
  const initialUrl = page.url();
  if (category === 'sketches') await page.locator('details.sketch-disclosure > summary').click();
  const tab = page.getByRole("tab", { name: new RegExp(`^${category}`, "i") });
  if (await tab.count()) await tab.click();
  const trigger = page.locator('.object-main-view a[data-preview-gallery]').first();
  const standalone = (await trigger.count()) === 0;
  const vectorLinks = page.locator('main a[href$=".svg"]');
  const opener = category === 'beauty' ? page.locator('.amara-beauty-gallery a').first()
    : category === 'concepts' ? page.locator('.amara-direction-gallery a').first()
    : category === 'sketches' ? page.locator('.award-sketch-grid a').first()
    : standalone ? (await vectorLinks.count() ? vectorLinks.first() : page.locator('main a[href$=".webp"]').first()) : trigger;
  await page.locator("#portfolio-image-dialog").waitFor({ state: "attached" });
  const gallery = standalone ? null : JSON.parse(await opener.getAttribute("data-preview-gallery"));
  await opener.click();
  const dialog = page.locator("#portfolio-image-dialog");
  await dialog.waitFor({ state: "visible" });
  const total = Number((await dialog.locator('[data-counter]').innerText()).split('/')[1]);
  if (gallery && total !== gallery.length) throw Error("Popup omitted gallery images");
  async function verify(index) {
    const counter = (await dialog.locator('[data-counter]').innerText()).trim();
    if (counter !== `${index + 1} / ${total}`) throw Error(`Wrong image counter: ${counter}`);
    await dialog.locator('img').evaluate(image => new Promise((resolve, reject) => {
      if (image.complete) return image.naturalWidth ? resolve() : reject(Error("Image failed to load"));
      image.addEventListener('load', resolve, { once: true });
      image.addEventListener('error', () => reject(Error("Image failed to load")), { once: true });
    }));
    if (gallery) {
      const expected = new URL(gallery[index].href, initialUrl).href;
      if (await dialog.locator('img').getAttribute('src') !== expected) throw Error("Navigation showed the wrong image");
      if (await dialog.locator('[data-download]').getAttribute('href') !== expected) throw Error("Download did not follow the displayed image");
      if (await dialog.locator('h2').innerText() !== gallery[index].title) throw Error("Caption did not follow the displayed image");
    }
    if (await dialog.locator('[data-download]').getAttribute('href') !== await dialog.locator('img').getAttribute('src')) throw Error('Download and displayed image differ');
    if (page.url() !== initialUrl) throw Error("Image popup navigated away from the portfolio");
  }
  await verify(0);
  if (total > 1) {
    for (let i = 1; i <= total; i++) {
      await dialog.locator('[data-next]').click();
      await verify(i % total);
    }
    await dialog.locator('[data-previous]').click();
    await verify(total - 1);
    await page.keyboard.press('ArrowRight');
    await verify(0);
    await page.keyboard.press('ArrowLeft');
    await verify(total - 1);
    await page.keyboard.press('ArrowRight');
    await verify(0);
  } else if (await dialog.locator('.portfolio-image-navigation').isVisible()) {
    throw Error("Single-image gallery has unnecessary navigation");
  }
  await dialog.locator('[data-zoom]').click();
  if (await dialog.locator('[data-zoom]').getAttribute('aria-pressed') !== 'true') throw Error('Zoom failed');
  await dialog.locator('[data-zoom]').click();
  if (await dialog.locator('[data-zoom]').getAttribute('aria-pressed') !== 'false') throw Error('Fit to screen failed');
  const downloaded = page.waitForEvent('download');
  await dialog.locator('[data-download]').click();
  const download = await downloaded;
  if (!/\.(svg|png|jpe?g|webp|avif|gif)$/i.test(download.suggestedFilename())) throw Error('Unexpected download file');
  await page.keyboard.press('Escape');
  await dialog.waitFor({ state: 'hidden' });
  if (!await opener.evaluate(element => document.activeElement === element)) throw Error('Focus was not restored');
  await opener.click();
  await dialog.locator('[data-close]').click();
  await dialog.waitFor({ state: 'hidden' });
  if (await page.evaluate(() => document.body.style.overflow === 'hidden')) throw Error('Page scroll remained locked');
  await opener.click();
  await verify(0);
  const fit = await dialog.evaluate(element => {
    const image = element.querySelector('img').getBoundingClientRect();
    const stage = element.querySelector('.portfolio-image-stage').getBoundingClientRect();
    return image.width <= stage.width + 1 && image.height <= stage.height + 1;
  });
  if (!fit) throw Error('Image does not fit in the popup');
  return { total, allImagesLoaded: true, next: true, previous: true, keyboard: true,
    zoom: true, download: download.suggestedFilename(), escape: true, close: true,
    focusRestored: true, pageScrollRestored: true, imageFits: true };
}
