from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN")
POSTGRES_DSN = getenv("POSTGRES_DSN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not POSTGRES_DSN:
    raise RuntimeError("POSTGRES_DSN is not set")

# todo: переписать на использование класса
