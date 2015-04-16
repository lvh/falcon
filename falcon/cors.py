from collections import namedtuple

Parameters = namedtuple('Parameters', ('origin', 'method', 'headers'))

def allow_all_origins(parameters):
    return True

def allow_origins(origins):
    allowed_origins = frozenset(origins)

    def pred(parameters):
        return parameters.origin in allowed_origins

    return pred

def allow_all_methods(parameters):
    return True

def allow_methods(methods):
    allowed_methods = frozenset(methods)

    def pred(parameters):
        return parameters.method in allowed_methods

    return pred

def pred_all(preds):
    return lambda *a, **kw: all(p(*a, **kw) for p in preds)
