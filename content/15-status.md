---
title: "15. Status"
---

# 15. Status

> [!info] State
> A snapshot at **15 November 2026**. Where this page and a repository disagree, the repository is right.

## What exists

| Piece | State |
|---|---|
| Hearth wire spec | Public; v0 subset implemented |
| Message Kit, Fabric Kit | Pre-release |
| Venue Kit and `venued` | Alpha; runnable |
| Executor | Built for a single node |
| Several-node link and tools | Built and reviewed against a simulated cluster |
| Gateway and glues | Live |
| Distribution mechanism | Prototype, throwaway keys |
| Claim agent and mDNS advertiser | Built |
| Storage Kit | Alpha |
| Inference Kit | Alpha |
| DeviceNix | Partial: boots headless; rollback not shown |
| Node contract v0 | Draft |
| Presenter spec and core | Draft; exercised by a local prototype |
| Wasm loader and signer | Prototype |
| Window shell (Casement) | Planned; prototype pieces exist |

## Not yet built

- Owner-signed grants and signed placements
- Sealing of node messages
- The Hearth conformance suite and a node conformance suite
- A local hub mode, so a household works without the internet
- Workload storage and egress control
- Real key custody for distribution signing
- A demonstrated DeviceNix rollback
- A stable API on any Kit
- A frozen presenter spec, and a presenter with a live window
- A trusted display path on any host
- Independent presenter and signer implementations
- A direct path across the WAN
- A production toolchain for asynchronous components

## How to read the labels

| Label | Means |
|---|---|
| **Built** | Code exists and is tested |
| **Partial** | Something real exists, but a stated part does not |
| **Draft** | A written design with no code behind it |
| **Planned** | Named in a plan; no design and no code |

## Next

[Glossary](90-glossary.html) · [About this book](about.html)
