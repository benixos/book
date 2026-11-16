---
title: "7. Grants and enforcement"
---

# 7. Grants and enforcement

> [!info] State
> **Executor policy v0: Built**, default-deny. It is a local policy, not a grant system.
>
> **Owner-signed grants: Draft.** A prototype of the typed-address rule exists. Nothing on the grant path is built to the node contract.

BenixOS enforces authority **at the resource**, not at the edge. The node agent is where scope, attenuation and revocation are checked.

## The grant model

There is one grant system:

- **Owner-signed, per-grantee, typed** *use* and *egress* grants, issued by the device-root holder and **verifiable offline**.
- Venue reads them through a `Grants` trait. Scheduler caller caps are not grants.
- The issuer chain is **device-root holder, then attenuated delegate, then member**, verified offline. An identity provider authenticates the person to the consent step and is **never an input to a node's check**.

### Three rules for the grant path

1. **Grants name typed resources and match segment by segment.** A grant is never matched against a raw string.
2. **An address is parsed once into a typed value** that rejects every non-canonical spelling. The gate, the proof-of-possession signature and the executor all consume that one value.
3. **The executor builds upstream requests from typed segments** with per-segment encoding, then **asserts** scheme, host, port, base prefix and segment count. Unknown means deny.

The spellings a parser must survive include `//`, `.`, `..`, `%2e`, `%2f`, double encoding, `\`, `?`, `#`, `;`, case variants, Unicode, control characters and empty segments.

### Attenuation and revocation

- Attenuation may **only narrow**: fewer operations, a longer prefix, an earlier expiry. It is checkable offline.
- Revocation is **short-lived grants plus a node-local revocation list**. The revocation SLA is the grant's TTL.

## Consent and grant requests

An owner approves a grant through consent that an app cannot forge. The loader signs a **grant request**, a presenter shows it from its own template, and after a fresh gesture a separate **signer** issues the grant ([Presenters](13-presenters.html)). The signer holds only an attenuated delegate key and re-derives the consent text from the request bytes.

## Placement checks

For each placement the agent checks:

1. the **signature**, made with the registry key;
2. the registry **incarnation**;
3. that the **revision exceeds a high-water mark persisted on disk**;
4. that the **lease is live** by the agent's own monotonic clock;
5. that the **grants verify offline** and cover the work;
6. that the spec fits **node-local policy**.

Any failure refuses the placement. The **fencing token** is `(registry key id, incarnation, hold revision)`, minted by the registry. A restored registry starts a new incarnation, and the owner re-anchors nodes.

### Partition policy

Each workload declares what happens if the node loses its registry.

| Policy | Behaviour |
|---|---|
| **replace** | The replacement starts only after the old lease has expired plus a clock-skew margin |
| **hold** | Keep running until the authority returns |
| **self-stop** | Stop when the lease ends |

"Unknown" refuses new work. It never kills running work by itself.

## Executor policy v0

The executor's policy is **local to the node** and read once at start. Unknown keys are an error. **Nothing runs until the owner allows an image by digest.**

| Control | Behaviour |
|---|---|
| Image | Only an owner-allowed image. A tag is always pulled; a digest only if absent |
| Privilege | Privileged mode refused. All capabilities dropped. `no-new-privileges` |
| Docker socket | A workload that asks for `docker.sock` is refused |
| Mounts | Any host-path mount is denied. Named volumes are the next step |
| User | A fixed non-root uid. The policy cannot allow the executor's own uids |
| Filesystem | Read-only root |
| Network | A dedicated user-defined bridge with inter-container traffic disabled. Egress is open |
| Resources | Limits applied |
| Refusals | Reported with the exact rule id; nothing is created |

The executor acts only on containers that carry the managed label, this node's name **and this install's random instance id**. A foreign or old container is never touched.

## Not yet built

- Owner-signed grants. The executor's local policy stands in for them.
- Signed placements. The executor trusts `venued` over a token.
- The typed-address library on the live path.

## Next

[8. The gateway and services](08-gateway-and-services.html)
