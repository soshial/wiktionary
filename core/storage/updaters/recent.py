from pywikibot import Timestamp
from pywikibot.pagegenerators import RecentChangesPageGenerator

from core.storage.updaters.base import BaseStorageUpdater
from lib.utils.dt import dt


def reduce_seconds(dt):
    if not dt:
        return None
    return Timestamp(dt.year, dt.month, dt.day, dt.hour, dt.minute)


class RecentStorageUpdater(BaseStorageUpdater):
    def __init__(self, start=None, end=None):
        self.start = reduce_seconds(start)
        self.end = reduce_seconds(end or self.storage.latest_edited)
        super().__init__()  # важно поместить его именно здесь

    def run(self):
        print(dt(), '- Processing recent pages until:', dt(self.end))
        generator = \
            RecentChangesPageGenerator(start=self.start, end=self.end,
                                       namespaces=[0])
        latest_edited = None
        for page in generator:
            edited = self.process_page(page)
            if not edited:
                continue
            latest_edited = latest_edited or reduce_seconds(edited)
        if latest_edited:
            self.storage.latest_edited = latest_edited
            print(dt(), '- New `latest_edited`:', dt(latest_edited))


if __name__ == '__main__':
    RecentStorageUpdater()
