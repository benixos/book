---
title: "12. Building on BenixOS"
---

# 12. Building on BenixOS

> [!info] State
> **Wasm components: Draft.** A prototype runs a component with no ambient authority under a loader. **Containers: Built.** **App Context Kit: alpha.** How a third party would package and publish an app is Draft.

## What can run on a node

| Kind | Delivered as | For | State |
|---|---|---|---|
| **A Wasm component** | An OCI artifact, pinned by manifest digest | **Apps written against Kits** (the primary form) | Draft |
| **A container** | An OCI image, pinned by digest | Ported software | **Built**: the executor runs it under local policy |
| **A system binary** | An artifact signed by the system | Components of BenixOS itself | Prototype |
| **A service behind the gateway** | A glue plus the upstream service | Existing household services | **Built**, outside Venue |

A container's contents are the OS's business only at the boundary. An app written against Kits is a component.

## An app is a component

A component is a single artifact, about 100 KB for a minimal one, built with the standard toolchain for `wasm32-wasip2`. It runs with **no ambient authority**:

- The filesystem, environment, arguments and network are denied.
- The clock is allowed, by design.
- CPU is bounded by fuel, and memory by a cap.

The app's **only way out** is one endpoint on the node-local bus. It sends and receives opaque frames, and the grammar of those frames is the [presenter spec](13-presenters.html). Frames speak the gateway's namespace operations, so an app reaches household resources the same way any other client does.

```text
interface endpoint {
  send: func(frame: list<u8>);
}

world app {
  import endpoint;
  export start: func();
  export deliver: func(frame: list<u8>);
}
```

The model is reactive: the loader calls `deliver` for each frame. Clocks and randomness stay as standard imports. WASI 0.3 is ratified, but the Rust toolchain for it is not ready, and the app model does not need async yet.

### The loader

A per-host **loader** runs one process per component instance.

- **A crash or a spin kills only that process.** A sibling app keeps serving.
- **Identity is attested.** The loader hashes the exact bytes it loads and checks the kernel-reported peer credentials of the connection.
- **Round trips across the node-local bus are fast enough for interactive use.** Launch time is dominated by compilation, which a cache would remove.

### Packaging

A component is an **OCI artifact**: an empty config, a wasm layer and a detached signature layer. Registry and digest pinning is the whole distribution story for components.

**Pin the manifest digest at admission, not the tag.** A tag can be re-pushed with a publisher's valid signature and point at different bytes. The digest still names the original.

## App Context Kit

One spec, held to shared conformance fixtures. It gives an app:

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
| A workflow strip | Work Strip Kit |

An app's interface is not a Kit. The app describes it, and a [presenter](13-presenters.html) renders it.

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

[13. Presenters](13-presenters.html)
