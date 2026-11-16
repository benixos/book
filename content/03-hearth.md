---
title: "3. Hearth"
---

# 3. Hearth

> [!info] State
> **Partial.** The wire spec is public. The v0 subset (sessions, pub/sub, presence digest) is implemented in the hub, Fabric Kit and Message Kit, and sealed payloads are in production use. **The conformance suite does not exist.**

Hearth is the wire contract between nodes. It is tier-agnostic. BenixOS depends on it; it never depends on BenixOS.

## Design discipline

Hearth borrows the discipline of Plan 9's 9P, not its encoding.

- **A small, fixed set of message types.** v1 has **24** envelope variants: nine request/response pairs, an error response, and five pushes. The target is to stay under 30. New interactions should be new *steps* of existing ones, or application-layer payloads.
- **One response per request**, matched by a per-message **tag**.
- **Pushes are a separate category.**
- **Multi-step interactions use server-issued handles.**
- **Errors are first-class.** Any request can be answered with `RError`.
- **Versioned from the first message.**

### T, R, D

| Prefix | Direction | Semantics |
|---|---|---|
| **T** | client to server | A request with a tag. The server answers with exactly one R or `RError`. |
| **R** | server to client | The response, with the same tag. |
| **D** | server to client | An unsolicited push with `tag = 0`. No reply. |

There is no fourth category.

## Two layers

| Layer | Covers | Implemented by |
|---|---|---|
| **Base** | The envelope, tags, the T/R/D grammar, `RError`, addressing | Message Kit |
| **Fabric** | Sessions, pub/sub, pairing, presence, offline catch-up, end-to-end encryption | The hub, and Fabric Kit as the client SDK |

A message is **one envelope end to end**. Crossing the box boundary swaps only the transport: a Unix socket on the device, a WebSocket to the hub, or, for interactive views, a direct peer link or data channel ([Presenters](13-presenters.html)).

## Transport

- WebSocket with a versioned subprotocol string.
- One Protobuf `Envelope` per binary frame.
- Maximum message size **1 MiB**. Larger payloads go out of band.
- Timestamps are **unix milliseconds, UTC**.

## Session lifecycle

1. Version negotiation
2. Hello (authentication)
3. Ready
4. Heartbeats

## What the protocol covers

| Area | Content |
|---|---|
| **Topics** | Naming, subscribe, unsubscribe, publish; `DDeliver` pushes to subscribers |
| **Presence** | `DPresence` is advisory; `DSessionRevoked` ends a session |
| **Offline catch-up** | A returning device reads what it missed |
| **Device pairing** | `TPair`/`RPair`, an attestation, a displayed fingerprint |
| **Roster** | Devices read the household roster and verify its attestations in a fixed order |
| **Sealing** | End-to-end encrypted payloads and a capability-grant model |

### What the hub can and cannot do to the roster

- It **can** withhold an entry or the whole roster, serve a stale entry, delay, reorder or refuse, and observe which device asked about which.
- It **cannot** substitute a key, fabricate a device, transplant an attestation from another household, or downgrade a v2 attestation.

Withholding and staleness are *denial*, not *substitution*. A transparency log would close that gap and is outside v1.

## How BenixOS uses Hearth

The node contract adds one Hearth clause: a node must speak Hearth v1, prove possession of its device key, verify the roster, and pass the conformance suite.

- **Node messages are payload conventions.** Heartbeats, advertisements, claims, grants and placements add no envelope variants.
- **Node liveness is advertisement freshness.** `DPresence` is advisory.
- **Handles never cross the remote boundary.** Over Hearth a handle means capability plus route plus lease, resolved again on the far side.
- **Placements and invokes are sealed off the LAN**, with the registry's signature inside the sealed payload.
- **Presenter traffic is payload too.** Views, patches and consent are payload kinds. The hub carries only signalling and control for them, never the interactive stream.

## Next

[4. Kits](04-kits.html)
