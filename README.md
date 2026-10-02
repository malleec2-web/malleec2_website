# Mallee C2 website

Static website for [malleec2.com.au](https://malleec2.com.au), designed for hosting with GitHub Pages.

## Local preview

Run a static server from the repository root:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Publishing

GitHub Pages is available at no cost when this repository is **public**. Do not commit passwords, API keys, client information or other secrets to this repository.

1. Push the site to the default branch of the GitHub repository.
2. In the repository, open **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the default branch and `/ (root)`, then save.
5. Set the custom domain to `malleec2.com.au` and enable **Enforce HTTPS** once the certificate is available.

The `CNAME` file tells GitHub Pages to serve the site at the custom domain. DNS records must also be configured at the domain registrar.

## Porkbun DNS

Remove any conflicting parking, URL-forwarding, `A`, `AAAA` or `CNAME` records for `@` and `www`, then add:

| Type | Host | Answer |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `malleec2-jtewes.github.io` |

DNS changes can take up to 24 hours to propagate. Configure the custom domain in GitHub before changing DNS to avoid a domain takeover risk.
