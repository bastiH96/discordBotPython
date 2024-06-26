from dotenv import load_dotenv
import discord
import os

load_dotenv()

GUILD_ID = discord.Object(int(os.getenv("GUILD_ID")))

TOKEN = os.getenv("TOKEN")

DB_PATH = os.getenv("DB_PATH")

EXCEL_FOLDER = os.getenv("EXCEL_FOLDER")
