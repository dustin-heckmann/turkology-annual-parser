from typing import Optional


class group():
    def __init__(self, pattern: str, name: Optional[str] = None, optional=False):
        if name:
            self.string = f'(?P<{name}>{pattern})'
        else:
            self.string = f'(?:{pattern})'
        if optional:
            self.string += '?'

    def __or__(self, other):
        return group(f'{self}|{other}')

    def __str__(self):
        return self.string
