---
title: "14. The security model"
---

# 14. The security model

> [!info] State
> **A design with a small built core.** Built: the executor's default-deny policy, container identity and lease handling, and a signed-channel prototype with throwaway keys. **Draft:** owner-signed grants, signed placements, sealing of node messages and typed addresses. This page summarises the design; it is not a threat model.

## Principles

1. **A placement is not an authorization.** The registry decides where; the node agent decides whether.
2. **Authority is checked at the resource**, from owner-signed grants verifiable offline.
3. **Default deny.** Unknown means deny. "Unknown" refuses *new* work and never kills running work by itself.
4. **Trust is never self-declared.** The registry records a node's key, never a node's claim about itself.
5. **Separate keys for separate jobs:** owner key, registry key, distribution signer, release channel and device key.
6. **The owner key and device-root material never live on the registry host.**
7. **No identity provider is an input to a grant check.**
8. **The transport is untrusted, and never an authorization input.** A channel or mirror is static files, the hub carries sealed frames, and a direct path bypasses the hub's revocation check.
9. **An app never emits anything a presenter treats as trusted.** Consent is built outside the app.

## Trust boundaries

| Boundary | What crosses | Control |
|---|---|---|
| Client to hub | Sealed payloads, roster reads | Sessions, proof of possession, sealing; the roster is attested |
| Hub to node | Sealed frames | The seal proves only "some household device", so the registry signature goes **inside** |
| Registry to node | Placements | Signed with the registry key; checked for incarnation, high-water mark, lease and grants |
| App to `venued` | Holds | A bearer token selects a manager; class caps and grants apply |
| Executor to Docker | Container specs | Local default-deny policy; the socket only in the executor |
| Node to upstream service | Invokes | Typed addresses; scheme, host, port and prefix asserted |
| Publisher to node | Releases | Threshold signatures, freshness, no rollback, hash and length |
| Loader to presenter | App frames | An origin binding (node key, component digest, placement id, nonce) signed inside the sealed payload |
| Presenter to signer | Grant requests | The signer re-derives the consent text from the bytes and issues single-use challenges |

## Threats and controls

| Threat | Control | State |
|---|---|---|
| **The executor is host root.** It holds the Docker socket | Default-deny policy; the socket in one container only; an optional filtering proxy | Partial |
| **A stolen executor token** | The NodeAgent class cannot place or start anything. It can read the specs on its node and report status | The token does not expire |
| **A stolen app token** | Limited to that manager's caps and grants; every workload still passes local policy | Built |
| **A stolen publisher key** | Cannot make anything run: the owner's admission is needed | Prototype |
| **Path spellings that slip a grant** | Parse once into a typed value; assert the upstream request | Draft |
| **Replay of a placement** | Fencing token, registry incarnation, a high-water mark on disk | Draft |
| **A partitioned registry** | Partition policy per workload; no new placement | Draft |
| **Remote code execution over the LAN, by design** | Pinned TLS and a token suit the owner's own machines only; signed placements and grants come first | Mutual-TLS link built, simulated only |
| **A workload escapes or exfiltrates** | Read-only root, dropped capabilities, non-root uid, isolated network | Built; egress is open |
| **Binary services have no sandbox** | A separate process group and cleared environment only | Gap |
| **A hostile component** | No ambient authority; bounded CPU and memory; one process per instance | Prototype |
| **A hostile tree crashes the presenter** | A non-recursive wire form, with depth and size enforced while reading | Draft |
| **An app fakes a consent screen** | The consent kind is reserved; consent is rendered from the presenter's own template | Draft |
| **In-app phishing** (chrome shows who, not what) | A rule is needed: presenter-owned secret inputs or a visible warning | Gap |
| **A compromised presenter lies about what it showed** | A trusted display path from the host's secure UI | Gap |
| **A tag re-pushed to different bytes** | Pin the manifest digest at admission | Draft |

## Next

[15. Status](15-status.html)
