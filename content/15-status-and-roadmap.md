---
type: meta
title: "15. Status and roadmap"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, status, roadmap, milestones]
status: draft
---

# 15. Status and roadmap

> [!info] State
> A snapshot at **15 November 2026**. The milestones are a **proposal** (2 November 2026); the split between a gateway bundle (MVP-A) and a distributed system (MVP-B) is not yet accepted.

## What exists, by evidence

| Piece | Evidence | Status |
|---|---|---|
| Hearth wire spec | Public repo; v0 subset implemented | Partial |
| Message Kit, Fabric Kit | Published 0.1.0; six dependents; about 7k lines | Pre-release |
| Venue Kit and `venued` | About 31k lines, 489 tests, runnable | Alpha |
| **`venue-node` executor** | 16.8k lines, 133-check exit test passed on two platforms | **Built, needs unmerged patches** |
| Compose bundle (one node) | Real run on Ubuntu 26.04 and macOS Docker Desktop | Built |
| Multi-node link and tools | Simulated cluster only; independent review found open issues | In review |
| Gateway and glues | 266 tests, released binaries | Live, with open security items |
| Distribution mechanism | 397 tests, throwaway keys | Prototype, parked |
| Claim agent, mDNS advertiser | Works end to end on a VM | Built |
| Storage Kit, bitchain | Alpha; encryption in a draft PR | Alpha |
| Inference Kit | 216 tests, public | Alpha |
| DeviceNix | Boots headless on AMD64; rollback never shown | Partial |
| Node contract v0 | 16 sections | Draft, unreviewed |
| Owner-signed grants, signed placements | None | Draft |
| Hearth conformance suite | None | Planned |
| `hub` local mode | Only the mDNS piece, in the gateway | Planned |

## The milestones (proposal)

| M | Name | Exit test (abridged) | Where it is |
|---|---|---|---|
| **M0** | Say it straight | Node contract v0 written; the six rulings made; Track H done or accepted; the host build's red checks fixed | Contract drafted; rulings made; Track H partly open |
| **M1** | **One node, enforced** | On an Ubuntu host the agent runs a container for a **signed** Venue placement it checked itself (signature, incarnation, high-water mark, lease, grants, policy); a grant for one resource cannot reach another under the full path-spelling table; mutation evidence shows each check is load-bearing | **The compose executor is the first half of this, without signing or grants** |
| **M2** | **Two nodes, one OS** | A second node on a different host OS joins over the public hub; sealed frames and fencing tokens; a partition policy exercised by unplugging a node | The weekend's simulated cluster is groundwork, on a different design (LAN star, no hub) |
| **M3** | **Our own work runs on it** | The fleet is nodes in one registry; Errand and Dispatcher jobs, a model-bench job and the Minecraft host are placed by BenixOS; limits enforced | Not started |
| **M4** | **DeviceNix is the native host** | A newer base; rollback proven with a deliberately broken artifact on a QEMU virtual machine; the agent a native `dinit` service | Runs in parallel with M1 to M3 |
| **M5** | **Works with the internet down** | Local hub mode; two nodes keep placing, reading and issuing grants with the WAN cut | Not started |

## The bootstrap decisions

**11 November 2026, compose first.** BenixOS's first install is `docker compose up` on a stock Ubuntu or Debian host with only Docker and the compose plugin. DeviceNix, the Yocto build, per-OS signing, the claim agent and the distribution mechanism are **deferred** for the first bootstrap: the compose bundle pinned by digest replaces the distribution mechanism for now.

**The two MVPs.**

| | MVP-A | MVP-B |
|---|---|---|
| Shape | A **household gateway bundle** | **Distributed**: a resident node agent and per-grantee grants |
| Result | A service behind the gateway, usable from a second device | `venued` places a container on a node; the grant is enforced at the node |
| Status | **Set aside** in favour of Venue first | The existing M1 |

**Direction (11 and 12 November 2026):** Venue first, as the wrapper in front of Docker on localhost; first LAN target is a laptop and a desktop sharing resources; the `benixos` GitHub org holds first-tier repos; **kits stay in `slash-builder`**.

## The critical path, as proposed

> [!warning] Security gate
> Capability design and new code may start now. **Before any build reaches a node that brokers real resources**, the credential split and a deploy-time check must be in place, and the **registry signing key is not issued until then.** The first loopback fixes do not wait.

The backlog is split into tracks: **0** (say it straight, docs), **H** (live exposure, independent), **C** (capability foundation), **N** (the node agent), **I** (identity and user management), **X** (distributions), **T** (Hearth and transport), **D** (DeviceNix), **S** (state and substrate, later). The reconciliations that decide the order:

- **M1 is local**, with no hub in the path and nothing to seal. **M2 is not.** Sealing is a top priority for protocol review and a lower one for security review; both are right, because it must land **before brokering over the hub**, not before M1.
- **The local hub is not on the M2 path.** It runs over the public hub first. It is on the path to "works offline" (M5).
- **`substrate-kit` is not on the critical path to M1.**
- **Track H comes first for anything that leaves the house:** the gateway's path traversal, authenticated loopback glue, replay protection, credential hygiene.

## What not to do now

- Move or rename repos.
- Build gateway item D (the scheduler) in the gateway; Venue's planner absorbs it.
- Migrate `docker_runtime.rs` onto `substrate-kit`.
- Build a richer scope language; three rules cover the three path defects.
- Work on the compositor, Courier kiosk phases, graphics and audio stacks, role images, the manifest-kit resolver, or any Pi work before the rollback proof.
- Put a directory or "user management" service inside the gateway.
- Build a bespoke transport: use the public hub, then the local hub role, then a mesh VPN as an interim.
- Grow a second Hearth profile for constrained devices.

## Decisions that sit with the project's owners

Merging grant-path changes; rotating credentials; deciding "unknown fails closed" versus "never block a local action"; organisation settings; and publishing. An implementing agent never takes a grant-path change out of draft or merges it.

## Next

[16. Open questions](16-open-questions.html)
