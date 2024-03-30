from database import DBHelper
from models import RSSItem
import feedparser


def fetch_data(url) -> bool | feedparser.FeedParserDict:
    data = feedparser.parse(url)
    if data.bozo:
        return False
    return data


class Monitor:

    def __init__(self):
        self.helper = DBHelper()

    def update_table(self):
        for resource in self.helper.get_all_resources():
            data = fetch_data(resource.url)
            if not data:
                continue
                # raise Exception("Ill-formed XML file.")
            for entry in data.entries:
                new_item = RSSItem(entry, resource.url)
                self.helper.add_rss_item(new_item)


def main():
    import time
    monitor = Monitor()
    while True:
        monitor.update_table()
        time.sleep(60)


if __name__ == "__main__":
    main()
