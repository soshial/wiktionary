import re

from pywikibot import NoPage

from core.reports.reports.ru.verbs.without_participles import get_participles, \
    remove_stress
from libs.utils.wikibot import load_page, save_page


def read_lines(title):
    lines = load_page(title).split('\n')
    for line in lines:
        if not line:
            continue
        yield line


base_pattern = '# \[\[([^]]+)\]\] +\((\?\?\?|сов|нес(?:\.|ов))\) +([^ ]+)'


def parse_lines(title, candidate=None):
    pattern_suffixes = {
        None: '$',
        'single': ' +→ +\[\[([^]]+)\]\]$',
        'any': ' +→ +\[\[(.+)\]\]$',
    }
    pattern_suffix = pattern_suffixes[candidate]
    for line in read_lines(title):
        try:
            groups = re.match(f'{base_pattern}{pattern_suffix}', line).groups()
        except AttributeError:
            print(line)
            raise

        if candidate:
            verb, aspect, verb_stressed, participle_candidate = groups
        else:
            verb, aspect, verb_stressed = groups
            participle_candidate = None

        if aspect == 'нес.':
            aspect = 'несов'
        if aspect == '???':
            print('aspect??:', line)
            raise Exception(f'Unknown `aspect`: {line}')

        if verb != remove_stress(verb_stressed).strip() \
                or '́' not in verb_stressed and 'ё' not in verb_stressed:
            if verb == verb_stressed:
                print(verb)
            else:
                print('-', verb, verb_stressed)
            raise Exception("Ошибка в данных (1).")

        yield verb, aspect, verb_stressed, participle_candidate


def save_new_page(title, content, desc='Заливка деепричастий'):
    try:
        load_page(title)
        return
    except NoPage:
        save_page(title, content, desc)


def save_participle(verb, aspect, participle, participle_stressed, synonym,
                    is_reflexive):
    tpl = 'дееся' if is_reflexive else 'дее'
    content = '{{подст:Участник:Cinemantique/' + tpl + \
              f'|{verb}||{participle_stressed}|{aspect}|{synonym}' + \
              '}}'
    save_new_page(participle, content)


def process_standard_normal_verb(verb, verb_stressed, aspect):
    verb_stem = verb_stressed[:-2]  # откусили "ть"
    participle_1 = f'{verb_stem}в'  # добавили "в"
    participle_2 = f'{verb_stem}вши'  # добавили "вши"

    cases = ((participle_1, participle_2), (participle_2, participle_1))
    for participle_stressed, synonym_stressed in cases:
        participle = remove_stress(participle_stressed)
        synonym = remove_stress(synonym_stressed)
        save_participle(verb, aspect, participle, participle_stressed, synonym,
                        is_reflexive=False)


def process_standard_reflexive_verb(verb, verb_stressed, aspect,
                                    participle_candidate):
    verb_stem = verb_stressed[:-4]  # откусили "ться"
    participle_stressed = f'{verb_stem}вшись'
    participle = remove_stress(participle_stressed)
    if participle != participle_candidate:
        print(f'"{participle}" != "{participle_candidate}"')
        raise Exception("Ошибка в данных (2).")
        # return
    save_participle(verb, aspect, participle, participle_stressed, '',
                    is_reflexive=True)


def process_special_verb(verb, verb_stressed, aspect, participle_candidate,
                         is_reflexive):
    participle_stressed = get_participles(verb_stressed, aspect)[0]
    participle = remove_stress(participle_stressed)
    if participle != participle_candidate:
        print(f'"{participle}" != "{participle_candidate}"')
        raise Exception("Ошибка в данных (2).")
        # return
    save_participle(verb, aspect, participle, participle_stressed, '',
                    is_reflexive)


def main(nums, candidate, mode):
    for num in nums:
        skip = True
        for entry in parse_lines(f'User:Vesailok/verb{num}', candidate):
            verb, aspect, verb_stressed, participle_candidate = entry

            if verb == '...': skip = False
            # if skip: continue

            if mode == 'std_norm':
                process_standard_normal_verb(verb, verb_stressed, aspect)
            elif mode == 'std_refl':
                process_standard_reflexive_verb(verb, verb_stressed, aspect,
                                                participle_candidate)
            elif mode == 'special_norm':
                process_special_verb(verb, verb_stressed, aspect,
                                     participle_candidate, is_reflexive=False)
            elif mode == 'special_refl':
                process_special_verb(verb, verb_stressed, aspect,
                                     participle_candidate, is_reflexive=True)
            else:
                raise Exception('Unknown mode.')


if __name__ == '__main__':
    # main([17], 'single', 'special_refl')
    # main([18], 'single', 'special_norm')
    # main([19], 'any', 'std_norm')
    # main([20], 'single', 'std_refl')
    pass
