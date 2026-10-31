# MatchLens — Engineering Plan

## Purpose

MatchLens helps soccer fans interpret scoring chances through match statistics, shot maps, and AI explanations grounded in event data.

The product answers the question “Where did each team create chances, and what does the final score leave out?”

## Implementation status

The command-line analyzer loads Leicester City vs Chelsea, played on 14 December 2015, from local StatsBomb event files. It reports the official score, event count, shots, shot-derived goals, and summed expected goals (xG) for both teams.

Five standard-library unit tests cover team totals, non-shot events, shootout exclusion, missing xG, and teams with zero shots. The analyzer and tests passed verification on 9 November 2026. The README contains local setup and execution instructions.

Dashboard development, shot maps, shots-on-target classification, and application API integration are pending. Release publication requires verification of the current Git state.

## Release roadmap

| Release | Scope | Acceptance criteria |
| --- | --- | --- |
| v0.1.0 | Command-line match analyzer | Reproducible setup, five passing tests, source documentation, reviewed public repository, and tagged release |
| v0.2.0 | Shot visualization | Documented shots-on-target classification, validated shot coordinates, xG-sized markers, distinct goal symbols, and a clear legend |
| v0.3.0 | Interactive dashboard | Match selection, team filtering, metric definitions, and three historical matches |
| v1.0 | Evaluated AI match explanations | Supported match questions, evidence references, response validation, recorded evaluation results, user feedback, and a runnable demo |

Intermediate releases provide reviewable checkpoints. Feature scope may be reduced to preserve correctness and evaluation quality.

## Product requirements

### Match analysis

- Display competition, season, date, teams, and official score.
- Calculate shots, shots on target, shot-derived goals, and total available xG.
- Identify missing values and distinguish full-match totals from filtered results.
- Support a small collection of Premier League 2015/16 matches initially.

### Shot map

- Plot each shot at its documented pitch coordinates.
- Encode xG through marker size and distinguish goals through marker shape.
- Include team labels, attack direction, and a readable legend.
- Support team filtering in the dashboard.
- Make player, minute, outcome, and xG available through an accompanying detail view. Hover interaction depends on the plotting implementation.
- Verify plotted counts against calculated totals. For the selected match, expect 20 shots overall and 11 for Chelsea.

### AI explanations

- Begin with three or four supported questions about the selected match.
- Provide calculated facts and metric definitions as the model's evidence.
- Require answers to identify supporting facts and acknowledge missing information.
- Validate structured responses before display.
- Keep the explanation's scope visible when chart filters change.
- Handle missing credentials, malformed output, timeouts, and provider failures.

### Future extensions

Player filters, event-location heatmaps, additional leagues, current-season post-match updates, and persistent storage are potential extensions. Heatmaps must describe the recorded event types they visualize. Current-season coverage requires verified provider fields, access terms, and costs.

Long-term target competitions are the Premier League, UEFA Champions League, and La Liga. Database selection will follow demonstrated storage and query requirements.

## Architecture and technology

```text
Local source files → load and validate → calculate statistics → dashboard and charts
Calculated facts → versioned prompt → model API → response validation → explanation
```

The existing calculation function remains reusable independently of the interface. Source-specific parsing should produce consistent shot records for visualization and analysis.

| Component | Technology | Status |
| --- | --- | --- |
| Runtime and data loading | Python 3.13, json, pathlib | Implemented |
| Calculation tests | unittest | Implemented |
| Event tables and filtering | pandas | Planned |
| Shot visualization | Matplotlib | Planned |
| Dashboard | Streamlit | Planned |
| AI explanations | Claude API | Planned |
| Version control | Git and GitHub | In use |

AI-assisted development is part of the engineering workflow. Application inference has separate credentials, costs, and evaluation requirements.

## Data provenance and handling

Use StatsBomb Open Data with pinned source revisions. Keep match IDs, retrieval instructions, checksums, and the source agreement reference in [data/SOURCE.md](data/SOURCE.md).

The initial match uses competition ID 2, season ID 27, and match ID 3754013. Raw files reside in Git-ignored `data/raw/`.

Project data handling follows the recorded source-use review. Preserve required StatsBomb attribution and logo in published analysis. Review unresolved third-party API use and deployment questions against the provider's terms before those integrations. Registration status and attribution assets remain outstanding checks.

## Metric definitions and validation

- Total xG is the sum of available per-shot model estimates. Report missing xG separately.
- Retain full precision during calculation and round only for display.
- Explain chance quality with appropriate context for rebound sequences and model uncertainty.
- Derive shots on target from documented source outcomes.
- Obtain the official score from match metadata. Investigate differences from shot-derived goals, including own goals and incomplete records.
- Exclude shootouts from match shot totals and retain applicable extra-time events.
- Verify coordinate bounds and attack direction before plotting.
- Display match date until the source kick-off timezone is established.

## Quality and AI evaluation

Maintain synthetic tests for calculation edge cases and use source-record checks for representative matches. Add targeted tests when new behavior or a specific regression requires them.

For the AI milestone, use approximately ten fixed cases covering draws, missing xG, zero shots, and a winner with lower xG. Record input facts, model, prompt version, structural validity, numerical accuracy, unsupported claims, latency, token usage, and estimated cost.

Compare AI answers with deterministic template summaries. Apply automated checks where practical and a documented human-review rubric for prose. Preserve representative failures and the changes made to address them.

The v1.0 evaluation must report sample size and observed failures. Reviewed release outputs must contain accurate numerical claims and evidence-supported statements, and missing-information cases must acknowledge their limitations. Failure states must be handled clearly.

## Cost and reliability

- Configure an explicit testing budget before application API usage.
- Store credentials in environment variables or deployment secrets.
- Generate answers on explicit user action.
- Bound output length, request duration, and retries.
- Cache against source facts, model, and prompt version.
- Record usage without exposing credentials.
- Apply appropriate request and spending controls before public live access.
- Support clearly labeled saved explanations for a demo when live inference is unavailable.

## Engineering workflow

1. Define the behavior and acceptance criteria for a focused change.
2. Review the implementation approach and relevant data definitions.
3. Implement and inspect the diff.
4. Execute the appropriate tests and normal application entry point.
5. Document material decisions, assumptions, and limitations.
6. Commit the verified milestone and update release status.

Review AI-generated changes using the same correctness and verification standards as other code. Keep changes small enough to trace from input through calculation to output.

## User validation and release artifacts

Ask two or three users to identify the team with more shots, explain the xG comparison, and identify a limitation of an AI answer. Record accuracy, confusion, and at least one resulting improvement.

Release artifacts include a README, reproducible setup, source attribution, meaningful tests, screenshots when available, and an AI evaluation report for v1.0. A deployment decision will consider compatibility, data access, secret management, and operating cost.

## Immediate next actions

1. Review current files and committed history for public release.
2. Run the analyzer and tests, and verify raw data remains ignored and untracked.
3. Commit and push the analyzer, tests, README, source notes, and engineering plan.
4. Publish the repository and tag v0.1.0.
5. Define shots on target and begin the shot-map milestone.
