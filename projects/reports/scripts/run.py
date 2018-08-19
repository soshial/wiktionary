from datetime import datetime

from core.storage.main import MainStorage
from libs.sync.saver import sync_save
from libs.utils.log import log_exception
from libs.utils.wikibot import save_page
from projects.reports.lib.base import BaseReportPage
from projects.reports.reports.bucket import Bucket


class RunAllReports:
    # root = 'Участник:Vitalik/Отчёты/v3'
    root = 'Викисловарь:Отчёты/v3'
    tree = {
        'Ошибки': {
            'Важные': {},
            'Средние': {},
            'Лёгкие': {},
        },
        'Отчёты': {},
    }

    def __init__(self, debug=False, limit=None):
        print(datetime.now())
        self.debug = debug
        self.limit = limit
        self.storage = MainStorage()
        self._check_pages()
        self._build_tree()
        self._save_reports(self.tree)

    def _check_pages(self):
        pages_iterator = \
            self.storage.iterate_pages(silent=True, limit=self.limit)
        for title, page in pages_iterator:
            for report in Bucket.reports.values():
                report.process_page(page)
        for report in Bucket.reports.values():
            report.convert_entries()

    def _build_tree(self):
        for report in Bucket.reports.values():
            for report_page in report.report_pages():
                keys = report_page.path.split('/')
                curr = self.tree
                for key in keys[:-1]:
                    if key not in curr:
                        curr[key] = {}
                    curr = curr[key]
                key = keys[-1]
                if key in curr:
                    raise Exception(f'Duplicated report: {report_page.path}')
                curr[key] = report_page

    def _save_reports(self, node: dict, key='', prefix=''):
        self._save_node(node, key, prefix)
        for key, value in node.items():
            if type(value) == dict:
                # value -- это секция
                new_prefix = f'{prefix}/{key}'
                self._save_reports(value, key, new_prefix)  # рекурсивно
            else:
                # value -- это отчёт
                self._save_report(value)

    def _save_node(self, node: dict, key: str, prefix: str):
        title = f'{self.root}{prefix}'

        content = ''
        if key:
            content = f"Раздел: '''{key}'''\n\n"
        content += f"Подразделы:\n"
        content += self._get_node_content(node) or "* ''пусто''"

        desc = 'Обновление дерева отчётов'
        self._save_page(title, content, desc)

    def _get_node_content(self, node: dict, indent=1, prefix='/'):
        content = ''
        asterisks = '*' * indent
        for key, value in node.items():
            link = f'[[{prefix}{key}|{key}]]'
            if type(value) == dict:
                # value -- это секция
                content += f"{asterisks} {link}\n"
                new_prefix = f'{prefix}{key}/'
                content += self._get_node_content(value, indent + 1, new_prefix)
            else:
                # value -- это отчёт
                report = value
                if report.count:
                    styled_count = f"'''{report.count}'''"
                else:
                    styled_count = f"<span style='color: silver'>0</span>"
                content += f"{asterisks} '''{link}''' ({styled_count})\n"
        return content

    def _save_report(self, report: BaseReportPage):
        title = f'{self.root}/{report.path}'
        content = report.page_content
        desc = f'Обновление отчёта: {report.count}'
        self._save_page(title, content, desc)

    def _save_page(self, title, content, desc):
        sync_save(title, content)
        if self.debug:
            print(f'{"=" * 100}\n{title}\n{content.strip()}\n')
        else:
            save_page(title, content, desc)


@log_exception('reports')
def reports():
    RunAllReports(debug=False)
    # RunAllReports(debug=True, limit=40000)


if __name__ == '__main__':
    reports()
