from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, TIMESTAMP
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from database.utils import remove_html_tags
from typing import List
from dataclasses import dataclass


class Base(DeclarativeBase):
    pass


class User(Base):
    """
        ORM-class which represents user table in database

        Attributes:
            id (int): id of user
            name (str): name of user
            subscriptions (list): user subscriptions of RSS resources
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(TEXT)

    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Resource(Base):
    """
        ORM-class which represents resource table in database

        Attributes:
            url (str): URL of RSS resource
            subscriptions (list): list of subscriptions of current resource
            rss_items (list): list of related to current resource RSS items
    """
    __tablename__ = "resource"

    url: Mapped[str] = mapped_column(TEXT, primary_key=True)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="resource")
    rss_items: Mapped[List["RSSItem"]] = relationship(back_populates="resource")


class Subscription(Base):
    """
        ORM-class which represents association subscription table in database

        Attributes:
            user_id (int): id of user
            resource_url (list): URL of RSS resource
            user (User): User ORM-object
            resource (Resource): Resource ORM-object
    """
    __tablename__ = "subscription"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    resource_url: Mapped[int] = mapped_column(ForeignKey("resource.url"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="subscriptions")
    resource: Mapped["Resource"] = relationship(back_populates="subscriptions")


@dataclass
class RSSItem(Base):
    """
        ORM-class which represents association subscription table in database

        Attributes:
            guid (str): GUID of RSS item
            title (str): title of RSS item
            link (str): link to news article
            description (str): description of news article
            pub_date (str): news article date of publication
            resource_url (str): URL of RSS resource
            resource (Resource): Resource ORM-object
    """
    __tablename__ = "rss_item"

    guid: Mapped[str] = mapped_column(TEXT, primary_key=True)
    title: Mapped[str] = mapped_column(TEXT)
    link: Mapped[str] = mapped_column(TEXT)
    description: Mapped[str | None] = mapped_column(TEXT)
    category: Mapped[str | None] = mapped_column(TEXT)
    pub_date = mapped_column(TIMESTAMP)
    resource_url: Mapped[str] = mapped_column(ForeignKey("resource.url"))

    resource: Mapped["Resource"] = relationship(back_populates="rss_items")

    def __init__(self, entry: dict, resource_url: str):
        """
            Safe constructor of initialization RSSItem fields
        """
        self.guid = entry.get("guid")
        self.title = entry.get("title")
        self.link = entry.get("link")
        self.description = remove_html_tags(entry.get("description"))
        self.category = entry.get("category")
        self.pub_date = entry.get("pubDate")
        self.resource_url = resource_url

        if not self.pub_date:
            self.pub_date = entry.get("published")