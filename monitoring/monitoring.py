from database.database import DBHelper
from database.models import RSSItem
import feedparser


def fetch_data(url) -> bool | feedparser.FeedParserDict:
    """
        Returns RSS data from URL if it's valid, otherwise False
    """
    data = feedparser.parse(url)
    if data.bozo:
        return False
    return data


class Monitor:
    """
        Class for monitoring (updating records) of database resources
    """
    def __init__(self):
        self.helper = DBHelper()

    def update_table(self):
        """
            Main method of Monitor class, which updates table with new gathered information
        """
        for resource in self.helper.get_all_resources():
            data = fetch_data(resource.url)
            if not data:
                continue
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
