#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException


class TestScorer(unittest.TestCase):
    longMessage = True

    def assertScores(self, expected, teams_data, arena_data):
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.calculate_scores()

        self.assertEqual(expected, scores, "Wrong scores!")

    def assertValidationError(self, teams_data, arena_data):
        with self.assertRaises(InvalidScoresheetException):
            scorer = Scorer(teams_data, arena_data)
            scorer.validate(None)

    def test_scores_match_start(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'YYYYY'},
            1: {'tokens': 'OOOOO'},
            2: {'tokens': 'PPPPP'},
            3: {'tokens': 'GGGGG'},
            'other': {'tokens': ''},
        }
        expected = {
            'ABC': -5,
            'DEF': -5,
            'GHI': -5,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_match_zeros(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': ''},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'PGOY PGOY PGOY PGOY PGOY'},
        }
        expected = {
            'ABC': 0,
            'DEF': 0,
            'GHI': 0,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_zone_with_mixed_opponent_colours(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'GOY GOY'},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'P P PGOY PGOY PGOY'},
        }
        expected = {
            'ABC': -6,
            'DEF': 0,
            'GHI': 0,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_zone_with_own_colours(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'PPP'},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'GOY GOY GOY PGOY PGOY'},
        }
        expected = {
            'ABC': 6,
            'DEF': 0,
            'GHI': 0,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_zone_with_mixed_colours(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'PPP GG OO'},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'Y Y GOY PGOY PGOY'},
        }
        expected = {
            'ABC': 2,
            'DEF': 0,
            'GHI': 0,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_zones_with_mixed_colours(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'PGOY PP'},
            1: {'tokens': 'GPO G'},
            2: {'tokens': 'YYY'},
            3: {'tokens': 'OY'},
            'other': {'tokens': 'P OO GG'},
        }
        expected = {
            'ABC': 3,
            'DEF': 2,
            'GHI': 6,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_movement_point(self):
        teams_data = {
            'ABC': {'zone': 0, 'moved': True},
            'DEF': {'zone': 1, 'moved': False},
            'GHI': {'zone': 2, 'moved': False},
        }
        arena_data = {
            0: {'tokens': ''},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'PGOY PGOY PGOY PGOY PGOY'},
        }
        expected = {
            'ABC': 1,
            'DEF': 0,
            'GHI': 0,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_scores_movement_point_and_tokens(self):
        teams_data = {
            'ABC': {'zone': 0, 'moved': True},
            'DEF': {'zone': 1, 'moved': False},
            'GHI': {'zone': 2, 'moved': False},
        }
        arena_data = {
            0: {'tokens': 'PGOY PP'},
            1: {'tokens': 'GPO G'},
            2: {'tokens': 'YYY'},
            3: {'tokens': 'OY'},
            'other': {'tokens': 'P OO GG'},
        }
        expected = {
            'ABC': 4,
            'DEF': 2,
            'GHI': 6,
        }

        self.assertScores(expected, teams_data, arena_data)

    def test_validate_error_non_present_team_moved(self):
        teams_data = {
            'ABC': {'zone': 0, 'present': False, 'moved': True},
            'DEF': {'zone': 1, 'present': False, 'moved': False},
            'GHI': {'zone': 2, 'present': False},
        }
        arena_data = {
            0: {'tokens': ''},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'PGOY PGOY PGOY PGOY PGOY'},
        }

        self.assertValidationError(teams_data, arena_data)

    def test_validate_error_invalid_notation(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': ''},
            1: {'tokens': 'Q'},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'PGOY PGOY PGOY PGOY PGOY'},
        }

        self.assertValidationError(teams_data, arena_data)

    def test_validate_error_not_enough_tokens(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': ''},
            1: {'tokens': ''},
            2: {'tokens': ''},
            3: {'tokens': ''},
            'other': {'tokens': 'PGOY PGOY PGOY PGOY'},
        }

        self.assertValidationError(teams_data, arena_data)

    def test_validate_error_too_many_tokens(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'YYY YYY'},
            1: {'tokens': 'GGG GGG'},
            2: {'tokens': 'PPP PPP'},
            3: {'tokens': 'OOO OOO'},
            'other': {'tokens': ''},
        }

        self.assertValidationError(teams_data, arena_data)

    def test_validate_error_invalid_combination_of_tokens(self):
        teams_data = {
            'ABC': {'zone': 0},
            'DEF': {'zone': 1},
            'GHI': {'zone': 2},
        }
        arena_data = {
            0: {'tokens': 'YYYYY'},
            1: {'tokens': 'YYYYY'},
            2: {'tokens': 'PPPPP'},
            3: {'tokens': 'OOOOO'},
            'other': {'tokens': ''},
        }

        self.assertValidationError(teams_data, arena_data)


if __name__ == '__main__':
    unittest.main()
