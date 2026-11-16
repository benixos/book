---
type: reference
title: "Glossary"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, glossary]
status: draft
---

# Glossary

Terms are as the project defines them on 15 November 2026. A term marked *(draft)* comes from a draft document.

| Term | Meaning |
|---|---|
| **Admission** | An owner-signed record saying "this service, from this publisher, as this class, may exist" on a node. No admission, no run. Chapter 9. |
| **Advertisement freshness** | How a node's liveness is judged: recency of its advertisement, not `DPresence`. *(draft)* |
| **Authority registry** | The one Venue registry a node is bound to for placement. *(draft)* |
| **BenixOS** | The distributed OS: one namespace, identity, placement and storage across every node a person or household owns. |
| **Channel** | A folder of signed release files (nightly, beta, stable) served by any web server; not trusted. |
| **Claim** | Binding a device to an owner: pins the owner key and produces a signed binding record. |
| **Client node** | A node that holds keys and presents grants but hosts no services and holds no leases. |
| **Conformance suite** | Tests a Hearth implementation, or a node, must pass. Neither exists yet. |
| **D (message)** | A server-pushed Hearth message with `tag = 0`. |
| **DeviceNix** | The BenixOS-native host distro; Yocto in `slash-builder/core`. |
| **Distribution** | A named bundle of services with roles and host support, resolved to a lock and published on a channel. |
| **Envelope** | The single Protobuf message on every Hearth frame. |
| **Executor** | The process that follows `venued`'s feed and runs containers. `venue-node` is its first form. |
| **Fencing token** | `(registry key id, incarnation, hold revision)`, minted by the registry. *(draft)* |
| **Full node** | A node that hosts services. |
| **Glue** | A service adapter exposing an upstream service as nodes in the namespace. |
| **Grant** | An owner-signed, typed, attenuable, offline-verifiable permission to use or egress a resource. *(draft)* |
| **Hearth** | The open wire protocol for distributed personal resources, 9P-inspired. |
| **High-water mark** | The highest registry revision a node has accepted, persisted on disk. *(draft)* |
| **Hold** | A Venue reservation: place, start, renew, release. |
| **Hub** | The server that routes Hearth sessions; Quickring operates the reference one. |
| **Incarnation** | A registry's restore generation; a restored registry starts a new one. *(draft)* |
| **Kit** | A focused library owning one domain, with an API others build on. |
| **Lease** | The time a hold or placement stays valid; judged by the node's own monotonic clock. |
| **libbenix** | The portable primitive library in `benix-base`; candidate node-contract primitives. |
| **Lock** | The complete, self-contained, hash-identified plan a distribution compiles to. |
| **Manager** | A Venue principal class with its own token and caps: Authoritative, NodeAgent, Consumer, Observer, Untrusted. |
| **Node** | A claimed machine or container running a node agent. |
| **Node agent** | The resident process that decides *whether* a placement runs, from grants and local policy. |
| **Node contract** | The document everything else is specified against. v0 is a draft. |
| **Owner** | The person whose key was pinned on the node at claim. |
| **Partition policy** | Per workload: *replace*, *hold* or *self-stop* if the registry is lost. *(draft)* |
| **Placement** | A Venue decision about where work runs. **Not an authorization.** |
| **Profile** | A tiered selection of BenixOS offered by Quickring, at engineering altitude. |
| **PoP** | Proof of possession of a device key. |
| **Quickring** | The commercial operator built on Hearth and BenixOS. |
| **R (message)** | A server response to a T, with the same tag. |
| **Registry key** | The key the registry signs placements with; separate from its TLS key. *(draft)* |
| **Release id** | The hash of a lock's contents. |
| **Roster** | The household's list of devices, attested and read by devices. |
| **Role** | An owner-signed assignment of what a node may do; checked against a placement's group label. *(draft)* |
| **Sealed payload** | An end-to-end encrypted Hearth payload; the hub cannot read it. |
| **Star topology** | One registry host, an executor on every node, outbound-only. |
| **T (message)** | A client request; the server answers with exactly one R or `RError`. |
| **Tag** | The per-message correlation id. |
| **Thunderhead** | The reference-hardware category: Aether (Pi 5, CM5) and Forge (AMD64). |
| **Typed address** | A resource address parsed once into a typed value that rejects non-canonical spellings. *(draft)* |
| **Venue** | The registry, planner and ledger for places work can run. Provisional name. |
| **`venued`** | Venue's daemon: JSON over HTTP, a token per app, a long-poll event feed. |
