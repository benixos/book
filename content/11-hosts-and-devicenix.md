---
title: "11. Hosts and DeviceNix"
---

# 11. Hosts and DeviceNix

> [!info] State
> **DeviceNix: Partial.** It boots headless on AMD64 and has A/B update plumbing. **Rollback has never been demonstrated.**
>
> **Other hosts:** Ubuntu is what runs today. macOS and Windows are **Draft**.

BenixOS runs on **any host that meets the node contract**. DeviceNix is the native one.

## DeviceNix

A light, headless, A/B-updated Linux that makes owned hardware a BenixOS node. It covers hardware enablement, root of trust and update. It is **not** the system.

| Fact | Detail |
|---|---|
| Build | Yocto, with a `meta-benixos` layer and a manifest-driven pipeline |
| C library | musl |
| Init | `dinit` |
| Update | A/B plumbing exists on AMD64; rollback is not demonstrated |
| Rule | A node must not be able to brick itself. A rollback must be demonstrated before it claims "native host" |

### Bring-up

The plan is to build an **all-in-one, heavily instrumented AMD64 desktop image first**, then subtract down into role-defined images. An all-in-one image gives far more real-world debugging surface than a headless one. DeviceNix proves itself on a virtual machine, with the rollback proof first.

### Related pieces

| Piece | Role |
|---|---|
| `libbenix` | Portable primitives, built for four targets; a candidate for the node contract's primitive layer |
| Claim agent | Device claim ([Nodes](05-nodes.html)) |
| mDNS advertiser | Unclaimed-box discovery |

## Host profiles

A first cut, to be settled by testing:

| Requirement | DeviceNix | Ubuntu | macOS | Windows | Android and iOS |
|---|---|---|---|---|---|
| Class | full | full | full, reduced | client until a named-pipe transport exists | client |
| Agent supervision | `dinit`, native | `systemd` | `launchd` | Windows service, later | n/a |
| Rootless runtime | per image | rootless Podman | a VM backend only | WSL2 or a VM | none |
| Local IPC | seqpacket, kernel peer creds | seqpacket | stream-framed (to build) | named pipe (to build) | n/a |
| Cgroup limits | to build | yes | no | no | n/a |
| Trusted display path | to build | to build | host secure UI | host secure UI | host secure UI |
| Update | A/B image | OS package manager | signed package | `benix-update` | store |

A host without a **trusted display path** is a reduced-trust host: consent cannot be shown in a way a compromised presenter cannot fake ([Presenters](13-presenters.html)). On Linux the window shell can run as the compositor.

The local bus uses `AF_UNIX SOCK_SEQPACKET`, which does not run on macOS. The proposed fix is length-prefixed framing over a stream socket carrying the same envelope bytes. Windows would use named pipes. **Loopback TCP is not allowed for the agent**: it has no peer identity.

## Reference hardware

Two reference families: a Raspberry Pi 5 and compute-module class, and an AMD64 micro-ATX class. DeviceNix consumes their board bring-up and peripheral support from a separate hardware program.

## Next

[12. Building on BenixOS](12-building-on-benixos.html)
