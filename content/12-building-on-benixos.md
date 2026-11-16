---
title: "12. Building on BenixOS"
---

# 12. Building on BenixOS

> [!info] State
> **App Context Kit: alpha.** How a third party would package and publish an app is **Draft**.

## What can run on a node

| Kind | Delivered as | State |
|---|---|---|
| **A container** | An OCI image pinned by digest | **Built**: the executor runs it under local policy |
| **A binary** | A signed artifact, only if the operator allows | **Prototype**, in the distribution mechanism |
| **A service behind the gateway** | A glue plus the upstream service | **Built**, outside Venue |

A workload's language is not the OS's concern. The OS runs it.

## App Context Kit

One spec, two implementations (a Dart core with a Flutter companion, and a Rust crate), both held to **shared conformance fixtures**. It gives an app:

- an **identity**,
- **directories and settings**, with **test and scratch modes**,
- a **roster presence** entry,
- a **Venue session**, and
- **opt-in peers**.

## Other Kits an app composes

| Need | Kit |
|---|---|
| Talk to the household | Fabric Kit over Message Kit |
| Place work on a machine | Venue Kit |
| Store content | Storage Kit |
| Know who someone is | Identity Kit |
| Run a gated agent task | Errand Kit |
| Local model inference | Inference Kit |
| UI | Interface Kit |
| A workflow strip | Work Strip Kit |

## What a workload needs from the node

A small, read-only web service is a useful test of the mechanism. It forces the gaps that matter.

| Needs | What the node must provide |
|---|---|
| A directory mounted **read-only** | A typed, owner-granted resource, **never a host path** |
| A **secret file** | Secrets delivery: not an environment variable, a command line or an image layer |
| **Exposure with no network** | The node proxies a Unix socket to loopback or the fabric |
| An image to **pin by digest** | A registry whose manifest digest a lock can name |
| An **unprivileged user** | The node's own user, not a uid baked into the image |

## Next

[13. The security model](13-security-model.html)
