from functools import wraps
from typing import List, Any

from sqlalchemy import create_engine, MetaData, null
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def none_as_null(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Replace None as null()
        """
        func(self, *args, **kwargs)
        for k, v in self.__dict__.items():
            if v is None:
                setattr(self, k, null())

    return wrapper


def map_attributes(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Map kwargs to class attributes
        """
        func(self, *args, **kwargs)
        for k, v in kwargs.items():
            if getattr(self, k):
                setattr(self, k, v)

    return wrapper


def false_if_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        """
        Return False if error encountered
        """
        try:
            return func(self, *args, **kwargs)
        except Exception as error_occurred:
            return False

    return wrapper


def table_exists(table_name: str) -> Any:
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if table_name not in self.registered_tables:
                raise Exception(f"Table schema {table_name} does not exist")
            return func(*args, **kwargs)

        return wrapper

    return decorator


class SQLAlchemyDatabase:
    def __init__(self,
                 sqlite_file: str,
                 table_schemas: List):
        self.sqlite_file = sqlite_file

        self.engine = None
        self.base = None
        self.meta = None
        self.session = None

        self.url = f'sqlite:///{sqlite_file}'

        self.setup()

        self.registered_tables = []
        for schema in table_schemas:
            schema.__table__.create(self.engine, checkfirst=True)
            self.registered_tables.append(schema.__tablename__)

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()

    def setup(self):
        if not self.url:
            return

        self.engine = create_engine(self.url)

        if not self.engine:
            return

        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        self.base = declarative_base(bind=self.engine)
        self.meta = MetaData()
        self.meta.create_all(self.engine)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def get_first_entry(self, table_schema, order=None):
        query = self.session.query(table_schema)
        if order:
            query = query.order_by(order)
        return query.first()

    def get_all_entries(self, table_schema, order=None):
        query = self.session.query(table_schema)
        if order:
            query = query.order_by(order)
        return query.all()

    def get_all_by_filters(self, table, order=None, **kwargs):
        query = self.session.query(table).filter_by(**kwargs)
        if order:
            query = query.order_by(order)
        return query.all()

    def get_first_by_filters(self, table, order=None, **kwargs):
        query = self.session.query(table).filter_by(**kwargs)
        if order:
            query = query.order_by(order)
        return query.first()

    def get_attribute_from_first_entry(self, table_schema, field_name, order=None):
        entry = self.get_first_entry(table_schema=table_schema, order=order)
        return getattr(entry, field_name, None)

    def set_attribute_of_first_entry(self, table_schema, field_name, field_value, order=None) -> bool:
        entry = self.get_first_entry(table_schema=table_schema, order=order)
        if not entry:
            entry = self.create_entry(table_schema, **{field_name: field_value})
        return self.update_entry_single_field(entry, field_name, field_value)

    @false_if_error
    def create_entry(self, table_schema, **kwargs):
        entry = table_schema(**kwargs)
        self.session.add(entry)
        self.commit()
        return entry

    @false_if_error
    def create_entry_if_does_not_exist(self, table_schema, fields_to_check: List[str], **kwargs):
        filters = {k: v for k, v in kwargs.items() if k in fields_to_check}
        entries = self.get_all_by_filters(table=table_schema, **filters)
        if not entries:
            return self.create_entry(table_schema=table_schema, **kwargs)
        return entries[0]

    @false_if_error
    def update_entry_single_field(self, entry, field_name, field_value) -> bool:
        setattr(entry, field_name, field_value)
        self.commit()
        return True

    @false_if_error
    def update_entry_multiple_fields(self, entry, **kwargs) -> bool:
        for field, value in kwargs.items():
            setattr(entry, field, value)
        self.commit()
        return True


class CustomTable:
    def __init__(self):
        self._ignore = []
