from resources.lib.adapter.betaseries import MediumRepositoryAbstract
from resources.lib.entity import MediumEntity


class EpisodeRepository(MediumRepositoryAbstract):
    @staticmethod
    def getKind() -> str:
        return 'markas'

    def retrieveById(self, mediumId: int) -> MediumEntity:
        response = self.http.get(
            '/episodes/display',
            {'id': mediumId}
        )
        return self._buildEntity(response)

    def retrieveByUniqueId(self, uniqueId: int) -> MediumEntity:
        response = self.http.get(
            '/episodes/display',
            {'thetvdb_id': uniqueId}
        )
        return self._buildEntity(response)

    def updateWatchedStatus(self, medium: MediumEntity) -> None:
        method = self.http.post if medium.isWatched else self.http.delete
        method(
            '/episodes/watched',
            {'id': medium.id}
        )

    def _buildEntity(self, response: dict) -> MediumEntity:
        if 'id' not in response.get('episode', {}):
            return None

        medium = response.get('episode')

        return MediumEntity(
            medium.get('id'),
            medium.get('thetvdb_id'),
            '{title} S{season:02d}E{episode:02d}'.format(
                title=medium.get('show', {}).get('title'),
                season=medium.get('season'),
                episode=medium.get('episode')
            ),
            medium.get('user', {}).get('seen', False)
        )
