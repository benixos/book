---
type: concept
title: "7. Grants and enforcement"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, grants, capabilities, policy, security]
status: draft
---

# 7. Grants and enforcement

> [!info] State
> **Two systems, one built and one designed.**
> - **Executor policy v0**: **Built** in `venue-node`, default-deny, exercised by the real-Docker exit test. It is a *local policy*, not a grant system.
> - **Owner-signed grants** (node contract §6): **Draft**. A `resource-addr` spike prototypes the typed-address rule. Nothing grant-path is built to the contract.

BenixOS enforces authority **at the resource**, not at the edge. The node agent is where scope, attenuation and revocation get checked. That is why capability enforcement is treated as the same track as hardening Venue, not a separate priority .

## The grant model (design)

One grant system (contract §6):

- **Owner-signed, per-grantee, typed** *use* and *egress* grants, issued by the device-root holder and **verifiable offline**.
- Venue reads them through its `Grants` trait. `StaticGrants` is for tests only. `authority.yaml` holds scheduler caller caps, **not** grants.
- The issuer chain is **device-root holder, then attenuated delegate, then member**, verified offline. Keycloak authenticates the human to the consent step and **is never an input to the node's check**.

### Three rules for the grant path

1. **Grants name typed resources and match segment by segment.** A grant MUST NOT be matched against a raw string.
2. **An address is parsed once into a typed value** that rejects every non-canonical spelling. The gate, the proof-of-possession signature and the executor all consume that one value.
3. **The executor builds upstream requests from typed segments** with per-segment encoding, then **asserts** scheme, host, port, base prefix and segment count. Unknown means deny.

### Attenuation and revocation

- Attenuation may **only narrow**: fewer operations, a longer prefix, an earlier expiry. It must be checkable offline.
- Revocation is **short-lived grants plus a node-local revocation list**. The revocation SLA is the grant's TTL.

### Placement checks (§5.3)

For a placement the agent MUST check:

1. the **signature** (registry key);
2. the registry **incarnation**;
3. that the **revision exceeds a high-water mark persisted on disk**;
4. that the **lease is live** by the agent's *own* monotonic clock;
5. that the **grants verify offline** and cover the work;
6. that the spec fits **node-local policy**.

Any failure refuses the placement. The **fencing token** is `(registry key id, incarnation, hold revision)`, minted by the registry. A hub ULID is never a fencing token or evidence of order. A restored registry starts a new incarnation and the owner re-anchors nodes.

### Partition policy (§5.5)

Each workload declares what happens if the node loses its registry:

| Policy | Behaviour |
|---|---|
| **replace** | The replacement starts only after the old lease has expired plus a clock-skew margin |
| **hold** | Keep running until the authority returns |
| **self-stop** | Stop when the lease ends |

"Unknown" refuses new work and **must not kill running work by itself**.

## What exists today

### `qr-cap` in the gateway: live, being reworked

Proof-of-possession signing over the path, with grants held as **household-wide prefix records** in the gateway's consent file. The plan is to rework it into a typed-address enforcement library. The path-spelling set the library must survive includes `//`, `.`, `..`, `%2e`, `%2f`, double encoding, `\`, `?`, `#`, `;`, case variants, Unicode, control characters and empty segments.

### Executor policy v0: built, default-deny

The executor's policy is **local to the node**, read once at start, and unknown keys are an error. **Nothing runs until the owner allows an image by digest.** The policy table has 69 rows (`POLICY-V0.md`). What the real run verified:

| Control | Result |
|---|---|
| Image | Only an owner-allowed image; a disallowed image is refused. A tag is **always pulled**; a digest only if absent. |
| Privilege | **Privileged mode refused.** All capabilities dropped. `no-new-privileges`. |
| Docker socket | A workload that asks for `docker.sock` is refused. |
| Mounts | **Any host-path mount is denied** (rule P5). Traversal and plain relative mounts are refused. Named volumes are the unbuilt next step. |
| User | Workloads run as **uid 10100**. The policy cannot allow uids 10000 or 10001. |
| Filesystem | Read-only root filesystem. |
| Network | A dedicated user-defined `icc=false` bridge. **Egress is still open.** |
| Resources | Limits applied (pids, memory). |
| Refusals | Reported with the **exact rule id**; the daemon's own event record shows nothing was created. |

### Ownership and identity of containers

The executor acts only on containers carrying the managed label, **this node's name, and this install's random instance id**. A foreign or old container is never touched. `down -v` creates a new identity and **orphans** the previous workloads: they are left alone, not removed.

## The review gate

Grant-path code is subject to a **review gate** (priorities §6), intended to live in a PR template: an independent review, mutation evidence that each check is load-bearing, and a request-recording mock that proves the upstream received nothing on a refused request. The M1 milestone's exit test is built on it.

## Gaps, stated plainly

- No owner-signed grant exists yet. The executor's local policy stands in.
- No placement is signed. The executor trusts `venued` over a token.
- The typed-address library is a prototype, not the gate.
- The executor's token never expires; its NodeAgent class can read every workload spec on its node and write false status for them, but cannot place or start anything.

## Next

[8. The gateway and services](08-gateway-and-services.html)
