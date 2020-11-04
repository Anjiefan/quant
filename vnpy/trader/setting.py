"""
Global setting of VN Trader.
"""

from logging import CRITICAL
from typing import Dict, Any
from tzlocal import get_localzone
import os
from .utility import load_json

APP_ENV = os.getenv('APP_ENV')
# APP_ENV = 'prod'
if APP_ENV == 'prod':
    from ._settings.prod import *
elif APP_ENV == 'test':
    from ._settings.test import *
else:
    from ._settings.dev import *

SETTINGS: Dict[str, Any] = {
    "font.family": "Arial",
    "font.size": 12,

    "log.active": True,
    "log.level": CRITICAL,
    "log.console": True,
    "log.file": True,

    "email.server": "smtp.qq.com",
    "email.port": 465,
    "email.username": "",
    "email.password": "",
    "email.sender": "",
    "email.receiver": "",

    "rqdata.username": "",
    "rqdata.password": "",

    "database.timezone": get_localzone().zone,
    "database.driver": "mysql",                # see database.Driver
    "database.database": "capital_quant",         # for sqlite, use this as filepath
    "database.host": DB_HOST,
    "database.port": 3306,
    "database.user": "root",
    "database.password": DB_PASSWORD,
    # "database.authentication_source": "admin",  # for mongodb

    "genus.parent_host": "",
    "genus.parent_port": "",
    "genus.parent_sender": "",
    "genus.parent_target": "",
    "genus.child_host": "",
    "genus.child_port": "",
    "genus.child_sender": "",
    "genus.child_target": "",
}

# Load global setting from json file.
SETTING_FILENAME: str = "vt_setting.json"
SETTINGS.update(load_json(SETTING_FILENAME))


def get_settings(prefix: str = "") -> Dict[str, Any]:
    prefix_length = len(prefix)
    return {k[prefix_length:]: v for k, v in SETTINGS.items() if k.startswith(prefix)}

