import os
import configparser
import mechanicalsoup

from getpass import getpass

from .exceptions import NeedToLoginException

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".fl-data-dl")

def get_credentials():
    # are there credentials in the config file?
    config = configparser.ConfigParser()
    
    config.read(CONFIG_PATH)

    user = config.get("fl", "user", fallback=None)
    pw = config.get("fl", "pw", fallback=None)

    # if not, ask for them
    if user is None or pw is None:
        user, pw = get_new_credentials()

    return user, pw

def get_new_credentials():
    print("Set your FutureLearn username and password")

    user = input("Username :")
    pw = getpass("Password :")

    return user, pw

def store_credentials():
    user, pw = get_new_credentials()

    config = configparser.ConfigParser()
    config.add_section("fl")
    config.set("fl", "user", user)
    config.set("fl", "pw", pw)

    # write new config gile
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def login(credentials=None):
    """
    Logs in to FutureLearn. 
    
    Returns a mechanicalsoup.StatefulBrowser which is required to get data.

    :param List credentials:
        Optional: A list of [user, password] to login.
    
    :return:
            A browser object required by [get data] methods.
    """
    if credentials is None:
        user, pw = get_credentials()
    else:
        user = credentials[0]
        pw = credentials[1]
    b = mechanicalsoup.StatefulBrowser(soup_config={'features':'lxml'}, raise_on_404=True, user_agent='Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',)
    b.open("https://www.futurelearn.com/sign-in")
    b.select_form('form[action="/sign-in"]')
    b["email"] = user
    b["password"] = pw
    response = b.submit_selected()
    return b