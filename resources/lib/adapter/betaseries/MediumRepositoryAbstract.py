from typing import List

from resources.lib.adapter import MediumRepositoryInterface
from resources.lib.infra.betaseries import Http


class MediumRepositoryAbstract(MediumRepositoryInterface):
    def __init__(self, http: Http) -> None:
        self.http = http

    def retrieveUpdatedIdsFrom(self, endpoint: int, limit: int = 100) -> List[dict]:
        user = self.http.get('/members/infos', {'summary': 'true'})

        params = {
            'types': self.getKind(),
            'id': user.get('member').get('id'),
            'nbpp': limit
        }
        if endpoint:
            params['last_id'] = endpoint

        response = self.http.get('/timeline/member', params)
        return [
            {
                'id': event.get('ref_id'),
                'endpoint': event.get('id')
            } for event in response.get('events')[::-1]
        ]
