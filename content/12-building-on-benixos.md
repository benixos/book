---
type: concept
title: "12. Building on BenixOS"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, apps, workloads, app-context-kit, first-workload]
status: draft
---

# 12. Building on BenixOS

> [!info] State
> **App Context Kit: alpha**, public, with 61 shared fixtures that Dart and Rust both pass. **Courier**, the Hearth client, is live and stays a client first. **The first workload (a notes reader) is built and verified locally but has never been placed by BenixOS.** How a third party would package and publish an app is **Draft or Planned**.

## What can run on a node

| Kind | How it is delivered | Status |
|---|---|---|
| **A container** | An OCI image, pinned by digest | **Built**: the executor runs it under local policy |
| **A binary** | A signed artifact; only if the operator allows | **Prototype**, in the distribution mechanism only |
| **A service behind the gateway** | A glue plus the upstream service | **Built** for Jellyfin, HA and others, outside Venue |

A workload's language is not the OS's concern: the OS runs it.

## App Context Kit: what an app gets

One spec, two implementations (a Dart core with a Flutter companion, and a Rust crate), both held to **61 shared conformance fixtures**. It gives an app:

- an **identity**,
- **directories and settings**, with **test and scratch modes**,
- a **roster presence** entry,
- a **Venue session**, and
- **opt-in peers**.

Six demo apps live in the Kit Book repo. It has no stable API and is not published to crates.io. An earlier spike of the same idea, `application-kit`, is probably superseded; the atlas asks for that to be confirmed and the spike archived or folded in.

## Other Kits an app composes

| Need | Kit |
|---|---|
| Talk to the household | Fabric Kit over Message Kit |
| Place work on a machine | Venue Kit |
| Store content | Storage Kit |
| Know who someone is | Identity Kit |
| Run a gated agent task | Errand Kit |
| Local model inference | Inference Kit (egress-gated, immutable OS-shipped models) |
| UI | Interface Kit over Digital Zen tokens |
| A workflow strip | Work Strip Kit |

## Courier

Courier is the Hearth client: an OSS core plus a branded overlay, in the Quickring org. **It stays a client first** (a locked decision) and stays backend-agnostic. DeviceNix may host it as a kiosk-mode Flutter client on a test machine; it does not modify it.

## The first workload: a notes reader

The first BenixOS workload is a **notes reader**. It is a good bootstrap project: we can use it immediately to do work in building out more BenixOS functionality.

It is a Python process behind a loopback-only, key-gated web server. It already earns its keep: it is how we read and search our own working notes, including BenixOS's, from any machine.

| Step | What runs | State |
|---|---|---|
| **v0** | The reader only, **no network** | Built and verified locally; **not yet run by any BenixOS node** |
| **v1** | Reader plus browser agent chat | Design only |
| **v2** | Published view as namespace nodes over `qr.view/patch` | Later |

### The run shape a node would apply

`--user <uid>`, `--network none`, `--read-only`, `--cap-drop ALL`, `no-new-privileges`, 128 pids, 512 MB, `/tmp` as a noexec tmpfs, the notes directory mounted `:ro`, a socket directory, the access key as a read-only file, exposed on loopback by a socket proxy. Tested inside the container: only a loopback interface, outbound connects fail, writes fail, executing from `/tmp` is denied, effective capabilities are zero, and the key is not in the environment.

### The five gaps it forces

| # | Needs | Why BenixOS cannot express it today |
|---|---|---|
| 1 | The notes directory **read-only** | No volumes at all. A mount must be a typed, owner-granted resource, **never a host path**. |
| 2 | The access key as a **secret file** | No secrets delivery. Not an env var, a command line or an image layer. |
| 3 | **Exposure with no network** | A published port needs a bridge network and egress. The node should proxy a **Unix socket** to loopback or the fabric. |
| 4 | A **registry** to pin by digest | The image is local; a lock needs a registry manifest digest. |
| 5 | The node's **unprivileged user**, not a baked-in uid | Containers run as the image's user today. |

Health checks, resource limits and a binary sandbox are not blockers.

### Why this is the right first workload

It is small and honest, it forces the right three mechanism gaps and little else, and the people building BenixOS use it daily, so defects surface fast. Milestone M3 names the next workloads: Errand and Dispatcher jobs, a model-bench job and the Minecraft host, all placed by BenixOS.

## Next

[13. The one-node bundle](13-one-node-bundle.html)
