---
title: "10. Data and identity"
---

# 10. Data and identity

> [!info] State
> **Storage Kit: alpha.** The encryption seam is in a draft change. The volume driver is a proof of concept.
>
> **Identity Kit: alpha**, with a stub family graph and an unbuilt authorization engine.

## Storage

### Storage Kit

A content-addressed binary storage engine:

- **BLAKE3** addressing,
- **FastCDC or fixed-size chunking** with recursive fragmentation,
- **Zstd-compressed packfiles**,
- **per-partition isolation and dedup**, with async local, S3 and HTTP backends.

The address of record is `(partition_id, content_id)`. Partitions are created explicitly. The interface is locked and gated by a conformance suite in CI. It is pre-1.0.

**Not yet:** the key-and-encryption seam, which would move the on-disk format to v4, and tiered or cached block storage.

### Volume driver

A FUSE mount and Docker volume plugin over Storage Kit. It is a **proof of concept**, and it is needed before *stateful* placement. Until then BenixOS is **stateless-only**: the executor has no storage for workloads. A workload's storage will be a typed, owner-granted resource, never a host path.

## Identity

| Piece | Role |
|---|---|
| **Identity Kit** | The client library: `ServicePrincipal`, `Account`, `FamilyMember`, `FamilyRole`, an OIDC client; module `claim` |
| **`ServicePrincipal`** | A **plain grant-holding subject with no persisted circle or tier**. A household is *emergent*: the set of principals holding grants on shared resources, never a stored role |
| **Identity provider** | Authenticates a person to the consent step |
| **Claim** | Binds a device to an owner ([Nodes](05-nodes.html)) |

### The rule that matters

**An identity provider authenticates a person. It is never an input to a node's grant check.** Grants are owner-signed and verified offline ([Grants and enforcement](07-grants-and-enforcement.html)).

For a hosted deployment, a standard identity provider is the back end. A local household deployment needs a local realm, a link table and signed logs.

### Not yet built

- The **family graph** is a stub.
- The **authorization engine** is unbuilt.
- The **owner's account log**, which the node pins at claim, is a proposed format.

## Next

[11. Hosts and DeviceNix](11-hosts-and-devicenix.html)
