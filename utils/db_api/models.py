from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column(unique=True, index=True)
    sol_private_key: Mapped[str] = mapped_column(unique=True, index=True)
    address: Mapped[str]
    proxy: Mapped[str]
    name: Mapped[str]
    next_action_time: Mapped[datetime | None] = mapped_column(default=None)

    def __repr__(self):
        return f'{self.name}: {self.address}'
