import asyncio

from loguru import logger

from functions.create_files import create_files
from functions.Import import Import
from functions.starter import starter
from utils.show_info import show_info

if __name__ == '__main__':
    show_info()
    create_files()

    print('''  Select the action:
1) Import wallets from the spreadsheet to the DB;
2) Start the script;
3) Exit.''')

    try:
        action = int(input('> '))
        if action == 1:
            asyncio.run(Import.wallets())

        elif action == 2:
            asyncio.run(starter())

    except KeyboardInterrupt:
        print()

    except ValueError as err:
        logger.error(f'Value error: {err}')

    except BaseException as e:
        logger.error(f'Something went wrong: {e}')
