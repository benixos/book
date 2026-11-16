# The BenixOS Book

A system-wide description of BenixOS, the distributed operating system built from Kits over the Hearth protocol: its design, what exists today, and what is still open.

The site is built from [`content/`](content/) into [`docs/`](docs/) and served at <https://book.benixos.com>.

> **Status: early.** Most of the code the book describes is not published, and several pieces are drafts. Each chapter opens with a State box that says what is built and what is not.

## Layout

| Path | What |
|---|---|
| `content/` | The book, one Markdown file per page |
| `assets/` | Stylesheet, script, the architecture diagram, and a vendored copy of Mermaid (see `assets/vendor/README.md`) |
| `tools/build.py` | The static-site build. It also fails on forbidden content and broken local links |
| `docs/` | The built site. Generated; do not edit by hand |

## Build

```sh
python3 -m pip install markdown pyyaml
make build     # content/ and assets/ into docs/
make serve     # http://localhost:8000
```

The build fails if the output contains a person's name, a vault or wiki link, an internal hostname or tracker key, or a local link that does not resolve.

## Contributing

Open an issue or a pull request. Keep to the register of the book: engineering, plain, one idea per paragraph, and a State box on every chapter that says what is built.

## AI assistance

Parts of this repository were designed, written and tested with AI tools. A person reviews what is merged and is responsible for it. AI-assisted commits carry an `Assisted-by:` line.

## Licence

The text is CC BY 4.0 (`LICENSE-docs`). The build tooling is Apache-2.0 (`LICENSE`).
