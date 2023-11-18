from pkg.providers.neptun import University


class LoginCredentials:

    def __init__(self, username: str, password: str, university: University) -> None:
        self._username = username
        self._password = password
        self._university = university
    
    @property
    def username(self) -> str:
        return self._username    
    
    @property
    def password(self) -> str:
        return self._password    
    
    @property
    def university(self) -> University:
        return self._university