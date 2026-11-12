# Mallee C2 website

Static website for [malleec2.com.au](https://malleec2.com.au), hosted on GitHub Pages. It is built from the designer's 2026 skins (MC002_WEBSITE SKINS_2026) and brand cheat sheet; those files are the source of truth for layout, copy, type and colour.

## Structure

| Path | Page |
| --- | --- |
| `index.html` | Home (also holds the Partners section, `/#partners`) |
| `capability/` | Capability |
| `approach/` | Approach |
| `about/` | About |
| `contact/` | Contact |
| `privacy/` | Privacy policy (placeholder until the policy is final) |
| `404.html` | Not-found page |
| `assets/css/site.css` | All styles. Brand colours, the T1–T7 type scale and spacing are tokens at the top |
| `assets/js/site.js` | Mobile menu and contact form |
| `assets/img`, `assets/fonts` | Web-optimised images, logos (SVG) and DM Sans (WOFF2) |
| `tools/build_assets.py` | Regenerates `assets/img` and `assets/fonts` from the designer's files |

There is no build step for the pages themselves: they are plain HTML. The header and footer are repeated in each page, so a change to the navigation or footer must be made in every `index.html` (and `404.html`).

## Contact form

No form-processing service is connected yet. Submitting the form opens the visitor's email app with the message addressed to info@malleec2.com.au. To switch to a hosted form service, set the form's `action` and `method="post"` in `contact/index.html` and remove its `data-mailto` attribute.

## Designer assets

The designer's source files live in `WEBSITE ASSETS/` locally. That folder is git-ignored because it is large (~42MB) and the repository is public. When the designer supplies updated imagery, logos or fonts, drop them into that folder and run:

```sh
python3 -m venv .venv && .venv/bin/pip install fonttools brotli pillow
.venv/bin/python tools/build_assets.py
```

This also needs `pdftocairo` (`brew install poppler`).

## Local preview

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Links use root-relative paths (`/assets/...`), so serve from the repository root rather than opening files directly.

## Publishing

GitHub Pages deploys from the `main` branch, `/ (root)`. Pushing to `main` updates the live site. Do not commit passwords, API keys, client information or other secrets to this repository.

The `CNAME` file tells GitHub Pages to serve the site at the custom domain.

## Porkbun DNS

Remove any conflicting parking, URL-forwarding, `A`, `AAAA` or `CNAME` records for `@` and `www`, then add:

| Type | Host | Answer |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `malleec2-web.github.io` |

DNS changes can take up to 24 hours to propagate. Configure the custom domain in GitHub before changing DNS to avoid a domain takeover risk.
