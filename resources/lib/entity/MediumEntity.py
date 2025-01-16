class MediumEntity:
    def __init__(
        self,
        mediumId: int = None,
        uniqueId: int = None,
        title: str = None,
        isWatched: bool = None
    ) -> None:
        self.id = mediumId
        self.uniqueId = uniqueId
        self.title = title
        self.isWatched = isWatched

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MediumEntity):
            return False

        return self.id == other.id \
            and self.uniqueId == other.uniqueId \
            and self.title == other.title \
            and self.isWatched == other.isWatched

    def clone(self) -> 'MediumEntity':
        return type(self)(
            self.id,
            self.uniqueId,
            self.title,
            self.isWatched
        )
