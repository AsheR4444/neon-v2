import os
import sys
from pathlib import Path

from loguru import logger
from dotenv import load_dotenv

load_dotenv()

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'data', 'abis')
FILES_DIR = os.path.join(ROOT_DIR, 'files')

LOG_FILE = os.path.join(FILES_DIR, 'log.log')
ERRORS_FILE = os.path.join(FILES_DIR, 'errors.log')

IMPORT_FILE = os.path.join(FILES_DIR, 'import.csv')

SETTINGS_FILE = os.path.join(FILES_DIR, 'settings.json')

# EXTENSIONS_DIR = os.path.join(ROOT_DIR, 'extensions',)
# RABBY_DIR = os.path.join(EXTENSIONS_DIR, 'rabby')
# BACKPACK_DIR = os.path.join(EXTENSIONS_DIR, 'backpack')

WALLETS_DB = os.path.join(FILES_DIR, 'wallets.db')

logger.add(ERRORS_FILE, level='ERROR')
logger.add(LOG_FILE, level='INFO')

WALLET_PASSWORD = "Qwerty123!"
ATTEMPTS_NUMBER_RESTORE = 10
DELAY_IN_CASE_OF_ERROR = 3600