import os
import sys
import datetime
import logging

import yaml

CONFIG_FILE = 'config.yml'
GITLAB_USER_LOGIN = os.environ['GITLAB_USER_LOGIN']

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

def load_config(filename: str) -> dict:
    with open(filename) as file:
        return yaml.safe_load(file)
    
def unpack_config(config: dict) -> tuple:
    try:
        bypass_users = config['glass_breaker_group']
        freezing_dates = config['freezing_dates']
        return (bypass_users, freezing_dates)
    except KeyError as e:
        logging.error(f'Error: {e} is not a valid key in the config file')
        sys.exit(1)

def is_user_in_bypass(username: str, bypass_users: list) -> bool:
    return username in bypass_users

def is_freezing_period(date_from: datetime.date, date_to: datetime.date) -> bool:
    today = datetime.date.today()
    if today >= date_from and today <= date_to:
        return True
    return False

def main():
    config = load_config(CONFIG_FILE)
    bypass_users, freezing_dates = unpack_config(config)
    
    # Exits the pipeline if user is authorized to bypass the freezing
    if is_user_in_bypass(GITLAB_USER_LOGIN, bypass_users):
        logging.info(f'User {GITLAB_USER_LOGIN} is in the bypass group')
        sys.exit(0)

    for period, freezing_date in freezing_dates.items():
        date_from = freezing_date.get('from')
        date_to = freezing_date.get('to')
        if is_freezing_period(date_from, date_to):
            logging.warning(f'We are currently in the {period} code freezing period')
            sys.exit(1)

if __name__ == '__main__':
    main()
