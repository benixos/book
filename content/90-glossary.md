---
title: "Glossary"
---

# Glossary

| Term | Meaning |
|---|---|
| **Admission** | An owner-signed record saying a service may exist on a node. No admission, no run |
| **Authority registry** | The one Venue registry a node is bound to for placement |
| **BenixOS** | The distributed OS: one namespace, identity, placement and storage across a person's or household's nodes |
| **Channel** | A folder of signed release files, served by any web server; not trusted |
| **Claim** | Binding a device to an owner: pins the owner key and produces a signed binding record |
| **Client node** | A node that holds keys and presents grants but hosts no services and holds no leases |
| **Conformance suite** | Tests a Hearth implementation, or a node, must pass |
| **D (message)** | A server-pushed Hearth message with `tag = 0` |
| **DeviceNix** | The native host distro |
| **Distribution** | A named bundle of services resolved to a lock and published on a channel |
| **Envelope** | The single Protobuf message on every Hearth frame |
| **Executor** | The process that follows `venued`'s feed and runs containers |
| **Fencing token** | `(registry key id, incarnation, hold revision)`, minted by the registry |
| **Full node** | A node that hosts services |
| **Glue** | A service adapter that exposes an upstream service as nodes in the namespace |
| **Grant** | An owner-signed, typed, attenuable, offline-verifiable permission to use or egress a resource |
| **Hearth** | The open wire protocol for distributed personal resources |
| **High-water mark** | The highest registry revision a node has accepted, persisted on disk |
| **Hold** | A Venue reservation: place, start, renew, release |
| **Hub** | The server that routes Hearth sessions |
| **Incarnation** | A registry's restore generation |
| **Kit** | A library that owns one domain, with an API others build on |
| **Lease** | The time a hold or placement stays valid, judged by the node's own monotonic clock |
| **libbenix** | The portable primitive library |
| **Lock** | The self-contained, hash-identified plan a distribution compiles to |
| **Manager** | A Venue principal with its own token and caps: Authoritative, NodeAgent, Consumer, Observer or Untrusted |
| **Node** | A claimed machine or container running a node agent |
| **Node agent** | The resident process that decides *whether* a placement runs |
| **Node contract** | The document everything else is specified against |
| **Owner** | The person whose key was pinned on the node at claim |
| **Partition policy** | Per workload: *replace*, *hold* or *self-stop* if the registry is lost |
| **Placement** | A Venue decision about where work runs. Not an authorization |
| **PoP** | Proof of possession of a device key |
| **R (message)** | A server response to a T, with the same tag |
| **Registry key** | The key the registry signs placements with; separate from its TLS key |
| **Release id** | The hash of a lock's contents |
| **Roster** | The household's list of devices, attested and read by devices |
| **Role** | An owner-signed assignment of what a node may do |
| **Sealed payload** | An end-to-end encrypted Hearth payload that the hub cannot read |
| **T (message)** | A client request; the server answers with exactly one R or `RError` |
| **Tag** | The per-message correlation id |
| **Typed address** | A resource address parsed once into a typed value that rejects non-canonical spellings |
| **Venue** | The registry, planner and ledger for places work can run |
| **`venued`** | Venue's daemon: JSON over HTTP, a token per app, a long-poll event feed |
