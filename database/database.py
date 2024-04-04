from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, URL, select, ScalarResult, desc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
import datetime

import os
from dotenv import load_dotenv

from database.models import Base, Resource, User, Subscription, RSSItem


class DBHelper:
    """
        Class for establishing connection with database
    """
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
        """
            Method for adding user to database
        """
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add_resource(self, resource: Resource):
        """
            Method for adding RSS resource to database
        """
        try:
            self.session.add(resource)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add_rss_item(self, rss_item: RSSItem):
        """
            Method for adding RSS item to database
        """
        try:
            self.session.add(rss_item)
            self.session.commit()
        except IntegrityError as e:
            print(e)
            self.session.rollback()

    def add_subscription(self, subscription: Subscription):
        """
            Method for adding subscription to database
        """
        try:
            self.session.add(subscription)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def get_rss_items(self, resource: Resource, delta: datetime.timedelta = datetime.timedelta(hours=1), limit: int =5):
        """
            Method for gathering information from specified resource
            params:
                resource: RSS resource
                delta: time difference (hour, 2 hours) in which the elements
                of the specified source should be located
        """
        now = datetime.datetime.now()
        time_ago = now - delta
        rss_items = self.session.scalars(select(RSSItem)
                                         .where(RSSItem.resource_url == resource.url)
                                         .filter(RSSItem.pub_date > time_ago)
                                         .order_by(desc(RSSItem.pub_date))
                                         .limit(limit))
        return list(rss_items)

    def get_resource(self, url: str) -> Resource:
        """
            Method for gathering Resource ORM object, specified by url
        """
        return self.session.scalar(select(Resource).where(Resource.url == url))

    def get_user(self, user_id: int) -> User:
        """
            Method for gathering User ORM object, specified by user_id
        """
        return self.session.scalar(select(User).where(User.id == user_id))

    def get_user_subscriptions(self, user_id: int):
        """
            Method for gathering all subscriptions from user, specified by user_id
        """
        return self.session.scalars(select(Subscription).where(Subscription.user_id == user_id))

    def get_all_resources(self) -> ScalarResult[Resource]:
        """
            Method for gathering all resources from resource table
        """
        return self.session.scalars(select(Resource))
