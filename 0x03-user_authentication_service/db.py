"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        func to Create a User object and save it to the database
        Args:
            email: user's email address
            hashed_password: password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)

        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        func to return a user who has an attribute matching the attributes
        Args:
            attributes: the dictionary of attributes to match the user
        Return:
            the result matching user or raise error
        """
        all_us = self._session.query(User)

        for ky, vl in kwargs.items():
            if ky not in User.__dict__:
                raise InvalidRequestError

            for usrx in all_us:
                if getattr(usrx, ky) == vl:
                    return usrx

        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        func to Update a user's attributes
        Args:
            user_id: user's id
            kwargs: dict of key, value pairs representing the
        Return:
            there is No return value
        """
        try:
            usrx = self.find_user_by(id=user_id)

        except NoResultFound:
            raise ValueError()

        for ky, vl in kwargs.items():
            if hasattr(usrx, ky):
                setattr(usrx, ky, vl)

            else:
                raise ValueError

        self._session.commit()
