from datetime import datetime
from typing import Final, List
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic
from app import database
from app.config import Commands
from app.calendar import fill_database


router = Router()


tasks_commands = {
    Commands.TODAY: 1,
    Commands.TOMORROW: 2,
    Commands.WEEK: 7,
    Commands.MONTH: 30,
    Commands.ALL: 999,
}


HELP_TEXT: Final = f'''{hbold('Вывод заданий:')}

{hbold(Commands.TODAY)} - на 1 день
{hbold(Commands.TOMORROW)} - на 2 дня
{hbold(Commands.WEEK)} - на 7 дней
{hbold(Commands.MONTH)} - на 30 дней
{hbold(Commands.ALL)} - на всё время'''


@router.message(F.text.lower().in_({'/start', '/help'}))
async def cmd_start(message: Message) -> None:
    await message.answer(HELP_TEXT)


def get_text(data: List[database.Task]) -> str:
    result = ''
    for record in data:
        date = datetime.strptime(record.end_date, "%Y-%m-%d %H:%M:%S%z").strftime('%d.%m.%y | %H:%M')
        result += f'{hitalic(record.categories)}\n{hbold(date)}\n{record.summary}\n\n'
    return result


@router.message(F.text.lower().in_(tasks_commands.keys()))
async def cmd_get_tasks(message: Message) -> None:
    await database.clear_all()
    await fill_database()
    data = await database.get_in_time_interval(tasks_commands[message.text])
    text = get_text(data)
    await message.answer(text)
