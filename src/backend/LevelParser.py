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
    box = Box(None, None, None, None, None)
    for field in named_tpl._fields:
        if field == 'rules':
            continue
        setattr(box, field, getattr(named_tpl, field))

    for rule_tpl in getattr(named_tpl, 'rules'):
        rule = Rule(None, None, None)
        for key, value in rule_tpl._asdict().items():
            setattr(rule, key, value)
        box.add_rule(rule)
    return box


def parse(cur_lvl):
    with open(join(LEVELS_PATH, f'lvl_{cur_lvl}')) as f:
        text = f.read()
    field_text, target_text = text.split('target:\n')
    pre_field = json.loads(field_text, object_hook=decoder)
    field = Field(pre_field.rows, pre_field.cols)
    for i in range(pre_field.rows):
        for j in range(pre_field.cols):
            field[i][j] = box_from(pre_field.field[i][j])

    target = [target_text.split()[i:i+pre_field.cols] for i in range(0, len(target_text.split()), pre_field.cols)]
    return field, target
