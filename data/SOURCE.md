# Data source

**Provider:** StatsBomb Open Data (Hudl StatsBomb)
**Repository:** https://github.com/hudl/open-data (old `statsbomb/open-data` links redirect here)
**Terms:** "StatsBomb Data: User Agreement Standard Terms", last updated 8 September 2023 —
https://github.com/hudl/open-data/blob/master/LICENSE.pdf

Raw files are stored only in `data/raw/`, which is git-ignored. Do not commit, upload, or share them.

## Files in use

| Local path | Source URL (pinned to revision) |
| --- | --- |
| `data/raw/matches/2/27.json` | https://raw.githubusercontent.com/hudl/open-data/4b73468fc5b0f1950f9f66fada70ad3a4f9327cb/data/matches/2/27.json |
| `data/raw/events/3754013.json` | https://raw.githubusercontent.com/hudl/open-data/4b73468fc5b0f1950f9f66fada70ad3a4f9327cb/data/events/3754013.json |

- **Source revision:** commit `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`
- **Retrieved:** 2026-11-04 22:58 UTC
- **SHA-256** (to confirm a re-download is identical):
  - `matches/2/27.json`: `e07d6d360b30e0cd17f9aeea0db1502d2a5666d298f1b44b83a2d2f21ba3d21b`
  - `events/3754013.json`: `e148a96760e1318228fc42402a3338deeba8cec152e00a7384da7f1e09c448aa`

## Selected match

| Field | Value |
| --- | --- |
| Competition | Premier League (ID 2), verified in `data/competitions.json` at the same revision |
| Season | 2015/2016 (ID 27) |
| Match | Leicester City vs Chelsea (ID 3754013), 2015-12-14 |

## Re-downloading

From the project root (Git Bash):

```sh
REV=4b73468fc5b0f1950f9f66fada70ad3a4f9327cb
B=https://raw.githubusercontent.com/hudl/open-data/$REV/data
mkdir -p data/raw/matches/2 data/raw/events
curl -fsSL "$B/matches/2/27.json" -o data/raw/matches/2/27.json
curl -fsSL "$B/events/3754013.json" -o data/raw/events/3754013.json
```

## Attribution and use requirements (from the terms)

- Any published analysis must credit StatsBomb with the StatsBomb logo (§1.4, p.2). Get the logo from the official media pack.
- Analysis and conclusions may be shared publicly (intro, p.1).
- The data itself may not be distributed, reproduced, or provided to third parties (§1.2.1, p.1; §7, p.4).
- No commercial use of the data or derived analysis (§1.2.2, p.1).
- StatsBomb asks users to register at statsbomb.com/resource-centre (intro, p.1; §2.2, p.2). Registration status: **not yet confirmed**.

See PROJECT_PLAN.md section 6 for interpretations that remain uncertain.

## Known data quirks

- Player name stored as `N''Golo Kanté` (doubled apostrophe) in the source events file.
- The match `kick_off` time has an undocumented timezone; display the date only.
