# Existing GitHub portfolio

Repository: https://github.com/Deybor/portfolio
Live portfolio: https://deybor.github.io/portfolio/

The repository's existing Pages workflow deploys the committed `dist` directory on a push to `main`. The updated editable web project is retained under `site/` in that repository. The local working project remains `C:\Users\Master\Documents\portfolio\porfolio update`.

## Build

From the web project directory, run `npm ci`, `npm run typecheck`, and `npm run build:pages` using a current Node version supported by Vite (Node 22.12+). `build:pages` prepares `dist-pages` with all 19 project pages pre-rendered and public media scoped to `/portfolio/`. The normal `npm run build` and local development paths remain available.

Copy the contents of `dist-pages` into the publishing repository's `dist` directory, inspect the diff, commit, and push normally to `main`. Keep the existing `.github/workflows/pages.yml`. Never force-push or include credentials, `.env` files, Blender source files, node_modules, local QA, or screenshots. The source snapshot includes `.grok/app-env.json` so the portfolio's approved public, sign-in-free behavior is reproducible.

## Check

Run `node scripts/check-pages-portfolio.mjs https://deybor.github.io` from the working web project to inspect all project pages, displayed media, drawings, and download links. The browser smoke helper also supports the published site when `BROWSER_ALLOW_EXTERNAL_HOST=1`; use the reviewer gallery option to check the popup. Confirm the GitHub Actions deployment for the actual commit before reporting the site live.

Direct project paths have their own HTML files, so opening or refreshing a jewellery or printed-object page works on GitHub Pages. Route matching tolerates Pages' trailing slashes. The site's approved renders, typography, dimensions, proposals, and production-status wording are preserved.
