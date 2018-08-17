from core.storage.main import MainStorage

from core.storage.updaters.lib.processors.base import BaseProcessor
from libs.utils.dt import dt, t
from libs.utils.exceptions import ImpossibleError


class MainStorageProcessor(BaseProcessor):
    """
    Обновление информации в главном хранилище.
    """
    def __init__(self, slug):
        super().__init__(slug)
        self.storage = MainStorage(lock=True)

    def process_delete(self, title):
        self.storage.delete(title)

    def process_update(self, title, content, edited, redirect):
        edited_str = dt(edited, utc=True)
        info = f"{edited_str}, {'R' if redirect else 'A'}"
        self.storage.update(title, content=content, info=info)
        self.log_hour('changed', f'<{info}> - {title}')

    @property
    def latest_edited(self):
        return self.storage.latest_edited

    @latest_edited.setter
    def latest_edited(self, value):
        self.storage.latest_edited = value

    def close(self, *args, **kwargs):
        self.save_titles()
        self.storage.unlock()

    def save_titles(self):
        titles = []
        articles = []
        redirects = []
        for title, info in self.storage.iterate('info'):
            titles.append(title)
            if info.endswith('A'):
                articles.append(title)
            elif info.endswith('R'):
                redirects.append(title)
            else:
                raise ImpossibleError()
        self.storage.save_titles(titles)
        self.storage.save_articles(articles)
        self.storage.save_redirects(redirects)

    @property
    def logs_path(self):
        return self.storage.logs_path
