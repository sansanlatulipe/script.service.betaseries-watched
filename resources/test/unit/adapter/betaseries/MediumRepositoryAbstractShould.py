import unittest
from unittest import mock

from resources.lib.adapter.betaseries import MediumRepositoryAbstract
from resources.lib.infra.betaseries import Http


class MediumRepositoryAbstractShould(unittest.TestCase):
    @mock.patch('resources.lib.infra.betaseries.Http')
    def setUp(self, http: Http) -> None:
        self.http = http()
        self.repo = MediumRepositoryAbstract(self.http)

        self.repo.getKind = mock.Mock(return_value='expected_tag')

    def test_retrieve_last_movie_event_when_retrieving_updates_with_limit_1(self) -> None:
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 5, 'id': 12345}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(None, 1)

        self.assertEqual(2, self.http.get.call_count)
        self.http.get.assert_called_with('/timeline/member', {
            'types': 'expected_tag',
            'id': 'user_1',
            'nbpp': 1
        })
        self.assertEqual([{'id': 5, 'endpoint': 12345}], events)

    def test_retrieve_movie_events_when_retrieving_updated_from_endpoint(self) -> None:
        self.http.get = mock.Mock(side_effect=[
            {'member': {'id': 'user_1'}},
            {'events': [{'ref_id': 7, 'id': 12347}, {'ref_id': 6, 'id': 12346}]}
        ])

        events = self.repo.retrieveUpdatedIdsFrom(12345)

        self.http.get.assert_called_with('/timeline/member', {
            'types': 'expected_tag',
            'id': 'user_1',
            'last_id': 12345,
            'nbpp': 100
        })
        self.assertEqual(
            [{'id': 6, 'endpoint': 12346}, {'id': 7, 'endpoint': 12347}],
            events
        )
