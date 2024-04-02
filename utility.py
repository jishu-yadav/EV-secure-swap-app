import uuid
from datetime import datetime

def generate_unique_id():
    unique_id = uuid.uuid4()
    return str(unique_id)

def get_date():
    timestamp_value = datetime.now()
    return timestamp_value

