import uuid
from datetime import datetime

#вспомогательные функции
async def generate_id() -> int:
    unique_id = uuid.uuid4()
    numeric_id = int(unique_id.int)
    id = numeric_id % 100000
    
    return id


async def convert_date(date: str):
    time, date_part = date.split()
    day, month, year = date_part.split('.')
    return f"{year}-{month}-{day} {time}"
    
    # time, day = date.split()
    # return time.split(":") + day.split(".")


async def valid_date(date: str)-> bool:
    try:
        input_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        return input_date > datetime.now()
    except:
        return False