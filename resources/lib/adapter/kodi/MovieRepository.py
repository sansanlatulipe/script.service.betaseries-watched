from typing import List
from resources.lib.adapter import MediumRepositoryInterface
from resources.lib.entity import MediumEntity
from resources.lib.infra.kodi import JsonRPC


class MovieRepository(MediumRepositoryInterface):
    def __init__(self, jsonrpc: JsonRPC):
        self.jsonrpc = jsonrpc

    @staticmethod
    def getKind() -> str:
        return 'movie'

    def retrieveById(self, mediumId: int) -> MediumEntity:
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovieDetails',
            {'movieid': mediumId},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        return self._buildEntity(response.get('result', {}).get('moviedetails'))

    def retrieveAll(self) -> List[MediumEntity]:
        response = self.jsonrpc.call(
            'VideoLibrary.GetMovies',
            {},
            ['uniqueid', 'sorttitle', 'playcount']
        )
        return list(map(
            self._buildEntity,
            response.get('result').get('movies')
        ))

    def updateWatchedStatus(self, medium: MediumEntity) -> None:
        self.jsonrpc.call(
            'VideoLibrary.SetMovieDetails',
            {
                'movieid': medium.id,
                'playcount': 1 if medium.isWatched else 0
            }
        )

    def _buildEntity(self, medium: dict) -> MediumEntity:
        if not medium:
            return None
        return MediumEntity(
            medium.get('movieid'),
            medium.get('uniqueid').get('tmdb'),
            medium.get('sorttitle'),
            medium.get('playcount') > 0
        )
