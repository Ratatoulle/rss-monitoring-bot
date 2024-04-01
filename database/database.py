from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, URL, select, ScalarResult
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import datetime

import os
from dotenv import load_dotenv

from database.models import Base, Resource, User, Subscription, RSSItem


class DBHelper:

    def __init__(self):
        load_dotenv()
        self._db_info: dict = {name: value for name, value in os.environ.items() if "DB" in name}
        self._url: URL = URL.create(
            drivername=self._db_info['DB_DRIVERNAME'],
            username=self._db_info['DB_USERNAME'],
            password=self._db_info['DB_PASSWORD'],
            host=self._db_info['DB_HOST'],
            port=self._db_info['DB_PORT'],
            database=self._db_info['DB_DATABASE'],
        )
        # self._url: URL = URL.create(*self._db_info.values())
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
        except IntegrityError as e:
            print(e)
            self.session.rollback()

    def add_subscription(self, subscription: Subscription):
        try:
            self.session.add(subscription)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def get_rss_items(self, resource: Resource, delta: datetime.timedelta = datetime.timedelta(hours=1), limit: int =5):
        now = datetime.datetime.now()
        time_ago = now - delta
        rss_items = self.session.scalars(select(RSSItem)
                                         .where(RSSItem.resource_url == resource.url)
                                         .filter(RSSItem.pub_date > time_ago)
                                         .limit(limit))
        return list(rss_items)

    def get_resource(self, url: str) -> Resource:
        return self.session.scalar(select(Resource).where(Resource.url == url))

    def get_user(self, user_id: int) -> User:
        return self.session.scalar(select(User).where(User.id == user_id))

    def get_user_subscriptions(self, user_id: int):
        return self.session.scalars(select(Subscription).where(Subscription.user_id == user_id))

    def get_all_resources(self) -> ScalarResult[Resource]:
        return self.session.scalars(select(Resource))
