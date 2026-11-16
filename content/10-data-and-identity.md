---
type: concept
title: "10. Data and identity"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, storage, identity, keycloak, bitchain]
status: draft
---

# 10. Data and identity

> [!info] State
> **Storage Kit and bitchain: alpha.** Interface-locked with a conformance gate in CI; the encryption seam is in a draft PR. **`bitchain-volume`: a proof of concept**, banked. **Identity Kit: alpha**, with a stub family graph and an **unbuilt authorization engine**. **Keycloak is live**, operated by Quickring.

## Storage

### Storage Kit

A content-addressed binary storage engine (on-disk format v3):

- **BLAKE3** addressing,
- **FastCDC or fixed-size chunking** and recursive fragmentation,
- **Zstd-compressed packfiles**,
- **per-partition isolation and dedup**, with async local, S3 and HTTP backends (the last two are Cargo features).

The address of record is `(partition_id, content_id)`. Partitions are created explicitly (`PartitionStore::create` versus `open`). The older `Context` and `Address` types are retired. It is **interface-locked** with a `spec-kit` conformance gate in CI, and pre-1.0.

**Not yet:** the key-and-encryption seam (draft PR #10, which would move the format to v4), and tiered or cached block storage.

### bitchain

`bitchain` is the content-addressed binary-versioning **CLI**, the first-party consumer of Storage Kit. `refraction` is the hosted storage backend that implements the bitchain block protocol; it is **parked** (27 October 2026).

### bitchain-volume

A **FUSE mount and Docker Volume Plugin** on Linux with dockerd. Its content-addressing core is a thin adapter over Storage Kit since 26 August 2026. It is a **proof of concept**, "off the beta-path focus lock". It is needed before *stateful* placement; until then BenixOS is **stateless-only** (node contract §10.2). Installed on the host as a Docker plugin or a host daemon, it is not something `compose up` starts, and it needs privileged FUSE access.

### What this means for workloads

The executor has **no storage for workloads** in v0: host-path mounts were *removed*, not hardened (chapter 7). Named volumes are the next step. The first real workload, the notes reader, needs a **read-only mount of a typed, owner-granted resource, never a host path** (chapter 12).

## Identity

### What the pieces are

| Piece | Role |
|---|---|
| **Identity Kit** | The client-side library: `ServicePrincipal`, `Account`, `FamilyMember`, `FamilyRole`, an OIDC/AuthN client; module `claim`. 94 tests, two dependents. |
| **`ServicePrincipal`** | A **plain grant-holding subject, no persisted circle or tier**. A household is *emergent*: the set of principals holding grants on shared resources, never a stored role. (Settled 31 August 2026.) |
| **Keycloak** | The IdP. Two realms: one for operators and one for consumer family accounts. |
| **`identity-service`, `identity-infra`** | Quickring's family-graph mutation plane and the Keycloak infrastructure. Live, Quickring-operated. |
| **`benix-claim-agent`** | Device claim; the BenixOS-side identity of a *machine* (chapter 5). |

### The rule that matters for BenixOS

**Keycloak authenticates a human. It is never an input to a node's grant check.** Grants are owner-signed and verified offline (chapter 7). The first plan had user management build on Keycloak and near-fit tools. The narrowed position is that **Keycloak is the back end for the *hosted* deployment only.** A local household deployment needs a local realm, a link table and signed logs. That narrowing is not yet confirmed.

### What is not built

- The **family graph** is a stub.
- The **authorization engine** is unbuilt.
- The **owner's account log**, which the node pins at claim, is a *proposed format*; `account_id` still equals the Keycloak id.
- **Federation** and enterprise SSO are not authorised as a market segment. We avoid generalising into enterprise IAM before that is decided.

## Next

[11. Hosts and DeviceNix](11-hosts-and-devicenix.html)
