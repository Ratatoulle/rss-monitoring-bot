from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="user")


class Resource(Base):
    __tablename__ = "resource"

    url: Mapped[str] = mapped_column(TEXT, primary_key=True)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="resource")
    rss_items: Mapped[List["RSSItem"]] = relationship(back_populates="resource")


class Subscription(Base):
    __tablename__ = "subscription"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    resource_url: Mapped[int] = mapped_column(ForeignKey("resource.url"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="subscriptions")
    resource: Mapped["Resource"] = relationship(back_populates="subscriptions")


class RSSItem(Base):
    __tablename__ = "rss_item"

    guid: Mapped[str] = mapped_column(TEXT, primary_key=True)
    title: Mapped[str] = mapped_column(TEXT)
    link: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
    category: Mapped[str | None] = mapped_column(TEXT)
    pub_date = mapped_column(TIMESTAMP)
    resource_url: Mapped[int] = mapped_column(ForeignKey("resource.url"))

    resource: Mapped["Resource"] = relationship(back_populates="rss_items")
