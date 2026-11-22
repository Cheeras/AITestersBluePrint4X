from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env
print(os.getenv("TOKEN"))