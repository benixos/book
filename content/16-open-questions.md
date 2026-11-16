---
type: question
title: "16. Open questions"
---

# 16. Open questions

> [!info] State
> A list of **choices not yet made**, not a to-do list. Collected from the node contract, the bootstrap plan and the multi-node build. Where the book assumes an answer, the page says so.

## Decisions open

| # | Question | Why it matters |
|---|---|---|
| 1 | **The executor and the Docker socket.** Accept the socket in a container (root-equivalent), a filtering proxy sidecar, a host service, or rootless Podman as the contract requires? | The contract and the shipping bundle disagree |
| 2 | **Does "desktop first" stand?** | Keeps the compositor and the manifest-kit resolver in scope |
| 3 | **Keycloak's scope.** Hosted deployments only, or household deployments too? | Decides whether a household needs a local realm |
| 4 | **The fourteen placement-authority amendments** from the protocol and security reviews | Several narrow the original position |
| 5 | **The first audience** for a one-node bundle | The gateway source is private; publishing an image is a choice |
| 6 | **Whether the distribution mechanism stays parked**, and the nightly channel signing posture | The plan currently says two contradictory things |
| 7 | **Name clearance** for BenixOS and DeviceNix before any public launch | Only a surface-level search has been done |
| 8 | **Venue's name.** Provisional on purpose | A rename touches one constant |

## Questions for the reviewers of the node contract

1. **"Unknown fails closed" versus "never block a local action."** Security review recommends that local actions still require a valid cached grant.
2. How far does the contract bind a **standalone** node with no registry on grant checks?
3. Should the **registry signing key** be held by the owner's device or by the registry host? The contract forbids the owner key on the host, not the registry key.
4. What is the **root-of-trust provider** interface for a host without a TPM?
5. Which host profile counts as "supported" at the two-node milestone? Is a macOS node with no local IPC acceptable?
6. Where do the **conformance suites** live: `spec-kit`, the Hearth repo, or the system monorepo?
7. Does the agent's Hearth endpoint make **`fabric-kit` a dependency** of the agent crate, and is that acceptable?

## Engineering questions

- **Substrate Kit.** Its container spec gained ports, user-defined networks and named volumes in a recent change. Resource limits, secret delivery and label cleanup are still missing.
- **Which container runtime layer wins.** Docker through the executor, the gateway's own runtime, Podman (the app-store Kit and the contract), Substrate Kit, and compose all start containers. The first bootstrap uses Docker only.
- **Stale documentation.** The Hearth `encryption.md` describes a pre-implementation state, and the spec's status header is out of date.
- **The `application-kit` spike** is probably superseded by App Context Kit. Confirm, then fold or archive it.
- **Open multi-node review findings**, and a GPU test that needs a host change.
- **How a second device reaches a hub-less gateway:** the hub's compose bundle, or a local hub role.

## What this book assumes

- The November 2026 vocabulary is final.
- **Venue first** is the current direction, not a gateway bundle.
- The Kit statuses in the registry (7 November 2026) are current.

## Next

[Glossary](90-glossary.html) · [About this book](about.html)
