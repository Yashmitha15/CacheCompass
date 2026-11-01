# Dataset

## Dataset Information

| Field | Details |
|---|---|
| Dataset name | Valkey Source Code |
| Source repository | https://github.com/valkey-io/valkey |
| Download location | `data/raw/valkey/` |
| Git branch | `unstable` |
| File count | 2,054 |
| Licence | BSD-3-Clause (verify individual file and dependency licences) |
| Dataset type | Open-source source code, tests, documentation and utilities |
| Downloaded on | 2026-11-01 |

## Dataset Structure

The downloaded Valkey repository contains the following main directories:

- `src/` - Core source code.
- `tests/` - Test cases.
- `deps/` - Dependencies.
- `utils/` - Utility scripts.
- `design-docs/` - Design documentation.
- `cmake/` - Build configuration files.

## Purpose

This dataset is used by CacheCompass, an AI research assistant that helps developers understand Valkey source code and investigate Redis-to-Valkey migration questions.

The system will retrieve relevant source-code sections and use them to generate answers with supporting references.

## Notes

- The source code was downloaded from the official Valkey GitHub repository.
- The repository is on the `unstable` branch.
- The file count was checked locally and was 2,054 at the time of verification.
- Individual file and dependency licences should be respected.
- Full source code is stored in `data/raw/valkey/`.
- The raw dataset is not committed to the CacheCompass repository.
