---
type: concept
title: "8. The gateway and services"
created: 2026-11-15
updated: 2026-11-15
tags: [benixos, book, gateway, glue, service-catalog, hub]
status: draft
---

# 8. The gateway and services

> [!info] State
> **Gateway: Built and live**, private source (Apache-2.0 licensed). A 12-crate Rust workspace with 266 tests as of 11 November 2026, and released binaries. **No gateway image and no compose file.** The split into a node agent and a smaller gateway is agreed in principle and **Draft** in detail.

## What the gateway is today

The per-device **fabric edge** of the household. One process does all of these:

- **fabric edge** (talks to the hub, speaks Hearth),
- **resource provider** (the "virtual cluster"),
- **service runtime** (`docker_runtime.rs`),
- **installer** and app store,
- **namespace normaliser**,
- **capability gate** (`qr-cap`).

Crates include `qr-gateway`, `qr-cap`, `qr-web`, `qr-cli`, `qr-remote` and the `qr-glue-*` service glues. It runs with no hub: with `HUB_URL` unset it logs "fabric edge disabled (local-only)".

## What it becomes

The plan: the Venue resident agent takes **resource provision and placement enforcement**. The gateway keeps an **optional cross-network router** plus a **system-administration and user-management layer**.

| Role | Today | After |
|---|---|---|
| Hub aggregation and routing | gateway | gateway |
| Install request and consent | gateway | gateway |
| Grant minting | gateway (`qr-cap`) | **owner-signed**, through a separate thin layer; the gateway must not hold a key that acts as a household key |
| Service runtime | gateway (`docker_runtime.rs`) | **node agent**, behind a runtime trait first; migration to `substrate-kit` later |
| Placement enforcement | none | node agent |
| Scheduler (item D) | **not built** | **absorbed by Venue's planner** |
| Local hub role | gateway, only mDNS shipped | the **hub binary's local mode** |

It stays **one repo and one install command**, but two units: a node agent and the gateway.

## Service glues

A **glue** is a service adapter: it exposes an upstream service (Home Assistant, an HTTP service, Pi-hole, Frigate, Jellyfin) as nodes in the namespace. Glues are **service adapters, not gateway features.**

| Glue | Notes |
|---|---|
| `qr-glue-ha` | Home Assistant |
| `qr-glue-http` | Generic HTTP |
| `qr-glue-pihole`, `qr-glue-frigate` | Dockerfiles in the gateway repo |
| Jellyfin | Has live tests; manifest drift across three copies |

**Glue must bind loopback and require auth.** The plan makes glue reachable only by the node agent, with a token required off loopback.

## The service catalog

`service-catalog` holds **11 manifests**, data only. It is the de facto package format. Debts it carries: only 1 of 16 is provisionable in the distribution schema (the rest are connectors), 20 floating artifacts including every glue image, and no manifest declares `provides`, `requires`, consumers or a publisher. The images for the HA and HTTP glues are hosted privately, so an outside reader cannot build them.

## The namespace op-set (`qr-proto`)

The gateway speaks a namespace protocol: **walk, read, write, invoke, watch, manifest**. It is **experimental and not frozen**. The plan is to extract it into the system tree as a separate spec with a Hearth `payload_type` binding. It is the BenixOS equivalent of Plan 9's file operations over a household.

## The gateway-led MVP, and why it was set aside

The first bootstrap plan proposed **MVP-A**: a gateway bundle. The project then chose **Venue first** ([Venue](06-venue.html)), which delivers the actual BenixOS shape (place, run, lease, ledger on one node). The gateway, glue and Jellyfin become **workloads Venue places** rather than the vehicle. The Venue-led route also builds from source for anyone, because `venue-kit` has only public dependencies, whereas the gateway depends on privately hosted crates.

## Next

[9. Distribution](09-distribution.html)
