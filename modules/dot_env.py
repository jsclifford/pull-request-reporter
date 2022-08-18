from dotenv import load_dotenv
from pathlib import Path
import os


def load_env():
    load_dotenv()
    env_path = Path('../')/'.env'
    load_dotenv(dotenv_path=env_path)
