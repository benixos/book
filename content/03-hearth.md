---
type: concept
title: "3. Hearth"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, hearth, protocol, wire]
status: draft
---

# 3. Hearth

> [!info] State
> **Partial.** The wire spec is public (`slash-builder/hearth`; code Apache-2.0, spec CC-BY-4.0). The v0 subset (sessions, pub/sub, presence digest) is implemented in the hub, Fabric Kit and Message Kit. Sealed payloads (levels E0 and E1) are live in Courier. **The Hearth conformance suite does not exist.** The `.proto` package is still named `quickring.v1`, and the spec's status header is out of date (see Known problems).

Hearth is the wire contract between nodes. It is **tier-agnostic** and sells nothing: SlashBuilder stewards it as a peer project alongside BenixOS, and Quickring is the commercial layer built on it. BenixOS depends on Hearth; Hearth never depends on BenixOS.

## Design discipline

Borrowed from Plan 9's 9P, in discipline rather than encoding:

- **A small, fixed set of message types.** v1 has **24** envelope variants: nine T/R pairs, `RError`, and five D-pushes. The aim is to stay under 30 for the life of the protocol. New interactions should be new *steps* of existing ones, or application-layer payloads, not new variants.
- **Every request gets exactly one response**, correlated by a per-message **tag**.
- **Server pushes are a separate category**, visibly distinct.
- **Multi-step interactions use server-issued handles**, as 9P's `Twalk` does.
- **Errors are first-class**: any request can be answered with `RError` carrying the same tag.
- **Versioned from message one**: version negotiation precedes all other traffic.

### T, R, D

| Prefix | Direction | Semantics |
|---|---|---|
| **T** | client to server | A request. Carries a tag. The server **must** answer with exactly one matching R or `RError`. |
| **R** | server to client | The response, with the same tag. |
| **D** | server to client | An unsolicited push. `tag = 0`. The client does not reply. |

"There is no fourth category."

## Two layers

| Layer | Covers | Implemented by |
|---|---|---|
| **Base** | The envelope, tag correlation, the T/R/D grammar, `RError`, the addressing model | **Message Kit**, on the device and in any client's transport core |
| **Fabric** | Sessions, networked pub/sub, pairing, presence, offline catch-up, E2E encryption, the feed convention | The hub (the Quickring daemon), and **Fabric Kit** as the client SDK |

A message is **one envelope end to end**. Crossing the box boundary swaps only the *transport*: `AF_UNIX SOCK_SEQPACKET` on the device, WebSocket to the hub. The Quickring daemon registers with Message Kit's router as the **remote-transport provider** (ADR-0002, 5 June 2026).

## Transport (hub)

- WebSocket, `wss://…/v1`, subprotocol `quickring.v1`.
- One Protobuf `Envelope` per binary frame. No multi-frame messages.
- Maximum message size **1 MiB**. Larger payloads go out of band and never traverse the hub.
- All timestamps are **unix milliseconds, UTC**. No local time on the wire.
- The hub is a Rust service on `axum`'s WebSocket support. A separate conventional HTTP API handles signup and device registration; the protocol document does not cover it.

## Session lifecycle

1. **Version negotiation.**
2. **Hello**: authentication.
3. **Ready.**
4. **Heartbeats** keep it alive.

## What the protocol covers

| Area | Content |
|---|---|
| **Topics** | Naming convention; subscribe, unsubscribe, publish; `DDeliver` pushes the message to subscribers |
| **Presence** | `DPresence` is advisory; `DSessionRevoked` ends a session |
| **Offline catch-up** | A device that was away reads what it missed |
| **Device pairing** | `TPair`/`RPair`, a pairing attestation, a displayed fingerprint, a conformance vector |
| **Roster** | A device can read the household's roster, and a reader must verify the attestations in a fixed order |
| **Sealing and E2E** | Sealed payloads and a capability-grant model; the design is in `encryption.md` |
| **Errors, rate limits, versioning** | `RError` taxonomy; abuse limits; the break and major-bump rules |

**What the hub can and cannot do to the roster.** The spec states this boundary itself.

- It **can** withhold an entry or the whole roster, serve a stale entry or roll back to an earlier one, delay, reorder or refuse, and observe which device asked about which.
- It **cannot** substitute a key, fabricate a device, transplant an attestation from another household, or downgrade a v2 attestation.

Withholding and staleness are *denial*, not *substitution*. The spec names the missing piece, a transparency log, and leaves it out of v1.

## How BenixOS uses Hearth

The node contract adds exactly **one** Hearth clause (§9): a node MUST speak Hearth v1, prove possession of its device key, verify the roster, and pass the conformance suite.

- **Node messages are payload conventions, not new wire types.** Heartbeats, advertisements, claims, grants and placements are application-layer payloads with **zero new envelope variants** (24 of about 30 used).
- **Node liveness is advertisement freshness.** `DPresence` is advisory only.
- **Handles never cross the remote boundary.** Over Hearth a handle means *capability plus route plus lease*, re-resolved on the far side.
- **Placements and invokes are sealed off the LAN**, with the registry's signature inside the sealed payload.

> [!warning] None of the node messages are built
> Sealing of machine frames is not built (`publish_encrypted` is absent from the gateway). The Venue executor in the compose bundle talks plain HTTP to `venued` on loopback or an internal Docker network. Node-contract §9 is **Draft**.

## The hub and local mode

The **hub** is the OSS reference server, operated by Quickring. Its **local mode** (`_hearth._tcp` discovery, roster cache, a listener so a household works with the WAN cut) is **Planned**: only the mDNS piece shipped, inside the gateway. The 2 November 2026 plan rehomes it to the hub binary. Milestone M5 ("works with the internet down") depends on it.

## Known problems

- **Stale status headers.** `protocol.md` still says pairing, catch-up, `DPresence`, unsubscribe, dedup, rate limits and E2E "remain spec-only". The Hearth README says E0/E1 sealing is live and device pairing ships in Courier. **`docs/encryption.md` still describes a pre-implementation state** ("NOTHING IN THIS DOCUMENT IS IMPLEMENTED"). Updating them is real work, flagged and not done.
- **The `.proto` package name** is still `quickring.v1`. Renaming it is a coordinated change across `hub`, `fabric-kit`, `gateway` and `courier`.
- **No conformance suite.** The plan is to build it in `spec-kit`.
- **macOS has no local transport.** `AF_UNIX SOCK_SEQPACKET` does not run there. The contract's proposed fix is u32-length-prefixed framing over `SOCK_STREAM`, capped at 1 MiB, carrying the same envelope bytes. Windows would use named pipes. **Loopback TCP is forbidden for the agent**: it has no peer identity.

## Next

[4. Kits](04-kits.html)
