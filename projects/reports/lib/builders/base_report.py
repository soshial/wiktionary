

class BaseReportBuilder:
    def check(self, page):
        raise NotImplementedError()

    def build(self) -> list:
        raise NotImplementedError()
