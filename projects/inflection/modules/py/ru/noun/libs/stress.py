from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version


def extract_stress_type(rest_index):  # export
    _.log_func('stress', 'extract_stress_type')

    #    OLD: Старая версия кода:
#    # local stress_regexp = "([abcdef][′']?[′']?)"
#    # local stress_regexp2 = '(' + stress_regexp + '.*//.*' + stress_regexp + ')'
#    stress_regexp = '(' + stress_regexp + '(% ?.*))'
#    data.stress_type = _.extract(rest_index, stress_regexp2)
#    if not data.stress_type:
#        data.stress_type = _.extract(rest_index, stress_regexp)
#    # end
    # local stress_type, allowed_stress_types

    # INFO: Извлечение ударения из оставшейся части индекса:
    stress_type = _.extract(rest_index, "([abcdef][′']?[′']?)")

    # INFO: Замена особых апострофов в ударении на обычные:
    if stress_type:
        stress_type = _.replaced(stress_type, '′', "'")
    # end

    # INFO: Список допустимых схем ударений:
    allowed_stress_types = {'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''" }

    # INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
    if stress_type and not _.equals(stress_type, allowed_stress_types):
        return stress_type, dict(error='Ошибка: Неправильная схема ударения: ' + stress_type)  # dict
    # end
    return stress_type, None  # INFO: `None` здесь -- признак, что нет ошибок
# end


# Данные: ударность основы и окончания в зависимости от схемы ударения
def get_noun_stress_schema(stress_type):  # export  # INFO: Вычисление схемы ударения
    _.log_func('stress', 'get_noun_stress_schema')

    # local stress_schema, types, sg_value, pl_value

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    stress_schema = dict(  # dict
        stem = dict(  # dict
            sg     = _.equals(stress_type, ["a", "c", "e"]),
            acc_sg = _.equals(stress_type, ["a", "c", "e", "d'", "f'"]),
            ins_sg = _.equals(stress_type, ["a", "c", "e", "b'", "f''"]),
            pl     = _.equals(stress_type, ["a", "d", "d'"]),
            nom_pl = _.equals(stress_type, ["a", "d", "d'", "e", "f", "f'", "f''"]),
        ),  # dict
        ending = dict(  # dict
            sg     = _.equals(stress_type, ["b", "b'", "d", "d'", "f", "f'", "f''"]),
            acc_sg = _.equals(stress_type, ["b", "b'", "d", "f", "f''"]),
            ins_sg = _.equals(stress_type, ["b", "d", "d'", "f", "f'"]),
            pl     = _.equals(stress_type, ["b", "b'", "c", "e", "f", "f'", "f''"]),
            nom_pl = _.equals(stress_type, ["b", "b'", "c"]),
        ),  # dict
    )  # dict

    types = ['stem', 'ending']
    for i, type in enumerate(types):
        sg_value = stress_schema[type]['sg']
        stress_schema[type]['nom_sg'] = sg_value
        stress_schema[type]['gen_sg'] = sg_value
        stress_schema[type]['dat_sg'] = sg_value
        stress_schema[type]['prp_sg'] = sg_value

        pl_value = stress_schema[type]['pl']
        stress_schema[type]['gen_pl'] = pl_value
        stress_schema[type]['dat_pl'] = pl_value
        stress_schema[type]['ins_pl'] = pl_value
        stress_schema[type]['prp_pl'] = pl_value
    # end

    return stress_schema
# end


# Данные: ударность основы и окончания в зависимости от схемы ударения
def get_adj_stress_schema(stress_type):  # export  # INFO: Вычисление схемы ударения
    _.log_func('stress', 'get_adj_stress_schema')

    # TODO: Пока не используется

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            sg = _.startswith(stress_type, "a/"),
            pl = _.startswith(stress_type, "b/"),
            srt_sg_f = _.endswith(stress_type, ["/a", "/a'"]),
            srt_sg_n = _.endswith(stress_type, ["/a", "/c", "/a'", "/c'", "/c''"]),
            srt_pl = _.endswith(stress_type, ["/a", "/c", "/a'", "/b'", "/c'", "/c''"]),
        ),  # dict
        ending = dict(  # dict
            sg = _.startswith(stress_type, "b/"),
            pl = _.startswith(stress_type, "a/"),
            srt_sg_f = _.endswith(stress_type, ["/b", "/c", "/a'", "/b'", "/c'", "/c''"]),
            srt_sg_n = _.endswith(stress_type, ["/b", "/b'", "/c''"]),
            srt_pl = _.endswith(stress_type, ["/b", "/b'", "/c'", "/c''"]),
        ),  # dict
    )  # dict
    return stress_schema
# end


def get_pronoun_stress_schema(stress_type):  # export  # INFO: Вычисление схемы ударения
    _.log_func('stress', 'get_pronoun_stress_schema')

    # TODO: Пока не используется

    # общий подход следующий:
    # если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
    # local stress_schema
    stress_schema = dict(  # dict
        stem = dict(  # dict
            sg = _.equals(stress_type, "a"),
            pl = _.equals(stress_type, "b"),
        ),  # dict
        ending = dict(  # dict
            sg = _.equals(stress_type, "b"),
            pl = _.equals(stress_type, "a"),
        ),  # dict
    )  # dict
    return stress_schema
# end


def get_stress_schema(stress_type, adj, pronoun):  # export  # Пока не используется
    _.log_func('stress', 'get_stress_schema')

    if adj:
        return export.get_adj_stress_schema(stress_type)
    elif pronoun:
        return export.get_pronoun_stress_schema(stress_type)
    else:
        return export.get_noun_stress_schema(stress_type)
    # end
# end


# TODO: вместо "endings" может передавать просто data
def add_stress(endings, case):
    _.log_func('stress', 'add_stress')

    endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
# end


def apply_stress_type(data):  # export
    _.log_func('stress', 'apply_stress_type')

    # If we have "ё" specific
    if _.contains(data.rest_index, 'ё') and not data.stem_type == 'n-3rd':
        data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    if data.stress_schema['stem']['sg']:
        data.stems['nom_sg'] = data.stem_stressed
    else:
        data.stems['nom_sg'] = data.stem
        add_stress(data.endings, 'nom_sg')
    # end

    # If we have "ё" specific
    _.log_value(data.stem_type, 'data.stem_type')
    if _.contains(data.rest_index, 'ё') and data.stem_type != 'n-3rd':  # Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
        data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
    # end

    # TODO: process this individually !!!
    if data.stress_schema['stem']['sg']:
        data.stems['gen_sg'] = data.stem_stressed
        data.stems['dat_sg'] = data.stem_stressed
        data.stems['prp_sg'] = data.stem_stressed
    else:
        data.stems['gen_sg'] = data.stem
        data.stems['dat_sg'] = data.stem
        data.stems['prp_sg'] = data.stem
        add_stress(data.endings, 'gen_sg')
        add_stress(data.endings, 'dat_sg')
        add_stress(data.endings, 'prp_sg')
    # end

    if data.stress_schema['stem']['ins_sg']:
        data.stems['ins_sg'] = data.stem_stressed
    else:
        data.stems['ins_sg'] = data.stem
        add_stress(data.endings, 'ins_sg')
    # end

    if data.gender == 'f':
        if data.stress_schema['stem']['acc_sg']:
            data.stems['acc_sg'] = data.stem_stressed
        else:
            data.stems['acc_sg'] = data.stem
            add_stress(data.endings, 'acc_sg')
        # end
    # end

    if data.stress_schema['stem']['nom_pl']:
        data.stems['nom_pl'] = data.stem_stressed
    else:
        data.stems['nom_pl'] = data.stem
        add_stress(data.endings, 'nom_pl')
    # end

    if data.stress_schema['stem']['pl']:
        data.stems['gen_pl'] = data.stem_stressed
        data.stems['dat_pl'] = data.stem_stressed
        data.stems['ins_pl'] = data.stem_stressed
        data.stems['prp_pl'] = data.stem_stressed
    else:
        data.stems['gen_pl'] = data.stem
        data.stems['dat_pl'] = data.stem
        data.stems['ins_pl'] = data.stem
        data.stems['prp_pl'] = data.stem
        add_stress(data.endings, 'gen_pl')
        add_stress(data.endings, 'dat_pl')
        add_stress(data.endings, 'ins_pl')
        add_stress(data.endings, 'prp_pl')
    # end
# end


# return export
