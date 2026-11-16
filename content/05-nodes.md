---
title: "5. Nodes"
---

# 5. Nodes

> [!info] State
> **Draft.** The node contract v0 is a 16-section draft that has not had an independent review. The claim flow is **Built**. The node agent exists only in a first, thin form (see [Venue](06-venue.html)).

A **node** is a machine, or a container, that runs a BenixOS **node agent** and has been **claimed** by an owner. The **owner** is the person whose key was pinned on the node at claim.

## What makes a machine a node

1. It runs the node agent as a supervised service.
2. It holds a device key and has completed a claim that pinned an owner key.
3. It is bound to exactly one authority registry, or declares itself standalone.
4. It meets the host profile for its OS ([Hosts](11-hosts-and-devicenix.html)).

## Claiming

Claim binds a device to an owner: a `TPair` state machine, a LAN endpoint, and TPM binding where a TPM exists. A host without a TPM needs a root-of-trust provider seam, which is not built.

**Discovery before claim.** An unclaimed box advertises `_benixos._tcp` over mDNS so a client can find it. After claim, discovery is Venue's. Machines found by mDNS arrive in Venue as *pending* and are never nodes until an authoritative manager adopts them. `_hearth._tcp` is a discovery signal, never a trust signal.

## Identity

- A node **must** have a device key. Trust is never self-declared: the registry records a node's key, never the node's claim about itself.
- At claim the node pins the **owner's public key** and the owner's account-log head. That pin is the root of every offline check.
- The claim produces **one owner-signed binding record**. It pins, as separate keys, the registry key, the distribution signer and the release channel, and assigns the node's **roles**. Neither a channel nor mDNS can assign a role.
- A node **must not** accept an identity assertion from any identity provider as input to a grant check.

## Registry binding

At claim the owner binds the node, by signature, to **exactly one authority registry** and pins that registry's key.

- Other registries may attach as consumers. They must not place work on the node. Federation is out of scope.
- The registry key is **separate from the registry's TLS key**.
- The owner key and device-root material **must not live on the registry host**.
- **If the registry is unreachable**, existing leases run to expiry under each workload's partition policy, and **no new placement happens**.

## Roles and classes

The owner-signed record assigns **roles**, and the agent checks a placement's group label against them.

| Class | Holds leases | Examples |
|---|---|---|
| **Full** | Yes, hosts services | A DeviceNix box, an Ubuntu server, macOS (reduced) |
| **Client** | No | Phones, tablets; they hold keys, present grants and show the shell |

## What the agent must not hold

Device-root material or the TPM `lockoutAuth`; unlock keys or session memory of any person; household or operator signing keys; identity-provider admin credentials; upstream service credentials; ssh keys to other nodes; an exec or shell path; policy loaded from the network.

## Update and supervision

- **Two speeds:** the host image (A/B, with a health-gated commit) and components (versioned containers and Kits). A node must not be able to brick itself: a rollback must be demonstrated on a host profile before it claims "native host".
- **Supervision** is a supervisor-agnostic contract: a start command, required environment, a health signal, and readiness and watchdog signalling. A `dinit` unit, a `systemd` unit and a `launchd` job are thin wrappers. On DeviceNix the agent is a native service, not a container.

## Next

[6. Venue](06-venue.html)
