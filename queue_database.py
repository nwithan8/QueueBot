import datetime
from typing import List, Union

from sqlalchemy import Column, String, Boolean, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base

import modules.databases.base as db

Base = declarative_base()


def _next_unprocessed(session) -> Union['QueueEntry', None]:
    return session.query(QueueEntry).filter(QueueEntry.processed is False).order_by(
        QueueEntry.timestamp).first()


class QueueEntry:
    __tablename__ = "queue"
    timestamp = Column("timestamp", DateTime, nullable=False)
    processed = Column("processed", Boolean, nullable=False)

    @db.none_as_null
    def __init__(self, timestamp: datetime.datetime = None, processed: bool = False, **kwargs):
        self.timestamp = timestamp or kwargs.get('timestamp') or datetime.datetime.now()
        self.processed = processed or kwargs.get('processed') or False


class UserQueueEntry(QueueEntry, Base):
    __tablename__ = 'user_queue'
    user_id = Column("user_id", String(1000), primary_key=True, nullable=False)

    @db.none_as_null
    def __init__(self, user_id: int = None, **kwargs):
        super().__init__()
        self.user_id = f"{user_id}" if user_id else kwargs.get('user_id', None)

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
        user_queue_entry = self.create_entry_if_does_not_exist(table_schema=UserQueueEntry, fields_to_check=["user_id"],
                                                               user_id=f"{user_id}")
        if user_queue_entry is False:
            return None
        return user_queue_entry

    @db.table_exists(table_name='user_queue')
    def find_user_location_in_queue(self, user_id: int) -> Union[int, None]:
        """
        Find the location of a user in the queue

        :param user_id:
        :return:
        """
        # get all unprocessed entries
        unprocessed_entries = self.get_all_by_filters(table=UserQueueEntry, order=desc(UserQueueEntry.ID),
                                                      processed=False)
        counter = 1
        for entry in unprocessed_entries:
            if entry.user_id == f'{user_id}':
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
        return self.get_first_by_filters(table=UserQueueEntry, user_id=f'{user_id}')

    @db.table_exists(table_name='user_queue')
    def update_user_status_in_queue(self, user_id: int, status: bool):
        """
        Update the status of a user in the queue

        :param user_id:
        :param status:
        :return:
        """
        user_queue_entry = self.get_first_by_filters(table=UserQueueEntry, user_id=f'{user_id}')
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
    def delete_user_from_queue(self, user_id: int) -> bool:
        """
        Delete a user from the queue

        :param user_id:
        :return:
        """
        return self.delete_by_filters(table=UserQueueEntry, user_id=f'{user_id}')

    @db.table_exists(table_name='user_queue')
    def purge_users(self):
        """
        Purge all processed users from the queue

        :return:
        """
        for user in self.get_all_processed_users():
            user.delete()
            self.commit()

    @db.table_exists(table_name='user_queue')
    def mass_remove_users(self, user_ids: List[int]):
        """
        Mass remove users from the queue

        :param user_ids:
        :return:
        """
        for user_id in user_ids:
            self.delete_user_from_queue(user_id)
            self.commit()

    @db.table_exists(table_name='user_queue')
    def export_user_queue_to_csv(self, csv_file: str) -> bool:
        """
        Export all users from the queue to a csv file

        :param csv_file:
        :return:
        """
        return self.export_table_to_csv(table_name=UserQueueEntry.__tablename__, file_path=csv_file)
