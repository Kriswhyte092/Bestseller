from dotenv import load_dotenv
import os


#föll sem þarf að kalla strax í byrjun
load_dotenv()

#api keys and urls
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

#Database connection
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#Timezone
TIMEZONE = "UTC"

#Scheduler config
SCEDULED_TASK_TIME = "00:01"
SCHEDULED_TASK_DAY = "22"

#Logging
LOG_LEVER = "DEBUG"
LOG_FILE = "payroll_system.log"



