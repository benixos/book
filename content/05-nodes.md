---
type: concept
title: "5. Nodes"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, node, node-contract, claim, identity]
status: draft
---

# 5. Nodes

> [!info] State
> **Draft.** The node contract v0 is a 16-section draft. It has not had an independent review, and most of it is not built. The claim flow is **Built** (works end to end on a VM; the TPM side is unverified). The node agent exists only in a first, thin form (see [Venue](06-venue.html)).

## What a node is

A **node** is a machine, or a container, that runs a BenixOS **node agent** and has been **claimed** by an owner. The **owner** is the person whose key was pinned on the node at claim.

A machine is a node when all four hold (contract §1):

1. It runs the node agent as a supervised service.
2. It holds a device key and has completed a claim that pinned an owner key.
3. It is bound to exactly one authority registry, or declares itself standalone.
4. It meets the host profile for its OS ([Hosts and DeviceNix](11-hosts-and-devicenix.html)).

| Condition | Today |
|---|---|
| Claim | **Built**: `benix-claim-agent`, end to end on a VM |
| Node agent | **Partial**: the executor `venue-node` (chapter 6), without signed placements or grants |
| Registry binding | **Draft**: Venue today is one daemon with a file registry and bearer tokens |
| Host profile | **Draft** |

## Claiming

`benix-claim-agent` is a public repo that implements device claim: a `TPair` state machine, a LAN endpoint, and TPM binding. It straddles two layers. The state machine is BenixOS identity. The TPM, first-boot and `dinit` pieces are DeviceNix. The plan asks for a **root-of-trust provider seam** so a host without a TPM can still claim; it does not exist yet.

**Discovery before claim.** An *unclaimed* box advertises `_benixos._tcp` over mDNS so a client can find it. `benix-mdns-advertiser` does this and works. After claim, discovery is Venue's, which also browses `_venue._tcp`. Machines found by mDNS arrive in Venue **pending**, and are never nodes until an authoritative manager adopts them. `_hearth._tcp` is a discovery signal and **never a trust signal**.

## Identity (contract §2)

- A node **MUST** have a device key. Trust is never self-declared: the registry records the key, never a node's claim about itself.
- At claim the node pins the **owner's public key** and the owner's account-log head. That pin is the root of every offline check.
- The claim produces **one owner-signed binding record**. It pins, as separate keys, the registry key, the distribution signer and the release channel, and it assigns the node's **roles**. Neither a channel nor mDNS can assign a role.
- A node **MUST NOT** accept an identity assertion from Keycloak or any realm as an input to a grant check.
- Where a TPM exists, the node SHOULD hold the TPM `lockoutAuth` as random, discarded bytes.

State: the device key and claim are partly built; the owner's account log is **Draft** (the log format is proposed, and `account_id` still equals the Keycloak id).

## Registry binding (§4)

At claim the owner binds the node, by signature, to **exactly one authority registry** and pins that registry's key.

- Other registries may attach as *consumers*. They must not place work on the node. Federation is out of scope.
- The registry key is **separate from the registry's TLS key**.
- The owner key and device-root material **must not live on the registry host**.
- **If the registry is unreachable**, existing leases run to expiry under each workload's partition policy, and **no new placement happens**.

## Roles and classes

The owner-signed record assigns **roles**; a placement's group label is checked against them. Venue uses a role as a placement constraint (*where*); the agent checks it (*whether*).

Two node classes:

| Class | Holds leases | Examples |
|---|---|---|
| **Full** | yes, hosts services | DeviceNix box, Ubuntu server, macOS (reduced) |
| **Client** | **no** | Phones, tablets, Windows until its transport exists. Hold keys, present grants, show the shell. |

## What the agent must not hold (§3.3)

The node agent MUST NOT hold: device-root material or the TPM `lockoutAuth`; unlock keys or session memory of any person; household or operator signing keys; Keycloak admin credentials; upstream service credentials; ssh keys to other nodes; an exec or shell path; policy loaded from the network; or any call to a Lockamy service.

## Update and supervision

- **Two speeds.** The host image (DeviceNix, A/B with a health-gated commit) and components (versioned containers and Kits). A node MUST NOT be able to brick itself: a rollback MUST have been demonstrated on a host profile before it claims "native host".
- **Supervision** is a supervisor-agnostic contract: a start command, required environment, a health signal, readiness and watchdog signalling. A `dinit` unit, a `systemd --user` unit and a `launchd` job are thin wrappers. On DeviceNix the agent is a **native service, not a container**.

> [!warning] A conflict the draft has not resolved
> The contract says the agent runs as a **dedicated non-root user** under **rootless Podman**, and is **not in the `docker` group**. The compose bundle that exists today puts the executor in a container with the **Docker socket mounted**, which is root-equivalent on the host. This is an open decision. See [The security model](14-security-model.html).

## Conformance

The first node conformance tests are the M1 and M2 milestone exit tests ([Status and roadmap](15-status-and-roadmap.html)): a path-spelling table, placement signature and fencing checks, and a partition-policy exercise. A `node-conformance` suite is meant to live in `spec-kit`, beside the Hearth suite. Neither exists.

## Next

[6. Venue](06-venue.html)
