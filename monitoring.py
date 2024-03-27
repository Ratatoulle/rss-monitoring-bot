from database import DBHelper
from sqlalchemy.exc import IntegrityError
from models import RSSItem
import feedparser


class Monitor:

    def __init__(self):
        self.helper = DBHelper()

    def update_table(self):
        resources = self.helper.get_all_resources()
        for resource in resources:
            data = feedparser.parse(resource.url)
            if data.bozo:
                raise Exception("Ill-formed XML file.")
            for entry in data.entries:
                # safe method to get value from dict
                guid = entry.get("guid")
                title = entry.get("title")
                link = entry.get("link")
                description = entry.get("description")
                category = entry.get("category")
                pub_date = entry.get("pubDate")

                if not pub_date:
                    pub_date = entry.get("published")
                new_item = RSSItem(
                    guid=guid,
                    title=title,
                    link=link,
                    description=description,
                    category=category,
                    pub_date=pub_date,
                    resource=resource,
                )
                try:
                    self.helper.add_rss_item(new_item)
                except IntegrityError:
                    self.helper.session.rollback()
                    continue


def main():
    import time
    monitor = Monitor()
    while True:
        monitor.update_table()
        time.sleep(60)


if __name__ == "__main__":
    main()
