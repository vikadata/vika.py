from environs import Env

env = Env()
env.read_env()

API_BASE = "https://vika.cn"
TEST_TABLE = env("TEST_TABLE")
TEST_API_TOKEN = env("TEST_API_TOKEN")
TEST_API_BASE = env("TEST_API_BASE") or API_BASE
TEST_SPACE_ID = env("TEST_SPACE_ID")
TEST_FOLDER_ID = env("TEST_FOLDER_ID")
