# MatchLens

**Understand the chances behind the scoreline.**

MatchLens is a soccer analytics project that will help fans explore match statistics, shot maps, and AI explanations supported by event data. Its central question is: **What do the scoring chances tell us beyond the final score?**

**Status: early development.** The current version is a command-line match analyzer with unit tests. The dashboard, visualizations, and AI question-answering features are planned, not implemented.

## What works today

- Load one historical Premier League match from local StatsBomb JSON files.
- Display the teams, date, official score, and event count.
- Calculate shots, shot-derived goals, and total expected goals (xG) by team.
- Exclude penalty shootout events while retaining extra-time events.
- Report missing xG separately from genuine zero values.
- Flag differences between shot-derived goals and the official score for investigation.
- Run five unit tests using synthetic events without downloading match data.

The first selected match is Leicester City vs Chelsea, played on 14 December 2015. This project currently uses historical data; it does not provide live or current-season coverage.

## Planned experience

A fan selects a match, explores its shot map, and asks questions such as:

- Which team created higher-quality scoring chances?
- How does the chance quality compare with the final score?
- Which players had the best opportunities?

Answers will reference calculated statistics and acknowledge missing evidence. Python will perform the calculations; the AI will explain the results.

The first release targets a small collection of Premier League 2015/16 matches, a team filter, a shot map, and a few supported match questions. Player activity heatmaps are optional. Current-season Premier League, Champions League, and La Liga coverage depends on verifying an appropriate data source and its terms.

## Run locally

The project is developed on Windows with Python 3.13.17. The current implementation uses only Python's standard library: no package installation or API key is required.

### 1. Clone and create an environment

In PowerShell:

```powershell
git clone https://github.com/kbhreddy/matchlens.git
cd matchlens
py -3.13 -m venv .venv
```

Repository access requires authorization while the repository is private. If you already have a checkout and `.venv`, skip this step. Commands below use the environment's Python directly, so activation is optional.

### 2. Obtain the data

Raw match files are intentionally excluded from Git. Review the provider's terms and the pinned sources, checksums, and attribution notes in [data/SOURCE.md](data/SOURCE.md) before downloading.

For a permitted local download, run these commands from the project root in PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path data/raw/matches/2, data/raw/events | Out-Null
$sourceRevision = "4b73468fc5b0f1950f9f66fada70ad3a4f9327cb"
$sourceBase = "https://raw.githubusercontent.com/hudl/open-data/$sourceRevision/data"
Invoke-WebRequest -Uri "$sourceBase/matches/2/27.json" -OutFile data/raw/matches/2/27.json
Invoke-WebRequest -Uri "$sourceBase/events/3754013.json" -OutFile data/raw/events/3754013.json
```

Do not commit raw files or credentials. The analyzer reports a missing-file message if the local data has not been downloaded.

### 3. Run the analyzer

```powershell
.\.venv\Scripts\python.exe match_analysis.py
```

### 4. Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Tests use hand-made events and do not require the raw files. They cover team totals, ignored non-shot events, shootout exclusion, missing xG, and teams with zero shots.

## How it works

```text
Local match list + event JSON
              |
       Load and find match
              |
    Select non-shootout shots
              |
   Accumulate per-team statistics
              |
       Print match summary
```

`summarize_shots()` separates calculations from display logic so the same function can later support the dashboard and AI feature.

```text
match_analysis.py             Loader, calculations, and CLI output
tests/test_match_analysis.py  Unit tests using synthetic events
data/SOURCE.md               Source revision, download instructions, and terms notes
data/raw/                    Local data; excluded from Git
PROJECT_PLAN.md              Scope, milestones, and release criteria
```

## Metric definitions and limitations

- **xG:** the source model's estimated scoring probability for a shot. Team xG is the sum of available per-shot values, displayed to two decimal places. Missing values are reported separately.
- **Interpretation:** total xG is not a win probability or proof that a team deserved to win. Multiple shots in a rebound sequence also require context when interpreting the sum.
- **Official score vs shot goals:** own goals and data inconsistencies can create differences; a mismatch needs investigation.
- **Shots on target:** not implemented yet. The calculation will follow the provider's documented outcomes.
- **Validation:** the current calculation expects the source's event structure and known team names. Broader input validation remains future work.
- **Heatmaps:** a future event-location heatmap would show recorded actions, not continuous player movement.

## AI engineering approach

AI assists development, but changes are reviewed and verified with executed code and tests. The planned in-app AI feature will be evaluated on fixed cases for factual correctness, unsupported claims, missing-data handling, response time, and API cost. No AI evaluation results are claimed yet.

Before integration, the project must resolve the source-data terms for sending derived facts to a third-party API. Deployment and public live API access also require data-use review and spending controls. No API integration or deployed demo exists yet.

## Data attribution

Match data source: **Hudl StatsBomb Open Data** — [official repository](https://github.com/hudl/open-data).

The data has its own [user agreement](https://github.com/hudl/open-data/blob/master/LICENSE.pdf); it is not covered by any license for this project's code. See [data/SOURCE.md](data/SOURCE.md) for the recorded terms and unresolved questions. Published analysis must include the required StatsBomb attribution and official logo. Raw data is not redistributed in this repository.

## Next milestones

1. Define and test shots on target.
2. Build the first shot map and interactive dashboard.
3. Add evidence-based match questions and evaluate AI answers.
4. Gather user feedback, document measured results, and prepare a demo.

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for the complete plan.
