import aiohttp
import os
import shutil
import icalendar


from app.config import Calendar, ENCODING, TIMEZONE
from app import database

from pytz import timezone
from pydantic import BaseModel
from typing import List


class Link(BaseModel):
    name: str
    url: str


class Ics(BaseModel):
    links: List[Link]


ics_links = Ics.parse_file(Calendar.URLS_FILE).links


async def download_ics_file(link: Link) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(link.url) as resp:
            with open(Calendar.ICS_FILE, 'wb') as f_handle:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
    new_name = f'{link.name}.ics'
    if os.path.exists(new_name):
        os.remove(new_name)
    os.rename(Calendar.ICS_FILE, new_name)
    shutil.move(new_name, Calendar.DIR)


async def download_data() -> None:
    if os.path.exists(Calendar.DIR):
        shutil.rmtree(Calendar.DIR)
    os.mkdir(Calendar.DIR)

    for link in ics_links:
        await download_ics_file(link)


async def fill_database() -> None:
    await download_data()
    ics_files = os.listdir(Calendar.DIR)
    for file_name in ics_files:
        path = f'{Calendar.DIR}/{file_name}'
        with open(path, mode='r', encoding=ENCODING) as file:
            cal = icalendar.Calendar.from_ical(file.read())
            for event in cal.walk('VEVENT'):
                summary = event.get('SUMMARY')
                description = event.get('DESCRIPTION')
                categories = event.get('CATEGORIES').to_ical().decode(ENCODING)
                start_date = str(event.get('DTSTART').dt.astimezone(timezone(TIMEZONE)))
                end_date = str(event.get('DTEND').dt.astimezone(timezone(TIMEZONE)))
                await database.write(
                    summary=summary,
                    description=description,
                    categories=categories,
                    start_date=start_date,
                    end_date=end_date
                )
