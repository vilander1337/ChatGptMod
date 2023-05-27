from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Keys(Base):
    __tablename__ = "Keys"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    oaikey: Mapped[str]