import os
import csv

from eth_async.utils.utils import update_dict
from eth_async.utils.files import touch, write_json, read_json

from data import config
from data.models import WalletCSV

def create_files():
    touch(path=config.FILES_DIR)
    touch(path=config.LOG_FILE, file=True)
    touch(path=config.ERRORS_FILE, file=True)

    if not os.path.exists(config.IMPORT_FILE):
        with open(config.IMPORT_FILE, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(WalletCSV.header)

    try:
        current_settings: dict | None = read_json(path=config.SETTINGS_FILE)
    except Exception:
        current_settings = {}

    settings = {
        'maximum_gas_price': 40,
        'minimal_balance': 0.0005,
        'eth_amount_for_swap': {'from': 0.01, 'to': 0.2 },
        'actions_delay': {'from': 28800, 'to': 43200},
        'telegram': {
            'send_notifications': False,
            'bot_key': "",
            'chat_id': ""
        }
        #'use_neonpass_bridge': False,
        # 'swap_on_jupiter': {
        #     'enabled': False,
        #     'amount': {'from': 0.001, 'to': 0.01}
        # }
    }
    write_json(path=config.SETTINGS_FILE, obj=update_dict(modifiable=current_settings, template=settings), indent=2)


create_files()
