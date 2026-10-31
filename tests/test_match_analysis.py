"""Unit tests for summarize_shots using small, hand-made events.

Run from the project root:
    .venv\\Scripts\\python.exe -m unittest discover -s tests -v
"""

import unittest

from match_analysis import SHOOTOUT_PERIOD, summarize_shots

HOME = "Home FC"
AWAY = "Away FC"


def shot(team, outcome="Off T", xg=0.1, period=1):
    """Build a minimal StatsBomb-style shot event. xg=None leaves the xG key out."""
    shot_data = {"outcome": {"name": outcome}}
    if xg is not None:
        shot_data["statsbomb_xg"] = xg
    return {"period": period, "type": {"name": "Shot"}, "team": {"name": team}, "shot": shot_data}


def other_event(team, type_name="Pass", period=1):
    """Build a minimal non-shot event."""
    return {"period": period, "type": {"name": type_name}, "team": {"name": team}}


class SummarizeShotsTests(unittest.TestCase):

    def test_totals_per_team(self):
        events = [
            shot(HOME, "Goal", 0.30),
            shot(HOME, "Saved", 0.10),
            shot(AWAY, "Goal", 0.45),
        ]
        stats = summarize_shots(events, [HOME, AWAY])

        self.assertEqual(stats[HOME]["shots"], 2)
        self.assertEqual(stats[HOME]["goals"], 1)
        self.assertAlmostEqual(stats[HOME]["xg"], 0.40)
        self.assertEqual(stats[AWAY]["shots"], 1)
        self.assertEqual(stats[AWAY]["goals"], 1)
        self.assertAlmostEqual(stats[AWAY]["xg"], 0.45)

    def test_non_shot_events_ignored(self):
        events = [other_event(HOME, "Pass"), other_event(AWAY, "Own Goal Against"), shot(HOME, xg=0.2)]
        stats = summarize_shots(events, [HOME, AWAY])

        self.assertEqual(stats[HOME]["shots"], 1)
        self.assertEqual(stats[AWAY]["shots"], 0)
        self.assertEqual(stats[AWAY]["goals"], 0)

    def test_shootout_shots_excluded(self):
        events = [
            shot(HOME, "Goal", 0.76, period=4),  # extra-time penalty: counts
            shot(HOME, "Goal", 0.76, period=SHOOTOUT_PERIOD),
            shot(AWAY, "Saved", 0.76, period=SHOOTOUT_PERIOD),
        ]
        stats = summarize_shots(events, [HOME, AWAY])

        self.assertEqual(stats[HOME]["shots"], 1)
        self.assertEqual(stats[HOME]["goals"], 1)
        self.assertAlmostEqual(stats[HOME]["xg"], 0.76)
        self.assertEqual(stats[AWAY]["shots"], 0)
        self.assertAlmostEqual(stats[AWAY]["xg"], 0.0)

    def test_missing_xg_counted_separately(self):
        events = [shot(HOME, xg=0.25), shot(HOME, xg=None)]
        stats = summarize_shots(events, [HOME, AWAY])

        self.assertEqual(stats[HOME]["shots"], 2)  # the shot still counts
        self.assertEqual(stats[HOME]["missing_xg"], 1)
        self.assertAlmostEqual(stats[HOME]["xg"], 0.25)  # total covers known values only

    def test_team_with_zero_shots_retained(self):
        stats = summarize_shots([shot(HOME)], [HOME, AWAY])

        self.assertIn(AWAY, stats)
        self.assertEqual(stats[AWAY], {"shots": 0, "goals": 0, "xg": 0.0, "missing_xg": 0})


if __name__ == "__main__":
    unittest.main()
