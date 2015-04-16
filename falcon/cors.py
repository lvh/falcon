from collections import namedtuple
from functools import partial

Parameters = namedtuple('Parameters', ('origin', 'method', 'headers'))

def _allow_all(parameters):
    return True

allow_all_origins = allow_all_methods = _allow_all

def _allow_some(attr, vals):
    allowed = frozenset(vals)

    def pred(parameters):
        return getattr(parameters, attr) in vals

    return pred

allow_origins = partial(_allow_some, "origin")
allow_methods = partial(_allow_some, "method")

def pred_all(preds):
    return lambda *a, **kw: all(p(*a, **kw) for p in preds)
