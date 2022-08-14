from datetime import datetime, date, timedelta
from genericpath import isfile
import os
import shutil
from typing import Dict, List
import logging

logging.basicConfig(filename='Cleanup.log', encoding='utf-8', level=logging.DEBUG)
DESKTOP = r'C:/Users/jakem/Desktop'

INCREMENT = 10  # number of days
DAYS_OLD_START = 25  # Start of how many days file/directory is older than
# Anything older than DAYS_OLD_START + INCREMENT will be placed in this folder
FOLDER_AGE = 50
EXCLUDE = []  # Manually add exclude files from being moved


desktop = os.listdir(DESKTOP)


def modify_time(path: str) -> str:
    # modify time of file
    m_timestamp = os.path.getmtime(path)
    # return date obj
    m_dt_obj = datetime.fromtimestamp(m_timestamp).strftime('%Y-%m-%d')
    return m_dt_obj


def create_time(path: str) -> str:
    # creation time of file
    c_timestamp = os.path.getctime(path)
    # get just date
    c_dt_obj = datetime.fromtimestamp(c_timestamp).strftime('%Y-%m-%d')
    return c_dt_obj


def convert(date_time: str) -> date:
    list_date = date_time.split('-')
    a, b, c = list_date
    datetime_str = datetime(int(a), int(b), int(c))
    return datetime_str.date()


def compare_date(date, file: str, created=True) -> None:
    today = date.today()
    past_date = today - timedelta(days=DAYS_OLD_START)
    delta = past_date - date
    if date < past_date:
        if created:
            logging.info(f"File, {file} is older than {DAYS_OLD_START} days")
            logging.info(f"Created on: {date}")
            logging.info(f"{file} is {delta.days} days older than past date")
        else:
            logging.info(f"File, {file} is older than {DAYS_OLD_START} days")
            logging.info(f"Last modified on: {date}")


def _older_than_start(date, file: str) -> int:
    today = date.today()
    past_date = today - timedelta(days=DAYS_OLD_START)
    delta = past_date - date
    if delta.days >= 0:
        return int(delta.days)
    else:
        return None


def find_oldest_file(files: Dict[str, int]) -> str:
    counter = 0
    oldest_file = ''
    for f in files:
        # logging.info(counter)
        logging.info(f"file {f}: days {files[f]}")
        if files[f] > counter:
            logging.info(f"{files[f]} is greater than {counter}")
            oldest_file = f
            counter = files[f]
            logging.info(f"Counter is now {counter}")
    logging.info(f"Oldest file is {oldest_file} at {counter} days")


def create_folder(dest: str, name: str) -> None:
    try:
        os.makedirs(f"{dest}/{name}")
    except FileNotFoundError as err:
        logging.error(f"{dest}/{name}, already exists: ERROR: {err}")


def move_files(src: str, dst: str) -> ValueError:
    # Check for destination directory
    if os.path.exists(dst):
        logging.info(f"{dst} exists")
        logging.info(f"Moving {DESKTOP}/{src} to {DESKTOP}/{dst}")
        shutil.move(f"{DESKTOP}/{src}", dst)
    else:
        logging.info(f"{dst} doent exists.")


def main():
    fileObj: Dict[str, int] = {}
    folder_day_counter: List[int] = []
    folder_dst: List[str] = []
    for x in desktop:
        modify_date = modify_time(f"{DESKTOP}/{x}")
        create_date = create_time(f"{DESKTOP}/{x}")
        days_older = _older_than_start(convert(create_date), x)
        if days_older != None:
            fileObj[x] = days_older
    folder_count = DAYS_OLD_START
    for i in range(DAYS_OLD_START, DAYS_OLD_START + FOLDER_AGE + 1, INCREMENT):
        create_folder(f'{DESKTOP}', f"older_than_{folder_count}_days")
        folder_day_counter.append(i)
        folder_dst.append(str(f"{DESKTOP}/older_than_{folder_count}_days"))
        folder_count += INCREMENT
        
    for f in fileObj:
        if f in EXCLUDE:
            logging.info(f"Found {f}")
        if fileObj[f] >= folder_day_counter[0] and fileObj[f] < folder_day_counter[1]:
            move_files(f, folder_dst[0])
        elif fileObj[f] >= folder_day_counter[1] and fileObj[f] < folder_day_counter[2]:
            move_files(f, folder_dst[1])
        elif fileObj[f] >= folder_day_counter[2] and fileObj[f] < folder_day_counter[3]:
            move_files(f, folder_dst[2])
        elif fileObj[f] >= folder_day_counter[3] and fileObj[f] < folder_day_counter[4]:
            move_files(f, folder_dst[3])
        elif fileObj[f] >= folder_day_counter[4] and fileObj[f] < folder_day_counter[5]:
            move_files(f, folder_dst[4])
        else:
            move_files(f, folder_dst[5])


if __name__ == "__main__":
    main()
