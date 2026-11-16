---
title: "14. Presenter trust"
---

# 14. Presenter trust

> [!info] State
> **Draft.** A prototype exercises the design: a supervisor with a compositor, a sandboxed renderer per instance, and a separate signer, with an owner-signed roster. **No build earns full trust**, and the gaps are listed at the end.

An app must never be able to make a presenter show something that the presenter treats as trusted. This chapter covers how a presenter is built to keep that true. How a presenter fits into the system is in [Presenters](13-presenters.html).

## What a presenter is made of

On a full-trust host a presenter is not one program. A **supervisor** spawns the parts and the channels between them.

| Part | Job | Trusted? |
|---|---|---|
| **Compositor** | Owns the screen, the input and the consent layer; draws window chrome from attested identity | Yes, and small |
| **Renderer** | Parses an app's tree and lays it out; one per app instance | **No** |
| **Signer** | Holds the delegated key and issues grants after consent | Yes, as a separate process |

The **renderer is outside the trusted base**, because it parses untrusted input. It is a separate process per instance and a client of the compositor. It receives only inherited descriptors, sets itself up, and then confines itself:

- its own user, process, mount, network, IPC and host-name namespaces;
- an empty read-only root and no capabilities;
- a filesystem and network sandbox, and a system-call filter.

**It refuses to run unsandboxed.** A hostile tree, a decode bomb or garbage bytes kill only that instance's renderer.

Two rules follow from the split:

- **Identity is bound to the stream** the supervisor hands the compositor, not to a process id. A process id cannot identify a process the supervisor spawned.
- **Trust signals are drawn by the shell, never the renderer.** The "no direct connection" banner is one.

The renderer shares the user's id for now, and a compromised renderer can still attack the compositor through the display protocol, so the compositor's protocol surface stays in the trusted base.

## The trust path

Consent is built outside the app:

1. The loader or node **signs a grant request**: "component D on node N requests typed resource R, these operations, this TTL".
2. The presenter verifies it against the roster, checks the owner's admission, and parses R **once** to a canonical value.
3. The presenter renders the consent from **structured fields in reserved chrome**. The compositor owns the labels and layout and re-validates everything.
4. After a **fresh user gesture**, a separate **signer** issues the grant.

Minimums for the spec:

- The presenter holds only an **attenuated delegate key**, inside a **separate signer** that re-derives the consent text from the grant bytes.
- The **consent kind is reserved.** Any app tree containing it is refused.
- **Consent is fields, never a sentence.** Free text cannot be made safe, because a name inside it can read as part of the request. Names pass a profile: normalised, a restricted character set, a single script, no look-alike characters, and distinct from one another.
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
- **No build earns full trust yet.** A headless compositor and a sandboxed renderer show the layering is right. Still missing: a physical input path (input devices, display master and virtual-terminal gating), a signer under a separate user id, a separate user id and resource limits per renderer, owner-key rotation, roster roles and enrollment, and a second implementation passing the golden vectors.
- **The signer and the presenter share verification code**, including the roster verifier, in the prototype. Production needs independent implementations.

## Next

[15. The security model](15-security-model.html)
