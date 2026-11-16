---
type: concept
title: "13. The one-node bundle"
---

# 13. The one-node bundle

> [!info] State
> **Built, not yet published.** The bundle runs on one machine and passed its 133-check exit test on Ubuntu 26.04 (amd64) and on macOS Docker Desktop (arm64, earlier code). It builds against a Venue Kit checkout plus three unmerged patches, and no images are published. This page describes what it does. It is not an install guide.

The one-node bundle is the first way to run the BenixOS placement path. `docker compose up -d` on one machine starts:

- **`venued`**, the Venue API, where reservations are called *holds*;
- **`venue-node`**, the executor, **the only container with Docker access**;
- two short-lived init containers: one creates the registry and mints the executor's token, the other creates the workload network.

A hold followed by a start runs a container, **but only if a local, default-deny policy allows it.**

## What it needs

| Need | Detail |
|---|---|
| Host | A Linux machine (Ubuntu 26.04 amd64 was the verified one) or Docker Desktop on macOS |
| Docker | **Engine 28 or newer.** Older engines let hosts on the same network segment reach ports published on loopback. The executor refuses to start on an older or unknown version unless told to. |
| Node name | **Required, with no default.** A registry created under another name is refused. |
| Docker group id | The host's real `docker` group id on Linux |
| Policy | An owner-written allowlist. **Nothing runs until an image is allowed by digest.** |

## What it does

1. The operator mints a token that selects a manager.
2. The owner puts an image digest on the allowlist and restarts the executor.
3. An app places a hold with a Placement document that carries the workload spec.
4. A start order makes the executor pull the image and run it under the hardening listed in [Grants and enforcement](07-grants-and-enforcement.html).
5. A release removes the container.

A workload that is privileged, mounts `docker.sock`, names a disallowed image, uses a `..` path or a plain relative mount is **refused with the exact rule id, and nothing is created.** The Docker daemon's own event record is the evidence.

## Lifecycle

| Operation | Effect |
|---|---|
| `docker compose down` | Leaves workloads running and the `workloads` network in place |
| `down` then `up` | The executor adopts the same container and keeps its instance id |
| **`down -v`** | **A full reset with a new identity. Running workloads are orphaned**: left alone, not removed |
| Reap orphans | `venue-node reap-orphans` lists them (a dry run) or removes them; tested against stubs only |

## How it is verified

The exit test builds the images, brings the bundle up on a real Docker daemon, and runs 133 required checks. A pass means the script ran to its end, every required check ran, and none failed. Any abort prints a failure. A separate self-test (22 cases, 111 assertions, including negative controls) proves the pass and fail logic against stubs.

The exit test mounts the **real Docker socket** into the executor, so it should only run on a machine where that is acceptable.

## What it does not do

- Run more than one node.
- Sign placements or check owner-signed grants.
- Provide workload storage or restrict workload egress.
- Run on Debian 12, native Linux on arm64, rootless Docker or SELinux; these were not tested.
- Use TLS between `venued` and the executor. It is plain HTTP on an internal network and on loopback.

## Next

[14. The security model](14-security-model.html)
