from typing import Never, NoReturn


def never(_: Never) -> NoReturn:
    error_message: str = "unhandled case"
    raise ValueError(error_message)
