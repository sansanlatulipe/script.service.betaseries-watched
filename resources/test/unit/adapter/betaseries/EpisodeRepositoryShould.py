import unittest
from unittest import mock

from resources.lib.adapter.betaseries import EpisodeRepository
from resources.lib.entity import MediumEntity
from resources.lib.infra.betaseries import Http


class EpisodeRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    def setUp(self, http: Http) -> None:
        self.http = http
        self.repo = EpisodeRepository(self.http)

    def test_build_episode_when_retrieving_with_known_id(self) -> None:
        self.http.get = mock.Mock(return_value=self._buildBsEpisodeObject(True))

        episode = self.repo.retrieveById(5)

        self.http.get.assert_called_once_with('/episodes/display', {'id': 5})
        self.assertEqual(
            self._buildEpisodeEntity(True),
            episode
        )

    def test_return_none_when_retrieving_with_unknown_id(self) -> None:
        self.http.get = mock.Mock(return_value={})

        episode = self.repo.retrieveById('unknown_id')

        self.http.get.assert_called_once_with('/episodes/display', {'id': 'unknown_id'})
        self.assertIsNone(episode)

    def test_build_episode_when_retrieving_with_known_tmdb_id(self) -> None:
        self.http.get = mock.Mock(return_value=self._buildBsEpisodeObject(False))

        episode = self.repo.retrieveByUniqueId(1005)

        self.http.get.assert_called_once_with('/episodes/display', {'thetvdb_id': 1005})
        self.assertEqual(
            self._buildEpisodeEntity(False),
            episode
        )

    def test_change_episode_status_when_updating_to_unwatched(self) -> None:
        episode = self._buildEpisodeEntity(False)
        self.repo.updateWatchedStatus(episode)

        self.http.delete.assert_called_once_with('/episodes/watched', {
            'id': episode.id
        })

    def test_change_episode_status_when_updating_to_watched(self) -> None:
        episode = self._buildEpisodeEntity(True)
        self.repo.updateWatchedStatus(episode)

        self.http.post.assert_called_once_with('/episodes/watched', {
            'id': episode.id
        })

    @staticmethod
    def _buildBsEpisodeObject(seen: bool) -> dict:
        return {
            'episode': {
                'id': 5,
                'thetvdb_id': 1005,
                'season': 1,
                'episode': 2,
                'show': {
                    'title': 'Fake title'
                },
                'user': {
                    'seen': seen
                }
            }
        }

    @staticmethod
    def _buildEpisodeEntity(isWatched: bool) -> MediumEntity:
        return MediumEntity(5, 1005, 'Fake title S01E02', isWatched)
