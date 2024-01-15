import yaml

class Language:
    ENGLISH = "en"
    HUNGARY = "hu"

class Localization(dict):
    _language: str = Language.ENGLISH

    def __init__(self, path: str, language: Language) -> None:
        self._language = language
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
            super().update(data)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getitem__(self, key):
        return super().__getitem__(self._language)[key]

    def __repr__(self):
        return super().__getitem__(self._language).__repr__()
