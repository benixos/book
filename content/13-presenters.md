---
title: "13. Presenters"
---

# 13. Presenters

> [!info] State
> **Draft.** The design is settled in outline, and a draft spec marks each requirement as tested, specified, or required but not built. A local prototype has exercised it end to end: a sandboxed app, a loader, a presenter core, a separate signer, an owner-signed roster, a LAN peer link and a headless compositor. **No presenter ships yet, and no build earns full trust.**

Apps do not draw. They describe their interface in terms of meaning, and a **presenter** renders it. The presenter owns widgets, layout, text editing, accessibility, theming, the window tree, focus and input routing. It also mediates the clipboard, drag and drop, and capture.

This is the BeOS `app_server` ownership model, cut at semantics instead of drawing commands.

## The presenter spec

The **presenter spec** is open and owned by BenixOS. It defines what an app may say and what a presenter must do with it.

- **Semantic only in v1.** Apps send a tree of meaningful elements, not pixels. Canvas and surface tiers are deferred extensions, each needing its own review.
- **Scenes, not windows.** A window-class presenter maps a scene to an OS window. A pane-class presenter maps it to a navigation destination.
- **Responsive layout is mandatory**, so one tree serves both classes.
- **Conformance profiles** are negotiated per mounted view: Core first, then Canvas, Surface and Windowing.
- **Text editing, scrolling and list pulls happen inside the presenter.** The app sees commits.

The **headless presenter core** is Apache-2.0 and shared by every presenter. It is a library with a small C interface, so a shell in any language can host it.

## Presenter classes

| Class | Shape | Examples |
|---|---|---|
| **Window class** | Multi-window; owns the window tree | A desktop shell on Linux (as a compositor), macOS and Windows |
| **Pane class** | A single pane; compact layout with a back bar | A phone or a single-pane desktop view |

**Casement** is the reference window-class presenter. It is a server, not a Kit. A pane-class presenter must be implementable from the presenter core alone.

## What goes on the wire

Almost all of the spec is application-layer payload. It adds **no Hearth envelope variant**, so the count stays at 24.

- **Kinds are namespaced and versioned**, for example `benixos.list/1`. Each carries a `fallbacks[]` chain, unknown properties are ignored, and a *must-understand* flag marks kinds that cannot be skipped. A consent view is must-understand and never falls back.
- **Never on Hearth:** GPU textures, file descriptors, handles, encoded video, fonts and glyph atlases, embedded bitmaps, raw pointer streams, and patches retained as history.

A prototype found requirements the spec must state:

| Requirement | Why |
|---|---|
| **The tree's wire form is non-recursive**: a flat pre-order list with explicit depth | A recursive decoder can be crashed by a deeply nested frame far below the size cap. Size caps alone do not protect |
| **Every patch and event carries a base revision** | The presenter can detect a gap |
| **A credit window**, counted in patches and bytes | The app cannot outrun the presenter |
| **Snapshot, then deltas.** Resync is re-requested until it succeeds, and no credit is granted while out of sync | A single lost resync request otherwise livelocks a lossy link |
| **Snapshot retries use stop-and-wait with exponential backoff and jitter** | A jitterless retry loop makes congestion worse |
| **Input is idempotent**, with a client sequence number, and some classes are droppable | Retries and drops must be safe |
| **Signed objects use a strict deterministic encoding** with bounded depth and size, verified over the received bytes and never re-encoded | Two independent implementations must agree, and a signature must not depend on re-encoding |
| **An unknown topic looks the same as a hidden endpoint**, and still gets one terminal reply | Probing cannot map what exists, and no caller hangs |

## Where the traffic flows

The **hub** carries signalling and low-rate control: session control, presence, push-wake, grant requests and rendezvous. **Interactive view traffic never rides the hub.** It takes a direct path:

| Where | Path |
|---|---|
| On the box | The local bus |
| On the LAN | A mutual-TLS 1.3 peer link whose identity is the device key, checked against the owner-signed roster; no certificate authority |
| Across the WAN | A WebRTC data channel, with a relay as fallback |

All three carry the same sealed envelopes. A hub is tuned for household state, not for interactive streams.

If no direct path exists, the presenter shows the **last cached snapshot, read-only, with a visible "no direct connection" state**. A class of view that cannot degrade this way is refused.

**Transport is never an authorization input.** A direct path bypasses a hub's revocation check, so authority comes only from grants. A remote message does not carry its sender's identity in the base transport, so the peer-link provider checks a signed sender device id against the authenticated device and drops mismatches. That is attribution, never authorization.

Work remaining on the wire is additive: carrier profiles for the peer link and the data channel, a device-key peer-authentication arm on the session hello, and a push-wake registration field. The first scope is the LAN and BenixOS; the WAN comes later.

```mermaid
flowchart TB
  subgraph NODE["Node (runs the app)"]
    APP["App<br/>Wasm component"] --- LDR["Loader<br/>attests the component digest"]
  end
  subgraph DEV["Device (shows the app)"]
    PRES["Presenter<br/>window or pane class"]
    SIG["Signer<br/>attenuated delegate key"]
    PRES -- "consent shown, then grant requested" --> SIG
  end
  LDR == "direct path: local bus, LAN peer link, WebRTC" ==> PRES
  HUB["Hub<br/>signalling and control only"]
  HUB -.- PRES
  HUB -.- LDR
```

## The trust path

An app must never emit anything that a presenter treats as trusted. Consent is therefore built from outside the app:

1. The loader or node **signs a grant request**: "component D on node N requests typed resource R, these operations, this TTL".
2. The presenter verifies it against the roster, checks the owner's admission, and parses R **once** to a canonical value.
3. The presenter renders the consent text **from its own template, in reserved chrome**.
4. After a **fresh user gesture**, a separate **signer** issues the grant.

Minimums for the spec:

- The presenter holds only an **attenuated delegate key**, inside a **separate signer** that re-derives the consent text from the grant bytes.
- The **consent kind is reserved.** Any app tree containing it is refused.
- **App identity is the loader-attested component digest**, never the descriptor's title, shown in chrome an app cannot draw.
- Every cross-node view stream carries an **origin binding** (node key, component digest, placement id, nonce) signed inside the sealed payload.
- **Clipboard, drag and drop, and capture are one-shot grants** bound to a user gesture.

Each minimum has a conformance fixture. For example, a fake consent descriptor from an app must be refused, and a recording mock proves the signer was never called.

The open window shell must be a **complete, conformant consent implementation**. Consent correctness cannot depend on any other presenter.

Grants are short-lived (draft values): at most an hour, or 15 minutes on a reduced-trust host, and delegations at most 30 days. Revocation is the short lifetime plus an owner-signed revocation list with a monotonic serial, exchanged on every peer-link handshake. **Revoking a device ends its live sessions**, not only its future handshakes.

### The trusted display path

A presenter that is fully compromised can lie about what it displayed. The defence is for the presenter to own the display and the input path.

- A **full-trust host** is one where the presenter is the compositor. It draws the consent layer above everything, and no client receives input during a prompt.
- A host that only offers a user-presence prompt proves *that* someone consented, not *what* they saw. It is a **reduced-trust host**: grants there are read-only with a short ceiling, and anything wider is confirmed on a full-trust device.

The grant records the host's trust class, and the spec states what it requires of each.

### Known gaps

- **Chrome shows who is asking, not what.** An app can still draw a convincing "enter your password" screen that passes validation. The spec needs a rule: presenter-owned secret inputs, or a visible warning on app-owned fields.
- **No build earns full trust yet.** A headless compositor prototype shows the layering is right. It still needs a physical input path, a signer running under a separate user id, attestation keyed by process handle, one unprivileged renderer process per instance, and structured consent fields.
- **The signer and the presenter share verification code**, including the roster verifier, in the prototype. Production needs independent implementations.

## Next

[14. The security model](14-security-model.html)
