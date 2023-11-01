from dotenv import load_dotenv
import os

load_dotenv()

ALG = str(os.environ.get('ALG'))
KEY = str(os.environ.get('KEY'))
USERNAME = str(os.environ.get('LOGIN'))
PASSWORD = str(os.environ.get('PASSWORD'))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))


