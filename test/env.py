from environs import Env

env = Env()
env.read_env()

API_BASE = "https://apitable.com"

SPACE_ID = env("SPACE_ID")
FOLDER_ID = env("FOLDER_ID")
DATASHEET_ID = env("DATASHEET_ID")
DATASHEET_ID_FOR_GET = env("DATASHEET_ID_FOR_GET")
VIEW_ID = env("VIEW_ID")
TOKEN = env("TOKEN")

DOMAIN = "https://" + env("DOMAIN") or API_BASE
