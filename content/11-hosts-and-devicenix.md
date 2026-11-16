---
type: concept
title: "11. Hosts and DeviceNix"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, devicenix, hosts, yocto, hardware]
status: draft
---

# 11. Hosts and DeviceNix

> [!info] State
> **DeviceNix** (`slash-builder/core`): **Partial.** It boots headless on AMD64; the A/B update plumbing exists; **rollback has never been demonstrated**. The base uplift (kirkstone to wrynose) is a draft PR. **Other hosts:** Ubuntu is what runs today; macOS and Windows are **Draft**.

BenixOS runs on **any host that meets the node contract**. DeviceNix is one such host: the native one.

## DeviceNix

A light, headless, A/B-updated Linux that makes owned hardware a BenixOS node. It covers hardware enablement, root of trust and update. It is **not** the system.

| Fact | Detail |
|---|---|
| Build | Yocto: `meta-benixos`, `kas`, `meta-mender`, a manifest-driven production pipeline |
| C library | **musl** (a README elsewhere wrongly says glibc) |
| Init | **dinit** (units for dockerd, qr-gateway, claim and mDNS exist) |
| Update | A/B plumbing via Mender exists on AMD64; **rollback not demonstrated** |
| CI | A Jenkins pipeline; artifacts publish to an internal registry |
| Host rule | A node MUST NOT be able to brick itself; a rollback must be demonstrated before it claims "native host" (contract §11.1) |

### Names to leave alone

Do **not** rename `meta-benixos`, the `benix-*` artifact paths or `benixos-manifest.yaml`; a pending PR already churns them. A **name-map note** in `core` will list old and new meanings. Existing `benix-*` repo names stay. New repos use `benixos-<thing>` for the system and `devicenix-<thing>` for the host.

### Bring-up plan

The standing plan (since 31 August 2026) is to **build an all-in-one, maximally-instrumented AMD64 desktop image first**, then subtract down into role-defined images. Three reasons:

- An all-in-one image is a desktop by another degree.
- It gives far more real-world debugging surface than a headless bring-up.
- `Squall` (the Forge workstation) is already BenixOS's reference desktop.

Since 2 November 2026 the Forge test machine **stays on Ubuntu for now**. DeviceNix proves itself on a **QEMU virtual machine**, with the rollback proof targeted there first. Moving the test machine to DeviceNix is a later swap.

**Open:** the Kconfig-style resolution that would let one all-in-one manifest subtract into per-device manifests is a separate, undesigned pass in `manifest-kit`. Whether desktop-first stands or is superseded is still to be confirmed; nothing in the first milestones depends on the answer.

### Pieces around it

| Piece | State |
|---|---|
| `benix-base` | `libbenix` (portable, four targets) plus an atomic kernel and libc bundle. README split: `libbenix` is a candidate node-contract primitive layer; the bundle is a DeviceNix build idea. |
| Curated ABI shim | A semi-stable shared library re-exporting libc plus kernel-primitive bindings, **the one blessed dynamic-linking boundary** (modelled on Haiku's `libroot.so`, not reusing the name). A design decision of 30 August 2026. |
| `benix-compositor` | Smithay kiosk compositor, Phase 1 MVP. PR #1 open since 1 September 2026. Parked. |
| `benix-mdns-advertiser` | Unclaimed-box discovery. Portable code; only its `dinit` unit is DeviceNix. |
| Interface Kit, `mediakit` | The kiosk chrome and media handling. `mediakit` is dormant since July. |

## Host profiles (a prompt, not a finding)

The contract's first-cut table, marked by its own author as "a prompt for the foreign-host study, not a finding":

| Requirement | DeviceNix | Ubuntu | macOS | Windows | Android / iOS |
|---|---|---|---|---|---|
| Class | full | full | full, reduced | client until the named-pipe transport exists | client |
| Agent supervision | dinit, native | systemd | launchd | Windows service, later | n/a |
| Rootless runtime | per image | rootless Podman | a VM backend only | WSL2 or Docker Desktop | none |
| Local IPC | seqpacket, kernel peer creds | seqpacket | stream-framed (to build) | named pipe (to build) | n/a |
| Cgroup limits | to build | yes | no | no | n/a |
| Update | A/B image | OS package manager | signed `.pkg` | `benix-update` | store |
| Signing | n/a | none (TUF) | Developer ID + notarisation (needs project credentials) | Authenticode (needs project credentials) | store accounts (needs project credentials) |

The bundle that runs today assumes **Docker on a Linux host**; the contract's rootless-Podman requirement is unreconciled with that ([Nodes](05-nodes.html)).

## Thunderhead hardware

**Thunderhead** is the reference-hardware category, run as its own program. DeviceNix is the OS those devices eventually ship on.

| Family | What | Notes |
|---|---|---|
| **Aether** | Raspberry Pi 5 / CM5 | |
| **Forge** | AMD64 micro-ATX 244×244 mm | **Squall** is the reference desktop workstation; a Forge test machine is in the lab |

The five devices are Cumulus, Anvil, Wisp, Halcyon and Squall (which family each belongs to is the Thunderhead program's record, not this book's). The device ladder is Maker, Kit, Assembled, Production. The program is currently **off-focus**, so Thunderhead Kit is banked. DeviceNix consumes board bring-up and peripherals from there; it does not own them.

## Next

[12. Building on BenixOS](12-building-on-benixos.html)
