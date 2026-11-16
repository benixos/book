---
title: "8. The gateway and services"
---

# 8. The gateway and services

> [!info] State
> **Gateway: Built and live.** The split into a node agent and a smaller gateway is **Draft**.

## What the gateway is

The per-device **fabric edge** of a household. Today one process does all of this:

- speaks Hearth to a hub (the fabric edge),
- exposes household resources (the resource provider),
- runs services in containers (the service runtime),
- installs services (the installer),
- normalises namespace paths,
- and checks capabilities.

It runs with no hub, in a local-only mode.

## What it becomes

The Venue node agent takes **resource provision and placement enforcement**. The gateway keeps an **optional cross-network router** plus **system administration and user management**.

| Role | Today | After |
|---|---|---|
| Hub aggregation and routing | gateway | gateway |
| Install request and consent | gateway | gateway |
| Grant minting | gateway | owner-signed, through the signer ([Presenter trust](14-presenter-trust.html)) |
| Service runtime | gateway | node agent |
| Placement enforcement | none | node agent |
| Scheduler | not built | Venue's planner |
| Local hub role | gateway (discovery only) | the hub binary's local mode |

It stays one repository and one install command, as two units.

## Service glues

A **glue** is a service adapter. It exposes an upstream service, such as a media server, a home-automation hub, a DNS filter or a camera system, as nodes in the namespace. Glues are service adapters, not gateway features.

**A glue must bind loopback and require authentication.** It is reachable only by the node agent, with a token required off loopback.

## The service catalog

The catalog holds service manifests: data only. It is the de facto package format.

## The namespace operations

The gateway speaks a namespace protocol: **walk, read, write, invoke, watch, manifest**. It is **experimental and not frozen**. It is planned to move into the system tree as a separate spec with a Hearth `payload_type` binding. It is BenixOS's equivalent of Plan 9's file operations over a household.

## Next

[9. Distribution](09-distribution.html)
