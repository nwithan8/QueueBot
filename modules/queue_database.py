import datetime
from typing import List, Union

from sqlalchemy import Column, Integer, String, Boolean, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base

import databases.base as db

Base = declarative_base()


def _next_unprocessed(session) -> Union['QueueEntry', None]:
    return session.query(QueueEntry).filter(QueueEntry.Processed is False).order_by(
        QueueEntry.TimeStamp).first()


class QueueEntry:
    __tablename__ = "queue"
    ID = Column(Integer, autoincrement=True)
    TimeStamp = Column(DateTime, nullable=False)
    Processed = Column(Boolean, nullable=False)

    @db.none_as_null
    def __init__(self, timestamp: datetime.datetime = None, processed: bool = False, **kwargs):
        self.TimeStamp = timestamp or kwargs.get('Timestamp') or datetime.datetime.now()
        self.Processed = processed or kwargs.get('Processed') or False


class UserQueueEntry(QueueEntry, Base):
    __tablename__ = 'user_queue'
    Entry = Column(String(1000), primary_key=True, nullable=False)

    @db.none_as_null
    def __init__(self, user_id: int = None, **kwargs):
        super().__init__()
        self.Entry = f"{user_id}" or kwargs.get('entry') or None

    @property
    def next_unprocessed(self) -> Union['UserQueueEntry', None]:
        return _next_unprocessed(self.session)


class QueueDatabase(db.SQLAlchemyDatabase):
    def __init__(self,
                 sqlite_file: str,
                 table_schemas: List):
        super().__init__(sqlite_file=sqlite_file, table_schemas=table_schemas)

    @db.table_exists(table_name='user_queue')
    def get_next_user_from_queue(self) -> Union[UserQueueEntry, None]:
        """
        Get the next user from the queue

        :return:
        """
        return UserQueueEntry().next_unprocessed

    @db.table_exists(table_name='user_queue')
    def add_user_to_queue(self, user_id: int) -> None:
        """
        Add a user to the queue

        :param user_id:
        :return:
        """
        user_queue_entry = self.create_entry_if_does_not_exist(table_schema=UserQueueEntry, fields_to_check=["Entry"],
                                                               Entry=f"{user_id}")

    @db.table_exists(table_name='user_queue')
    def find_user_location_in_queue(self, user_id: int) -> Union[int, None]:
        """
        Find the location of a user in the queue

        :param user_id:
        :return:
        """
        # get all unprocessed entries
        unprocessed_entries = self.get_all_by_filters(table=UserQueueEntry, order=desc(UserQueueEntry.ID),
                                                      Processed=False)
        counter = 1
        for entry in unprocessed_entries:
            if entry.Entry == f'{user_id}':
                return counter
            counter += 1
        return None  # user not found

    @db.table_exists(table_name='user_queue')
    def get_user_from_queue(self, user_id: int) -> Union[UserQueueEntry, None]:
        """
        Get a user from the queue

        :param user_id:
        :return:
        """
        return self.get_first_by_filters(table=UserQueueEntry, Entry=f'{user_id}')

    @db.table_exists(table_name='user_queue')
    def update_user_status_in_queue(self, user_id: int, status: bool):
        """
        Update the status of a user in the queue

        :param user_id:
        :param status:
        :return:
        """
        user_queue_entry = self.get_first_by_filters(table=UserQueueEntry, Entry=f'{user_id}')
        if user_queue_entry:
            user_queue_entry.Processed = status
            self.commit()

    @db.table_exists(table_name='user_queue')
    def get_all_unprocessed_users(self) -> List[UserQueueEntry]:
        """
        Get all unprocessed users

        :return:
        """
        return self.get_all_by_filters(table=UserQueueEntry, Processed=False)

    @db.table_exists(table_name='user_queue')
    def get_all_processed_users(self) -> List[UserQueueEntry]:
        """
        Get all processed users

        :return:
        """
        return self.get_all_by_filters(table=UserQueueEntry, Processed=True)

    @db.table_exists(table_name='user_queue')
    def get_all_users(self) -> List[UserQueueEntry]:
        """
        Get all users

        :return:
        """
        return self.get_all_by_filters(table=UserQueueEntry)

    @db.table_exists(table_name='user_queue')
    def delete_user_from_queue(self, user_id: int) -> None:
        """
        Delete a user from the queue

        :param user_id:
        :return:
        """
        user_queue_entry = self.get_first_by_filters(table=UserQueueEntry, Entry=f'{user_id}')
        if user_queue_entry:
            user_queue_entry.delete()
            self.commit()

    @db.table_exists(table_name='user_queue')
    def purge(self):
        """
        Purge all processed users from the queue

        :return:
        """
        for user in self.get_all_processed_users():
            user.delete()
            self.commit()
