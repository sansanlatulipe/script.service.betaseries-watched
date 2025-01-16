from resources.lib.adapter.betaseries import MediumRepositoryAbstract
from resources.lib.entity import MediumEntity
from resources.lib.infra.betaseries import Http


class MovieRepository(MediumRepositoryAbstract):
    def __init__(self, http: Http, config: dict):
        super().__init__(http)
        self.config = config

    @staticmethod
    def getKind() -> str:
        return 'film_add'

    def retrieveById(self, mediumId: int) -> MediumEntity:
        response = self.http.get(
            '/movies/movie',
            {'id': mediumId}
        )
        return self._buildEntity(response)

    def retrieveByUniqueId(self, uniqueId: int) -> MediumEntity:
        response = self.http.get(
            '/movies/movie',
            {'tmdb_id': uniqueId}
        )
        return self._buildEntity(response)

    def updateWatchedStatus(self, medium: MediumEntity) -> None:
        self.http.post(
            '/movies/movie',
            {
                'id': medium.id,
                'state': 1 if medium.isWatched else 0,
                'mail': 1 if self.config.get('mail')() else 0,
                'twitter': 1 if self.config.get('twitter')() else 0,
                'profile': 1 if self.config.get('profile')() else 0
            }
        )

    def _buildEntity(self, response: dict) -> MediumEntity:
        if 'id' not in response.get('movie', {}):
            return None

        medium = response.get('movie')

        return MediumEntity(
            medium.get('id'),
            medium.get('tmdb_id'),
            medium.get('title'),
            medium.get('user', {}).get('status') == 1
        )
