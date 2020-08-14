import json
from collections import namedtuple
from json import JSONEncoder
from types import SimpleNamespace as Namespace
from src.backend.Box import Box
from src.backend.Field import Field
from src.backend.Rule import Rule
from os.path import dirname, abspath, join
from src.backend.constants import *


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def decoder(dct):
    return namedtuple('Something', dct.keys())(*dct.values())


# Bad one.
def box_from(named_tpl):
    if named_tpl is None:
        return None
    box = Box(None, None, None)
    for field in named_tpl._fields:
        if field == 'rules':
            continue
        setattr(box, field, getattr(named_tpl, field))

    return box


def parse_field(field_text):
    pre_field = json.loads(field_text, object_hook=decoder)
    field = Field(pre_field.rows, pre_field.cols)
    for i in range(pre_field.rows):
        for j in range(pre_field.cols):
            field[i][j] = box_from(pre_field.field[i][j])
    return field


def parse_target(target_text, field):
    return [target_text.split()[i:i+field.cols] for i in range(0, len(target_text.split()), field.cols)]


def parse_kind_ro_rules(kind_to_rules_text):
    kind_to_rules = {}
    pre_kind_to_rules = json.loads(kind_to_rules_text)
    for kind_str, rule_dict_list in pre_kind_to_rules.items():
        kind = int(kind_str)
        ''' Make sure that we define kind rules only once'''
        assert kind not in kind_to_rules.keys()
        kind_to_rules[kind] = []
        for rule_dict in rule_dict_list:
            rule = Rule(None, None)
            for field, value in rule_dict.items():
                setattr(rule, field, value)
            kind_to_rules[kind].append(rule)
    return kind_to_rules


def parse(cur_lvl):
    with open(join(LEVELS_PATH, f'lvl_{cur_lvl}')) as f:
        text = f.read()
    field_text, tail = text.split('kind_to_rules:\n')
    kind_to_rules_text, tail = tail.split('target:\n')
    if 'min moves:' in tail:
        target_text, min_moves = tail.split('min moves:')
    else:
        target_text, min_moves = tail, None

    field = parse_field(field_text)
    target = parse_target(target_text, field)
    kind_to_rules = parse_kind_ro_rules(kind_to_rules_text)

    return field, target, kind_to_rules, int(min_moves) if min_moves else None

