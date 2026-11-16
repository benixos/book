---
type: concept
title: "14. The security model"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, security, threat-model, trust]
status: draft
---

# 14. The security model

> [!info] State
> **A design with a small built core.** The built parts are the executor's default-deny policy, container identity and lease handling, and a signed-channel prototype with throwaway keys.
>
> The rest is **Draft**: owner-signed grants, signed placements, sealing of node messages and typed addresses.
>
> Independent reviews of the executor and the multi-node link found problems that were then fixed. The latest round judged the multi-node stack not yet ready for real services. This page summarises; it is not a threat model.

## The principles

1. **A placement is not an authorization.** Where is Venue's; whether is the node agent's.
2. **Authority is checked at the resource**, from owner-signed grants verifiable offline.
3. **Default deny.** Unknown means deny; "Unknown" refuses *new* work and never kills running work by itself.
4. **Trust is never self-declared.** The registry records a node's key, never a node's claim about itself.
5. **Separate keys for separate jobs.** Owner key, registry key (separate from the registry's TLS key), distribution signer, release channel, device key.
6. **The owner key and device-root material never live on the registry host.**
7. **No identity provider is an input to a grant check.**
8. **The untrusted thing is the transport.** A channel or mirror is static files; the hub carries sealed frames.

## The trust boundaries

| Boundary | What crosses | Control |
|---|---|---|
| Client to hub | Sealed payloads, roster reads | Sessions, PoP, sealing; the roster is attested |
| Hub to node | Sealed frames | The seal proves only "some household device", so the registry signature goes **inside** |
| Registry to node | Placements | **Draft**: signed with the registry key, checked for incarnation, high-water mark, lease, grants |
| App to `venued` | Holds | Bearer token to a manager; class caps and grants |
| Executor to Docker | Container specs | Local default-deny policy; the socket only in the executor |
| Node to upstream service | Invokes | Typed addresses, asserted scheme, host, port and prefix |
| Publisher to node | Releases | Threshold signatures, freshness, no rollback, hash and length |

## The threats that drive the design

| Threat | Mitigation | State |
|---|---|---|
| **The executor is host root.** It holds the Docker socket. | Default-deny policy; the socket only in one container; an optional filtering `socket-proxy` profile | Partial; the proxy was never run |
| **A stolen executor token** | NodeAgent class cannot place or start; it can read specs on its node and write false status | **Open**: the token never expires and there is no rotation |
| **A stolen app token** | Limited to that manager's caps and grants; every workload still passes the executor's local policy | Built |
| **A stolen publisher key** | Cannot make anything run: the owner's admission is needed | Prototype |
| **Path spellings that slip a grant** (`..`, `%2e`, `//`, `\`, `;`) | Parse once into a typed value; assert the upstream request | **Draft**; the current gateway matches grants by path prefix |
| **Replay of a placement** | Fencing token, registry incarnation, a high-water mark on disk | **Draft** |
| **A partitioned registry** | Partition policy per workload; no new placement | **Draft** |
| **The LAN executor is remote code execution by design** | Pinned TLS plus a token is acceptable for the owner's own boxes only; signed placements and grants come before anyone else uses it | Rule recorded; mTLS link **built, simulated only** |
| **A workload escapes or exfiltrates** | Read-only root, capabilities dropped, uid 10100, `icc=false` network | Built; **egress is still open** |
| **A container on Docker Desktop reaching host loopback** (including `venued`) | None | **Untested** |
| **Binary services have no sandbox** | None beyond own process group and cleared environment | Gap |

## What the independent reviews found

The executor's security and QA reviews were answered and mostly fixed. Still open or partial: the raw Docker socket is the default; workload egress is open; the executor token never expires; and an image `VOLUME` still gives a writable anonymous volume with no quota.

The multi-node weekend added two review rounds. The first round rejected one patch and one tool as written, and the fixes landed. **The second round, on fresh eyes, judged the stack not yet ready for a machine that hosts real services.** Those findings went back for another pass. The review rule held throughout: the reviewer is never the implementer.

## The review gate

Grant-path code needs an independent review, mutation evidence that each check is load-bearing, and a request-recording mock proving a refused request reached no upstream. It applies to all of the node agent's code, which is also kept **private**.

## Decisions that are policy, not engineering

Real key custody; a floor that a node cannot be pinned to a software key for rollback; who holds the registry signing key; CA key custody for the node tunnel; a firewall for the tunnel port; whether the Docker socket is acceptable in a container or rootless Podman is required; and every action that touches a real shared machine.

## Next

[15. Status and roadmap](15-status-and-roadmap.html)
