from typing import List

from resources.lib.adapter import MediumRepositoryInterface
from resources.lib.entity import MediumEntity
from resources.lib.infra.kodi import JsonRPC


class EpisodeRepository(MediumRepositoryInterface):
    def __init__(self, jsonrpc: JsonRPC) -> None:
        self.jsonrpc = jsonrpc

    @staticmethod
    def getKind() -> str:
        return 'episode'

    def retrieveById(self, mediumId: int) -> MediumEntity:
        response = self.jsonrpc.call(
            'VideoLibrary.GetEpisodeDetails',
            {'episodeid': mediumId},
            ['uniqueid', 'showtitle', 'playcount']
        )
        return self._buildEntity(response.get('result', {}).get('episodedetails'))

    def retrieveAll(self) -> List[MediumEntity]:
        response = self.jsonrpc.call(
            'VideoLibrary.GetEpisodes',
            {},
            ['uniqueid', 'showtitle', 'playcount']
        )
        return list(map(
            self._buildEntity,
            response.get('result').get('episodes')
        ))

    def updateWatchedStatus(self, medium: MediumEntity) -> None:
        self.jsonrpc.call(
            'VideoLibrary.SetEpisodeDetails',
            {
                'episodeid': medium.id,
                'playcount': 1 if medium.isWatched else 0
            }
        )

    def _buildEntity(self, medium: dict) -> MediumEntity:
        if not medium:
            return None
        return MediumEntity(
            medium.get('episodeid'),
            medium.get('uniqueid').get('tvdb'),
            medium.get('showtitle'),
            medium.get('playcount') > 0
        )
