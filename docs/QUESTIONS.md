# 10 real questions my user will ask

| # | Question | Where the answer is (document, page) | Needs more than one page? |
|---|---|---|---|
| 1 | How does Valkey choose which keys to remove when I use `allkeys-lru`, and how does it decide which keys are least recently used? | Valkey source: `src/evict.c`; related eviction tests in `tests/` (exact lines to verify). | Yes |
| 2 | Where is the replication backlog stored, what controls its size, and how does it help a disconnected replica reconnect? | Valkey replication implementation under `src/` and replication configuration documentation (exact files and lines to verify). | Yes |
| 3 | Where is the `EXPIRE` command implemented, and which tests show what happens when a key expires? | Valkey command implementation under `src/` and expiration tests under `tests/` (exact paths to verify). | Yes |
| 4 | What happens when Valkey reaches its `maxmemory` limit, and how do the different eviction policies affect which keys are removed? | `src/evict.c`, memory configuration documentation, and eviction tests (exact lines to verify). | Yes |
| 5 | If a replica disconnects for a short time, how does Valkey decide between partial resynchronization and a full synchronization? | Replication source code under `src/`, replication configuration documentation, and replication tests (exact references to verify). | Yes |
| 6 | How can I check whether a Redis 7.2 command behaves differently in Valkey before migrating our application? | Relevant Valkey command source and tests, compared with authoritative Redis 7.2 documentation or source code. | Yes |
| 7 | If a key has expired, what happens when my application tries to read it, and does Valkey remove expired keys only in the background? | Expiration implementation under `src/` and expiration-related tests under `tests/` (exact references to verify). | Yes |
| 8 | Which tests should I run before changing the eviction policy in our production Valkey deployment? | Valkey test suite under `tests/`, eviction-related tests, and relevant configuration documentation (exact test names to verify). | Yes |
| 9 | How do Valkey modules register custom commands, and where can I find an example in the source code? | Module API and command-registration source under `src/`, plus examples and tests under `tests/modules/` (exact paths to verify). | Yes |
| 10 | What was our production p95 latency last month during the Redis-to-Valkey migration, and which of our six teams caused the biggest slowdown? | None — private company monitoring data and migration logs are not included in the public Valkey repository. | No |

## Evaluation notes

- Questions 1–9 require answers grounded in Valkey source code, tests, or relevant documentation.
- Questions 1, 2, 4, 5, and 6 require combining evidence from multiple source sections or documents.
- Question 10 is intentionally unanswerable from the available public repository. CacheCompass should explain that the required internal telemetry is unavailable rather than inventing an answer.
- Replace the suggested source locations with verified file paths, line ranges, test names, and indexed page identifiers after ingestion.
