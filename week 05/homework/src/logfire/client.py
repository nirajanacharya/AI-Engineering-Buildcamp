# Setup logfire query client
import os
from logfire.query_client import LogfireQueryClient

def get_client():
    token = os.getenv('LOGFIRE_READ_TOKEN')
    return LogfireQueryClient(read_token=token)
