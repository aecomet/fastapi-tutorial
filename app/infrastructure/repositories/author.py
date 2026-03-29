from sqlalchemy.orm import Session

from app.domain.entities.author import Author
from app.domain.repositories.author import IAuthorRepository
from app.infrastructure.models.author import AuthorModel


def _to_entity(model: AuthorModel) -> Author:
    return Author(
        id=model.id,
        name=model.name,
        bio=model.bio,
        created_at=model.created_at,
    )


class SqlAlchemyAuthorRepository(IAuthorRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def get(self, author_id: int) -> Author | None:
        model = self._db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
        return _to_entity(model) if model else None

    def get_list(self, skip: int = 0, limit: int = 100) -> list[Author]:
        models = self._db.query(AuthorModel).offset(skip).limit(limit).all()
        return [_to_entity(m) for m in models]

    def create(self, name: str, bio: str | None) -> Author:
        model = AuthorModel(name=name, bio=bio)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def update(
        self, author: Author, name: str | None = None, bio: str | None = None
    ) -> Author:
        model = self._db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
        if name is not None:
            model.name = name
        if bio is not None:
            model.bio = bio
        self._db.commit()
        self._db.refresh(model)
        return _to_entity(model)

    def delete(self, author: Author) -> None:
        model = self._db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
        self._db.delete(model)
        self._db.commit()
