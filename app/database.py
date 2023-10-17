from app.config import Database

from gino import Gino
from app.config import Database
from typing import Final, List
import datetime

URI: Final = f'postgresql://{Database.USER}:{Database.PASSWORD}@{Database.HOST}:{Database.PORT}/{Database.NAME}'


db = Gino()


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer(), primary_key=True)
    summary = db.Column(db.Unicode(), nullable=False)
    description = db.Column(db.Unicode(), nullable=True)
    categories = db.Column(db.Unicode(), nullable=False)
    start_date = db.Column(db.Unicode(), nullable=False)
    end_date = db.Column(db.Unicode(), nullable=False)


async def clear_all() -> None:
    await db.gino.drop_all()
    await db.gino.create_all()


async def connect() -> None:
    await db.set_bind(URI)
    await clear_all()


async def disconnect() -> None:
    await db.pop_bind().close()


async def write(**kwargs) -> None:
    await Task.create(**kwargs)


async def get_in_time_interval(days: int) -> List[Task]:
    now = datetime.datetime.now()
    border = now + datetime.timedelta(days=days)
    result = await Task.query.where(
        (Task.end_date >= now.strftime('%Y-%m-%d %H:%M:%S%z')) &
        (Task.end_date <= border.strftime('%Y-%m-%d %H:%M:%S%z'))
    ).order_by(Task.end_date).gino.all()
    return result


async def get_all() -> List[Task]:
    result = await Task.query.order_by(Task.end_date).gino.all()
    return result
