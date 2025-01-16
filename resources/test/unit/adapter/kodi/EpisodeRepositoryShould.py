import unittest
from unittest import mock
from resources.lib.adapter.kodi import EpisodeRepository
from resources.lib.entity import MediumEntity


class EpisodeRepositoryShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.kodi.JsonRPC')
    def setUp(self, jsonrpc):
        self.jsonrpc = jsonrpc
        self.repo = EpisodeRepository(self.jsonrpc)

    def test_build_episode_when_retrieving_with_known_id(self):
        fakeResponse = {'result': {'episodedetails': self._buildEpisodeObject(1)}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        episode = self.repo.retrieveById(5)

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': 5},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertEqual(
            self._buildEpisodeEntity(True),
            episode
        )

    def test_return_none_when_retrieving_with_unknown_id(self):
        self.jsonrpc.call = mock.Mock(return_value={})

        episode = self.repo.retrieveById('unknown_id')

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': 'unknown_id'},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertIsNone(episode)

    def test_build_episodes_when_retrieving_all(self):
        fakeResponse = {'result': {'episodes': [
            self._buildEpisodeObject(1),
            self._buildEpisodeObject(0)
        ]}}
        self.jsonrpc.call = mock.Mock(return_value=fakeResponse)

        episodes = self.repo.retrieveAll()

        self.jsonrpc.call.assert_called_once_with(
            'VideoLibrary.GetEpisodes',
            {},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        self.assertEqual(
            [self._buildEpisodeEntity(True), self._buildEpisodeEntity(False)],
            episodes
        )

    def test_change_episode_playcount_to_0_when_updating_to_unwatched(self):
        episode = self._buildEpisodeEntity(False)
        self.repo.updateWatchedStatus(episode)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetEpisodeDetails', {
            'episodeid': episode.id,
            'playcount': 0
        })

    def test_change_episode_playcount_to_1_when_updating_to_watched(self):
        episode = self._buildEpisodeEntity(True)
        self.repo.updateWatchedStatus(episode)

        self.jsonrpc.call.assert_called_once_with('VideoLibrary.SetEpisodeDetails', {
            'episodeid': episode.id,
            'playcount': 1
        })

    @staticmethod
    def _buildEpisodeObject(playcount):
        return {
            'episodeid': 5,
            'uniqueid': {
                'tvdb': 1005
            },
            'sorttitle': 'Episode title S01E01',
            'playcount': playcount
        }

    @staticmethod
    def _buildEpisodeEntity(isWatched):
        return MediumEntity(5, 1005, 'Episode title S01E01', isWatched)
