from typing import Callable


def real_datas_unused(parser: Callable) -> Callable:
    """
    A decorator which indicates that the "datas" argument is not going to be used by
    the decorated parser. aocd will just send an empty list in this case, which speeds
    up invocation of the parser entrypoint somewhat.
    """
    parser.uses_real_datas = False
    return parser
