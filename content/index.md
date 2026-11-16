---
title: The BenixOS Book
---

# The BenixOS Book

BenixOS is a distributed operating system. It is composed of Kits, speaks the Hearth protocol, and runs on any host that meets a small node contract. This book describes its design, what exists today, and what is still open.

> [!warning] Early, and mostly unreleased
> Most of the code described here is not published, and several pieces are drafts. Each chapter opens with a **State** box that says what is built and what is not. Status is as of 15 November 2026. See [About this book](about.html).

![BenixOS system architecture: applications, Kits, system servers, node contract and wire, node runtime, hosts, hardware](assets/benixos-system-architecture.svg)

## Contents

### What it is
1. [What BenixOS is](01-what-benixos-is.html): the plan in one sentence, the vocabulary, the lineage
2. [Architecture](02-architecture.html): the layers, the three planes, who trusts whom

### Foundations
3. [Hearth](03-hearth.html): the wire contract
4. [Kits](04-kits.html): the framework layer and the catalog

### The system
5. [Nodes](05-nodes.html): what makes a machine part of BenixOS
6. [Venue](06-venue.html): the registry, the planner and the executor
7. [Grants and enforcement](07-grants-and-enforcement.html): who may run what, and how that is checked
8. [The gateway and services](08-gateway-and-services.html)
9. [Distribution](09-distribution.html): signed releases of service bundles
10. [Data and identity](10-data-and-identity.html)

### Underneath and on top
11. [Hosts and DeviceNix](11-hosts-and-devicenix.html)
12. [Building on BenixOS](12-building-on-benixos.html): apps, workloads, the first workload

### Practice
13. [The one-node bundle](13-one-node-bundle.html)
14. [The security model](14-security-model.html)
15. [Status and roadmap](15-status-and-roadmap.html)
16. [Open questions](16-open-questions.html)

### Reference
- [Glossary](90-glossary.html)
- [About this book](about.html)
