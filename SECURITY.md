# Security policy

## Supported versions

Only the latest release on the `main` branch receives security fixes.

## Reporting a vulnerability

Please **do not open a public issue** for security problems.

Report privately by email to **kneblewskitomasz@gmail.com** with:

- a short description of the problem and its impact,
- the input text (or a minimal reproduction) that triggers it,
- the version / commit you tested.

You can write in English or Polish.

## What counts as a security issue here

`siatka` is a safety filter that runs in front of a household voice assistant. Its only input is
untrusted user text. We treat the following as security issues:

- a crash, exception or hang on any input (an emergency message would not be shown),
- catastrophic backtracking / ReDoS in any pattern,
- an input that silently bypasses a crisis, violence, medical-emergency or child-safety rule
  that the test suite says should match.

## Response

We aim to acknowledge a report within 7 days and to publish a fix, with credit if you want it,
once it is verified by a regression test.
