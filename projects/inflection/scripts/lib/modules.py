files = [
    'noun[.out]',
    'libs[.out]/endings',
    'libs[.out]/form',
    'libs[.out]/index',
    'libs[.out]/parse_args',
    'libs[.out]/reducable',
    'libs[.out]/result',
    'libs[.out]/stem_type',
    'libs[.out]/stress',
    # 'libs[.out]/testcases',
]


def get_module_title(file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else ''
    file = file.replace('[.out]', '')
    title = f'Module:{dev_prefix}inflection/ru/noun'
    if file == 'noun':
        return title
    if file.startswith('libs/'):
        title += file[len('libs'):]
        return title
    raise Exception('Unknown module title')
