#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ get all objects depending of the class name (argument cls)"""
        classes = {
          'State': State,
          'City': City,
          'User': User,
          'Place': Place,
          'Review': Review,
          'Amenity': Amenity
        }

        if cls is None:
            objs = []
            for class_type in classes.values():
                objs.extend(self.__session.query(class_type).all())
        else:
            if isinstance(cls, str):
                cls = classes.get(cls)
            objs = self.__session.query(cls).all()

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """ Add the new obj to database session"""
        self.__session.add(obj)

    def save(self):
        """ Save the added objs in the session into the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete the new obj to database session"""
        self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        s_session = scoped_session(Session)
        self.__session = s_session()

    def close(self):
        """Dispose of current session if active"""
        self.__session.close()
