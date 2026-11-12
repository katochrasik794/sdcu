# Security Policy

SDCU is a local audit suite. It reads the tree you point it at, and it does not phone home. Security reports are about the tool itself: the core engine, the CLI, the agent skills, and the workflows that ship with this repository.

Please report vulnerabilities privately. A public issue or pull request gives every fork the details before a fix exists.

---

## Supported versions

Security fixes land on `main` and ship with the current `0.1.x` line.

| Version | Supported |
| --- | --- |
| `0.1.x` | Yes |
| Older tags and forks | No |

If you are on an old checkout, update to the latest `main` before reporting. Fixes are not backported.

---

## Report a vulnerability

Use one of these private channels:

| Channel | Where |
| --- | --- |
| **GitHub Security Advisory** | [Open a private advisory](https://github.com/katochrasik794/sdcu/security/advisories/new) |
| **LinkedIn** | [Rasik Katoch](https://www.linkedin.com/in/rasik-katoch-29b66b365/) |

GitHub advisories are the preferred path. They stay private until a fix is released. Use LinkedIn if advisory creation is unavailable.

Include:

1. A short description of the issue and the impact you expect.
2. The SDCU version or commit (`git rev-parse HEAD`) and the command you ran.
3. A minimal repro: files, flags, and the output that shows the problem.
4. Whether the issue needs a local file, a crafted path, or a dependency the tool shells out to.

A proof of concept against your own checkout is enough. Do not include data from a codebase you do not own.

---

## What happens next

| Step | When |
| --- | --- |
| Acknowledgement | Within 3 business days |
| Initial assessment | Within 7 business days of acknowledgement |
| Fix or declined report | As soon as the assessment is clear; you will hear either way |
| Public disclosure | After a fix is on `main`, or after 90 days, whichever comes first |

If the report is accepted, you will get credit in the release notes unless you ask to stay unnamed. If it is declined, the reply will say why: not a vulnerability, already known, or outside the scope below.

There is no bug bounty.

---

## Scope

**In scope**

- `packages/core` and `packages/cli`, including argument handling, path traversal, and anything the CLI executes
- `skills/` content that instructs an agent to take an unsafe action
- Install scripts, GitHub Actions, and other files a user is expected to run
- A dependency pin in this repo that is known to be exploitable through normal SDCU use

**Out of scope**

- Findings inside [`examples/vulnerable-app`](examples/vulnerable-app). Those files are intentional fixtures so `sdcu audit` has something to flag.
- Scanner results that only restate an SDCU checkpoint (a secret in a sample, a wildcard CORS line, a string-built SQL query) without a flaw in the scanner itself.
- Issues that require the user to already be running untrusted code on their own machine.
- Social-engineering attempts against maintainers.
- Volumetric traffic against GitHub, or denial of service against a local `sdcu` process.

Third-party advisories in `networkx`, `rich`, Node, or Python belong upstream. Still send a note if a released SDCU install is exposed through one of them.

---

## Disclosure

Keep the details private until a fix is on `main` or the 90-day window above has passed. After that, a GitHub Security Advisory will describe the impact, the fixed commit, and the workaround if one exists.

Good-faith research against your own copy of this repository is welcome. Do not access anyone else's data, and do not disrupt services you do not own.
