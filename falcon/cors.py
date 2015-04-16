from collections import namedtuple

Parameters = namedtuple('Parameters', ('origin', 'method', 'headers'))

def _allow_all(parameters):
    return True

allow_all_origins = allow_all_methods = _allow_all

def allow_origins(origins):
    allowed_origins = frozenset(origins)

    def pred(parameters):
        return parameters.origin in allowed_origins

    return pred

def allow_methods(methods):
    allowed_methods = frozenset(methods)

    def pred(parameters):
        return parameters.method in allowed_methods

    return pred

def pred_all(preds):
    return lambda *a, **kw: all(p(*a, **kw) for p in preds)
