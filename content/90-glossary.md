---
title: "Glossary"
---

# Glossary

| Term | Meaning |
|---|---|
| **Admission** | An owner-signed record saying a service may exist on a node. No admission, no run |
| **Authority registry** | The one Venue registry a node is bound to for placement |
| **BenixOS** | The distributed OS: one namespace, identity, placement and storage across a person's or household's nodes |
| **Casement** | The reference window-class presenter. A server, not a Kit |
| **Channel** | A folder of signed release files, served by any web server; not trusted |
| **Claim** | Binding a device to an owner: pins the owner key and produces a signed binding record |
| **Client node** | A node that holds keys and presents grants but hosts no services and holds no leases |
| **Component** | A WebAssembly component: the primary form of an app written against Kits |
| **Compositor** | On a full-trust host, the small trusted program that owns the screen, the input and the consent layer |
| **Conformance suite** | Tests a Hearth implementation, or a node, must pass |
| **Consent** | A grant approval shown by a presenter from its own template, never by an app |
| **D (message)** | A server-pushed Hearth message with `tag = 0` |
| **DeviceNix** | The native host distro |
| **Distribution** | A named bundle of services resolved to a lock and published on a channel |
| **Envelope** | The single Protobuf message on every Hearth frame |
| **Executor** | The process that follows `venued`'s feed and runs containers |
| **Fencing token** | `(registry key id, incarnation, hold revision)`, minted by the registry |
| **Full node** | A node that hosts services |
| **Full-trust host** | A host where the presenter is the compositor, so consent cannot be covered or faked |
| **Glue** | A service adapter that exposes an upstream service as nodes in the namespace |
| **Grant** | An owner-signed, typed, attenuable, offline-verifiable permission to use or egress a resource |
| **Grant request** | A signed statement that a component on a node requests a typed resource, operations and a TTL |
| **Hearth** | The open wire protocol for distributed personal resources |
| **High-water mark** | The highest registry revision a node has accepted, persisted on disk |
| **Hold** | A Venue reservation: place, start, renew, release |
| **Hub** | The server that routes Hearth sessions |
| **Incarnation** | A registry's restore generation |
| **Kit** | A library that owns one domain, with an API others build on |
| **Lease** | The time a hold or placement stays valid, judged by the node's own monotonic clock |
| **libbenix** | The portable primitive library |
| **Loader** | The per-host process that runs a component, one process per instance, and attests its digest |
| **Lock** | The self-contained, hash-identified plan a distribution compiles to |
| **Manager** | A Venue principal with its own token and caps: Authoritative, NodeAgent, Consumer, Observer or Untrusted |
| **Node** | A claimed machine or container running a node agent |
| **Node agent** | The resident process that decides *whether* a placement runs |
| **Node contract** | The document everything else is specified against |
| **Owner** | The person whose key was pinned on the node at claim |
| **Partition policy** | Per workload: *replace*, *hold* or *self-stop* if the registry is lost |
| **Peer link** | The direct, mutually authenticated connection between two devices on a LAN |
| **Placement** | A Venue decision about where work runs. Not an authorization |
| **PoP** | Proof of possession of a device key |
| **Presenter** | The server that renders an app's interface, routes input and mediates consent |
| **Presenter class** | *Window class* (multi-window) or *pane class* (a single pane) |
| **Presenter spec** | The open specification of what an app may say to a presenter |
| **R (message)** | A server response to a T, with the same tag |
| **Reduced-trust host** | A host that offers only a user-presence prompt: grants are read-only and short-lived |
| **Registry key** | The key the registry signs placements with; separate from its TLS key |
| **Release id** | The hash of a lock's contents |
| **Renderer** | The unprivileged process that parses an app's tree and lays it out; one per instance, outside the trusted base |
| **Role** | An owner-signed assignment of what a node may do |
| **Roster** | The household's list of devices, attested and read by devices |
| **Sealed payload** | An end-to-end encrypted Hearth payload that the hub cannot read |
| **Signer** | The separate process, holding an attenuated delegate key, that issues grants after consent |
| **Supervisor** | The launcher that spawns the signer, the compositor and the renderers and creates the channels between them |
| **T (message)** | A client request; the server answers with exactly one R or `RError` |
| **Tag** | The per-message correlation id |
| **Trusted display path** | The presenter's ownership of the display and input path, so a compromised app or presenter cannot fake what the user sees |
| **Typed address** | A resource address parsed once into a typed value that rejects non-canonical spellings |
| **Venue** | The registry, planner and ledger for places work can run |
| **`venued`** | Venue's daemon: JSON over HTTP, a token per app, a long-poll event feed |
