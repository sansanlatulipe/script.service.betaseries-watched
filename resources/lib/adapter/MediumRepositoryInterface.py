from resources.lib.entity import MediumEntity


class MediumRepositoryInterface:
    @staticmethod
    def getKind() -> str:
        pass

    def retrieveById(self, mediumId: int) -> MediumEntity:
        pass

    def retrieveByUniqueId(self, uniqueId: int) -> MediumEntity:
        pass

    def updateWatchedStatus(self, medium: MediumEntity) -> None:
        pass
