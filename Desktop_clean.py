from datetime import datetime, date, timedelta
import os
import shutil


DESKTOP = r'C:/Users/jakem/Desktop'


DAYS_OLD = 25

desktop = os.listdir(DESKTOP)


def modify_time(path: str) -> str:
    #modify time of file
    m_timestamp = os.path.getmtime(path)
    #return date obj
    m_dt_obj =  datetime.fromtimestamp(m_timestamp).strftime('%Y-%m-%d')
    return m_dt_obj
    

def create_time(path: str) -> str:
    #creation time of file
    c_timestamp = os.path.getctime(path)
    #get just date
    c_dt_obj = datetime.fromtimestamp(c_timestamp).strftime('%Y-%m-%d')
    return c_dt_obj
    

def convert(date_time: str) -> date:
    list_date = date_time.split('-')
    a,b,c = list_date
    datetime_str = datetime(int(a),int(b),int(c))
    return datetime_str.date()

        
def compare_date(date, file: str, created=True) -> None:
    today = date.today()
    past_date = today - timedelta(days=DAYS_OLD)
    if date < past_date:
        if created:
            print(f"File, {file} is older than 25 days")
            print(f"Created on: {date}")
        else:
            print(f"File, {file} is older than 25 days")
            print(f"Last modified on: {date}")
            
            
def create_folder(dest: str, name: str) -> None:
    if os.path.exists(f"{dest}/{name}"):
        print(f"{dest}/{name}, already exists")
        return
    else:
        os.makedirs(f"{dest}/{name}")
        
    
def move_files(src: str, dest: str) -> ValueError:
    if len(src) == 0 or len(dest) == 0:
        raise ValueError('Either destination or Source not provided!') 
    

for x in desktop:

    modify_date = modify_time(f"{DESKTOP}/{x}")
    
    create_date = create_time(f"{DESKTOP}/{x}")

    #defaults to comparing by create date
    compare_date(convert(create_date), x,)

# create_folder(DESKTOP, 'TestingPy')
