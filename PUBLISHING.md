# Publishing

How the site is hosted, how to change it, and how to check that a change went live.

## How it is hosted

| Part | Setting |
|---|---|
| Host | GitHub Pages, from the `main` branch, folder `/docs` |
| Build type | Branch deploy. `docs/.nojekyll` turns off GitHub's own Jekyll build, so the files are served exactly as committed |
| Domain | `book.benixos.com`, set by `docs/CNAME` and in the repository's Pages settings |
| HTTPS | A certificate issued and renewed by GitHub Pages |
| Third-party requests | None. Mermaid is vendored in `assets/vendor/` |

There is no deploy pipeline of our own. Merging to `main` publishes the committed `docs/` folder.

## Changing the book

1. Edit files in `content/` (or `assets/`, or `tools/build.py`). To change the architecture diagram, edit `tools/make_diagram.py` and run `make diagram`.
2. Run `make build`. It rewrites `docs/` and fails on forbidden content or a broken local link.
3. Commit `content/` and `docs/` **together**. The published site is `docs/`, so a content change without a rebuild is not live.
4. Open a pull request. The `check` workflow runs the build.
5. A person reviews and merges. The site footer says "a person reviews what we publish", so the merge is that review.
6. Wait about a minute for the Pages build, then run `make validate`.

Pages serves files with `Cache-Control: max-age=600`, so a browser can show the old page for up to ten minutes.

### What the build refuses

The build fails if any page or the diagram contains a person's name or initials, a vault or wiki link, an internal hostname, machine name or tracker key, or a local link that does not resolve. Edit `FORBIDDEN` in `tools/build.py` to change the list.

### The footer year

The footer year is generated at build time. A site that is rebuilt in a new year carries the new year; pages that are not rebuilt keep the old one.

## Validating the live site

```sh
make validate                                   # against https://book.benixos.com/
python3 -I tools/validate_live.py https://example.test/   # against another base URL
```

It checks, in order:

| Check | Fails when |
|---|---|
| DNS | The name does not resolve |
| HTTPS certificate | The handshake fails, the certificate does not name the host, or it expires within 14 days (a warning under 30) |
| HTTP behaviour | A plain `http://` request does not return 200 or a redirect. It warns if HTTP is served without redirecting to HTTPS |
| Files | A file in `docs/` is missing, or is not byte-identical to what is served |
| Footer | A page lacks the footer sentence |
| Not found | A missing page does not return 404 with the custom page |

The script exits 0 when nothing fails (warnings are allowed) and 1 otherwise.

## The domain

Two things must be true for the custom domain to work:

- **The Pages settings name the domain.** That is the `cname` setting, which `docs/CNAME` keeps in step.
- **DNS points the name at GitHub Pages.** GitHub's guidance for a subdomain is a `CNAME` record to `benixos.github.io`. Pointing `A` and `AAAA` records at GitHub's Pages addresses (`185.199.108.153` to `185.199.111.153`, and the matching IPv6 addresses) also works, but a single address leaves the site exposed if that one address changes.

Enable **Enforce HTTPS** in the repository's Pages settings once the certificate shows as approved. Until it is on, `http://book.benixos.com/` is served as plain HTTP, and `https://benixos.github.io/book/` redirects to the `http://` form of the custom domain.

Set the DNS record **after** the domain is claimed in the Pages settings, never before. A record that points at GitHub for a name no repository has claimed can be taken over by anyone.

## Rolling back

Revert the merge commit on `main` and push. The previous `docs/` is published again within a minute. `make validate` confirms it.

## Updating Mermaid

`assets/vendor/mermaid.min.js` is a pinned, unmodified copy (see `assets/vendor/README.md`). To update it, download the new release from the same CDN path, replace the file and its licence, update the version in the README, rebuild, and look at every page that has a diagram: `02`, `04`, `06`, `09` and `13`.
