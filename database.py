from sqlalchemy import create_engine, URL, select, and_, update
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

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

    def add_user(self, id: int, name: str):
        user = User(id=id, name=name)
        self.session.add(user)
        self.session.commit()

    def add_resource(self, url: str):
        resource = Resource(url=url)
        self.session.add(resource)
        self.session.commit()

    def add_rss_item(self, **kwargs):
        pass



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