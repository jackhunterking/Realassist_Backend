import argparse
import os
import sys

from dotenv import load_dotenv

dotenv_path = None

if sys.argv[0] == "bootstrap.py":
    parser = argparse.ArgumentParser(description="Bootstrap the application.")
    parser.add_argument("-e", "--env")
    args = parser.parse_args()
    dotenv_path = args.env

load_dotenv(dotenv_path=dotenv_path)


ENV = os.getenv("ENV", "prod")


PORT = int(os.getenv("PORT", "3000"))
OPENAI_API_SECRET = os.getenv("OPENAI_API_SECRET")

OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
