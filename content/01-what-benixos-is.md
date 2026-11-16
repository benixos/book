---
title: "1. What BenixOS is"
---

# 1. What BenixOS is

> [!info] State
> **Partial.** The definition and vocabulary are settled. The system is partly built; see [Status](15-status.html).

BenixOS is a distributed operating system: one namespace, identity, placement and storage across every machine a person or household owns. It is composed of **Kits**, speaks the **Hearth** protocol, and runs on any **host** that meets a small **node contract**.

## Vocabulary

| Term | Means | Is not |
|---|---|---|
| **BenixOS** | The distributed OS | A Linux image |
| **Hearth** | The wire contract between nodes | An OS |
| **Kit** | A library that owns one domain, with an API others build on | A product |
| **Venue** | The registry, planner and ledger for places work can run | The data path |
| **Presenter** | The server that renders an app's interface and mediates consent | The app |
| **Node** | A claimed machine that runs a node agent | Any machine on the network |
| **DeviceNix** | The native host: a light, headless, A/B-updated Linux | The system |

## Principles

- **BenixOS depends on Hearth. Hearth never depends on BenixOS.** The Hearth conformance suite must pass with no BenixOS code present.
- **Products compose Kits.** Kit logic is never forked into a product.
- **Rust for the system.** Apps are Wasm components, and can be written in any language that targets them.
- **Apache-2.0.**

## What BenixOS is not

- **Not a Linux distribution.** DeviceNix is one host among several.
- **Not a replacement for Docker or Kubernetes.** Containers run on Docker. Venue follows the Kubernetes resource model.

## Lineage

BenixOS borrows two ideas and no code.

**Plan 9, through Hearth.** The wire protocol keeps 9P's discipline: a small fixed set of message types, one response per request matched by a tag, pushes kept separate, and multi-step interactions carried by server-issued handles. Household resources are addressed like a namespace: walk, read, write, invoke, watch.

**BeOS, through Kits and presenters.** An API organised as Kits over servers over a kernel, with a server that owns the interface. BenixOS keeps that shape without inheriting any BeOS code or ABI. Its presenter is the `app_server` idea cut at semantics.

No Kit has a stable API yet. Until one does, the Kit layer is a boundary, not a guarantee.

## Next

[2. Architecture](02-architecture.html)
