---
type: meta
title: "About this book"
---

# About this book

## What it is

A system-wide description of BenixOS, the distributed operating system built from Kits over the Hearth protocol. It covers the design, what exists today, and what is still open.

## What it is not

- **Not a specification.** The node contract and the Hearth spec are the normative documents.
- **Not a tutorial.** Chapter 13 describes a bundle; it is not an install guide.
- **Not a consumer product description.** Quickring and its tiers appear only as the operator and a client of an open platform.

## Scope and method

Written from the project's design notes, the Kit registry, and a read of the public Hearth spec and the executor and distribution repositories. **Nothing was built or run to write it.** Test counts and exit-test results are the repositories' own claims. Each chapter opens with a **State** box that says what is built and what is not.

| Label | Means |
|---|---|
| **Built** | Code exists and is tested; the page names the evidence |
| **Partial** | Something real exists, but a stated part does not |
| **Draft** | A written design with no code behind it |
| **Planned** | Named in a plan; no design and no code |

Kit statuses use the registry's words: design, scaffold, alpha, pre-release, stable, legacy, banked. **No Kit is `stable` today.**

## Status

Written on 15 November 2026. Most of the code described is unpublished, and parts of it change daily. Where a page and a repository disagree, the repository is right.

## AI assistance

Parts of this repository were designed, written and tested with AI tools. A person reviews what is merged and is responsible for it.

## Licence

The text is licensed under Creative Commons Attribution 4.0 International. The build tooling is licensed under Apache-2.0. See `LICENSE-docs` and `LICENSE`.

## Corrections

Open an issue or a pull request on the repository.
