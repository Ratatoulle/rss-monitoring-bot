from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, URL, select, ScalarResult
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from typing import Iterator
import datetime

import os
from dotenv import load_dotenv

from models import Base, Resource, User, Subscription, RSSItem


class DBHelper:

    def __init__(self):
        load_dotenv()
        self._db_info: dict = {name: value for name, value in os.environ.items() if "DB" in name}
        self._url: URL = URL.create(*self._db_info.values())
        self.engine: Engine = create_engine(self._url, echo=True if __debug__ else False)
        self.session: Session = Session(self.engine)
        Base.metadata.create_all(self.engine)

    def add_user(self, user: User):
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add_resource(self, resource: Resource):
        try:
            self.session.add(resource)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add_rss_item(self, rss_item: RSSItem):
        try:
            self.session.add(rss_item)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add_subscription(self, subscription: Subscription):
        try:
            self.session.add(subscription)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def get_rss_items(self, resource: Resource, delta: datetime.timedelta = datetime.timedelta(hours=1)) -> Iterator[RSSItem]:
        now = datetime.datetime.now()
        rss_items = self.session.scalars(select(RSSItem).where(RSSItem.resource == resource))
        # suitable_items = []
        for item in rss_items:
            if now - item.pub_date <= delta:
                yield item

    def get_resource(self, url: str) -> Resource:
        return self.session.scalar(select(Resource).where(Resource.url == url))

    def get_user(self, user_id: int) -> User:
        return self.session.scalar(select(User).where(User.id == user_id))

    def get_all_resources(self) -> ScalarResult[Resource]:
        return self.session.scalars(select(Resource))


if __name__ == "__main__":
    helper = DBHelper()

load_dotenv()
db_info = {name: value for name, value in os.environ.items() if "DB" in name}
url = URL.create(*db_info.values())
engine = create_engine(url, echo=True)
s = Session(engine)
Base.metadata.create_all(engine)

# from models import Base, Resource, User, Subscription, RSSItem
# from database import s
