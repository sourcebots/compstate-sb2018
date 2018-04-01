import collections


class InvalidScoresheetException(Exception):
    pass


TOKEN_HOME_CORNERS = 'PGYO'
EXPECTED_TOKEN_COUNTS = {x: 5 for x in TOKEN_HOME_CORNERS}

ZONES = list(range(len(TOKEN_HOME_CORNERS))) + ['other']


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def _score_team(self, team_info):
        zone_id = team_info['zone']
        own_token = TOKEN_HOME_CORNERS[zone_id]

        token_string = self._arena_data[zone_id]['tokens'].replace(' ', '')

        score = 1 if team_info.get('moved') else 0

        for token in token_string:
            if token == own_token:
                score += 2
            else:
                score -= 1

        return score

    def calculate_scores(self):
        return {
            team_id: self._score_team(team_info)
            for team_id, team_info in self._teams_data.items()
        }

    def validate(self, extra_data):
        all_tokens = ''.join(
            self._arena_data[zone_id]['tokens']
            for zone_id in ZONES
        )

        token_counts = collections.Counter(all_tokens.replace(' ', ''))

        if token_counts != EXPECTED_TOKEN_COUNTS:
            raise InvalidScoresheetException(
                "Wrong token counts. Should be five of each of '{}' but was {!r}".format(
                    "', '".join(EXPECTED_TOKEN_COUNTS.keys()),
                    token_counts,
                ),
            )


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
