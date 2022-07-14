import logging

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include('components/base.py', 'components/database.py', 'components/local.py')
logger = logging.getLogger(__name__)
