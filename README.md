# Next Generation AI — DIA1-G2

ESILV, *Trustworthy Generative AI* module (Next Generation AI), Data & AI major, year 4.
Repository of sub-group **DIA1-G2**, used from TD 1 to TD 3.
Course pack: `2026-10-18-students-1` (kit of 14 October 2026).

## Members

| Member | Role in TD 1 |
|---|---|
| Oryssa Stella TALATALA | A — GPT-OSS 120B (Groq) |
| Jolan NALLET--PANG | B — GPT-OSS 20B (Groq); trace consolidation; TD 1 analysis |
| Cecilia Sessi DOSSA | C — Cohere North Mini Code (OpenRouter) |
| Tony THEBAUD-PERRIER | D — Qwen3.8-27B (Groq) |
| Hugo HOUPPE | E — Dots3-Note Preview (OpenRouter); TD 1 analysis |
| Pierre-Olivier WAFO BAKAM | F — reference cross-checks, consolidation, repository |

Protocol roles: A to E each operate one model (20 calls); the other members cross-check the references and consolidate the traces. Each session report (`reports/`) details individual contributions.

## Repository layout

```
.
├── README.md
├── .gitignore                  keeps keys, .env files, virtual environments and local outputs out
├── skeleton-multi-llm-en.py    orchestrator: prompt, calls, SQL sandbox, verdicts, traces
├── sandbox_sqlite.py           read-only SQL execution
├── check_access.py             environment and model-access check
├── verify-data.py              database integrity check
├── check_references.py         references C01-C20: SQL execution + independent computation on the CSV files
├── atelier-vote.py             TD 2 workshop
├── atelier-routage.py          TD 2 workshop
├── modeles-autorises.json      configuration: models, parameters, limits (read by the code)
├── schema.sql                  schema sent to the models
├── questions-td1.json          the twenty questions
├── manifest.json               kit file fingerprints
├── data/                       boutique.sqlite database and CSV files (never modify)
├── docs/                       kit assignments, protocol, guides and materials
├── reports/
│   └── td1.md                  TD 1 session report
└── TD1/
    ├── reference-td1.csv       20 reference queries, values and checker
    ├── prompts-en.md           system message and user template, as used
    ├── traces/                 raw traces: state-A..E.jsonl, traces-A..E.csv, merged traces-td1.*
    └── results/                model/question comparison, five-model summary, pivot view
```

Code, configuration and `data/` stay at the root: the kit scripts look for them next to themselves.
Each TD has its own folder (`TD1/`, then `TD2/`, `TD3/`); reports are in `reports/`.

## Data

Database `data/boutique.sqlite`, seed 20260925, identical for every sub-group.
SHA-256: `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`.

## Environment

Python 3.10 or later; `requests` package (only for the network checks of `check_access.py`).
Everything else uses the standard library only.

```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\python.exe -m pip install requests

# macOS / Linux
python3 -m venv .venv
.venv/bin/python -m pip install requests
```

On Windows, replace `python` with `.venv\Scripts\python.exe` in the commands below if the environment is not activated; on macOS/Linux, use `python3`.

## Replay the TD 1 work (no API key, no network)

From the root of a fresh clone:

```bash
# 1. Database and environment integrity
python verify-data.py
python check_access.py --no-network

# 2. The 20 references: SQL on the database + independent computation on the CSV files
python check_references.py

# 3. Offline re-execution of every SQL query returned by the models, compared with our references
python skeleton-multi-llm-en.py --replay TD1/traces/traces-td1.jsonl --reference TD1/reference-td1.csv --state replay-check.jsonl --out replay-check.csv

# 4. Rates per model
python skeleton-multi-llm-en.py --rates --state replay-check.jsonl
```

Expected result of step 4: GPT-OSS 120B 20/20, GPT-OSS 20B 19/20, Qwen3.8-27B 14/20, Cohere North Mini Code 13/20, Dots3-Note 12/20.
Replayed rows carry `nature = replay`; the `replay-check.*` files are excluded from the repository by `.gitignore`.

## Run real calls again (optional)

Requires Groq (Free plan) and OpenRouter (`:free` models only) accounts. Keys stay in environment variables, never in a repository file.

```powershell
$env:GROQ_API_KEY = "..."
$env:OPENROUTER_API_KEY = "..."
python skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b --cases C01,C02 --reference TD1/reference-td1.csv --state new-experiment-A.jsonl --out new-experiment-A.csv
```

Use new `--state` and `--out` files: the traces in `TD1/traces/` must not be modified. A new call may give a different result or hit a rate limit (HTTP 429).

## Progress

| TD | Date | Status | Report |
|---|---|---|---|
| TD 1 — compare | 2026-10-21 | 100 cells run (106 calls); Qwen C18 and C20 not executed after two HTTP 429 | [reports/td1.md](reports/td1.md) |
| TD 2 — vote and route | 2026-11-18 | upcoming | |
| TD 3 — quantify and decide | 2026-12-11 | upcoming | |

## Security

No API key, password or `.env` file in this repository. Keys are set locally as environment variables.
