from .exceptions import BaseAppException


def doc_e(*errs: type[BaseAppException]) -> str:
    return f"errors({', '.join(err.__name__ for err in errs)})"
