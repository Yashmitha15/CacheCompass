# CacheCompass

> AI-powered source-code research for Valkey, with verified answers and fair LLM quotas for every team.

## Problem

Platform engineers migrating internal services from Redis to Valkey need reliable answers about command behavior, eviction policies, replication, and compatibility differences. Searching hundreds of source files and tests manually is time-consuming, and general-purpose LLMs can generate answers without sufficient code evidence. Shared LLM quotas also create a problem because one team's heavy usage can exhaust the available resources for everyone. CacheCompass retrieves relevant source code, generates answers with citations, fact-checks claims against code and tests, and enforces separate usage quotas for each team.

## Who it is for

- Platform engineers at payments companies migrating internal services from Redis to Valkey.
- Backend and infrastructure engineers investigating database behavior, replication, memory management, and source-code implementation details.

## Signature feature

A source-grounded AI research agent that verifies technical claims against Valkey code and tests while enforcing independent request and token quotas for each team.

## Hardest problem (my interview story)

The hardest problem is ensuring reliable AI answers while multiple teams share limited LLM resources. The research agent must retrieve the correct source files and tests, provide traceable citations, and flag claims that cannot be verified. At the same time, quota enforcement must remain correct under concurrent requests so that one team's heavy usage cannot bypass limits or unfairly affect other teams. I plan to validate the solution through source-grounding tests, concurrent quota tests, and noisy-team load testing, targeting less than a 10% increase in other teams' p95 latency and zero quota bypasses.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| Valkey source repository | [valkey-io/valkey](https://github.com/valkey-io/valkey) | To be measured | To be measured | BSD-3-Clause; verify applicable notices |
| Valkey test suite | [Valkey tests](https://github.com/valkey-io/valkey/tree/unstable/tests) | To be measured | To be measured | Check repository licensing and applicable notices |

Target: ingest at least 900 source files. Record the actual number of indexed files and extracted pages after ingestion; do not report targets as completed counts.

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

## Run it

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements-dev.txt

# Linux / macOS
cp .env.example .env

# Windows
# copy .env.example .env

uvicorn app.main:app --reload

# In another terminal
curl http://localhost:8000/health
```

## Live link

Coming in Week 2 — update this section once the application is deployed.
