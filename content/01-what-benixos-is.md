---
type: concept
title: "1. What BenixOS is"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, vocabulary, lineage]
status: draft
---

# 1. What BenixOS is

> [!info] State
> **Partial.** The definition and vocabulary on this page are settled. The system itself is partly built: the placement path runs on one node in a compose bundle, and most of the rest is draft or planned. See [Status and roadmap](15-status-and-roadmap.html). Status is as of 15 November 2026.

## The plan in one sentence

**SlashBuilder builds BenixOS, a distributed operating system composed of Kits, over the Hearth protocol, and runs it on any host. DeviceNix is the light Linux distro that is its native host on owned hardware. Quickring is the commercial operator, offering tiered versions (profiles) of BenixOS.**

That sentence dates from 2 November 2026. It was a refinement of the plan, not a change of direction. Before it, "BenixOS" meant a Linux distribution. After it, BenixOS is the system and the Linux distribution is DeviceNix.

## The vocabulary

| Name | Means | Is not |
|---|---|---|
| **Hearth** | The wire contract between nodes. Tier-agnostic. | An OS |
| **BenixOS** | One namespace, identity, placement and storage across every node a person or household owns. Runs on any host that meets the node contract. | A Linux image |
| **DeviceNix** | The BenixOS-native host distro: a light, headless, A/B-updated Linux that makes owned hardware a BenixOS node. | The system |
| **Kits** | The libraries both layers are built from. | Products |
| **Venue** | The registry, planner and broker for resources in BenixOS, with a resident node agent. | The data path |
| **Thunderhead** | The reference-hardware category noun. | A brand or an OS |
| **Quickring** | The commercial operator. A paid tier is a BenixOS *profile*. | The OS |

## Rules that are locked

- **BenixOS depends on Hearth. Hearth never depends on BenixOS.** The Hearth conformance suite must pass with zero BenixOS code present (locked 22 August 2026).
- **Products compose Kits.** Never fork Kit logic into a product.
- **Rust everywhere except the Flutter/Dart UI facade.**
- **SlashBuilder sells nothing.** The open platform is substrate. Quickring is the commercial layer on top.
- **Licence.** BenixOS is Apache-2.0.

## What BenixOS is not

- **Not a Linux distribution.** That is DeviceNix, and it is one host among several.
- **Not a rewrite of Docker or Kubernetes.** On a node today, containers are run by Docker. Venue follows Kubernetes' resource model on purpose ([[benixos-book/06-venue]]).
- **Not a consumer product.** Nothing here ships to a household as "BenixOS".
- **Not finished.** See the State box on every page.

## Lineage

BenixOS borrows two ideas and no code.

**From Plan 9, through Hearth.** Hearth's wire protocol is described as "9P-inspired": not in encoding (it uses Protobuf) but in discipline. A small, fixed set of message types. Every request gets exactly one response, matched by a tag. Server pushes are a visibly separate category. Multi-step interactions use server-issued handles instead of new message types. The household's resources are addressed like a namespace: walk, read, write, invoke, watch.

**From BeOS, through the Kit model.** BeOS organised its API as a set of Kits over a set of servers over one kernel. BenixOS adopted that shape in May 2026: a kernel-sized platform of composable Kits with stable APIs. It keeps the organising idea without inheriting any BeOS code, ABI or the compatibility burden that binds Haiku to the original BeAPI.

> [!warning] A promise the code does not yet keep
> BeOS's strength was that Kit APIs were stable. **No BenixOS Kit is `stable`.** Two are `pre-release` (Message Kit, Fabric Kit); the rest are alpha, banked or archived. The Kit layer is a boundary today, not yet a guarantee. See [[benixos-book/04-kits]].

## A short history of the name

| When | What happened |
|---|---|
| By 2026-05 | "DeviceNix" names the headless edition of one OS (the earliest, BeagleBone-era work is in `devicenix-legacy/`). |
| 2026-05 | The Kit model is adopted, modelled on BeOS. |
| 22 August 2026 | DeviceNix is retired into BenixOS: "one OS, not three classes". The `core` Yocto build becomes "BenixOS". |
| 23 August 2026 | The SlashBuilder consolidation moves the Kits into `slash-builder/`. |
| **2 November 2026** | **The split.** BenixOS becomes the distributed OS. DeviceNix is reclaimed for the host distro, with a different scope. |
| 11 November 2026/12 | The compose-first bootstrap and the Venue-led one-node bundle (chapter 13). |

A reader who finds "DeviceNix" in `devicenix-legacy/` or an archived GitHub org is looking at the earlier BeagleBone-era use of the name.

## Next

[2. Architecture](02-architecture.html)
