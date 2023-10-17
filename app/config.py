from dotenv import load_dotenv
from typing import Final
from os import getenv


ENV_PATH: Final = '.env'
ENCODING: Final = 'utf-8'
TIMEZONE: Final = 'Europe/Moscow'


load_dotenv(ENV_PATH)


class Telegram:
    TOKEN: Final = str(getenv('TG_TOKEN'))
    ADMIN_ID: Final = int(getenv('ADMIN_ID'))


class Calendar:
    URLS_FILE: Final = 'ics_urls.json'
    ICS_FILE: Final = 'icalexport.ics'
    DIR: Final = 'ics_files'


class Database:
    NAME: Final = 'polytasks'
    USER: Final = 'postgres'
    PASSWORD: Final = str(getenv('DB_PASSWORD'))
    HOST: Final = '127.0.0.1'
    PORT: Final = '5432'


class Commands:
    TODAY: Final = '/today'
    TOMORROW: Final = '/tomorrow'
    WEEK: Final = '/week'
    MONTH: Final = '/month'
    ALL: Final = '/all'
