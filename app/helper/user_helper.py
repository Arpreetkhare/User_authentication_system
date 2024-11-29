from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# app/helpers.py

import logging

# Configure the logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('debug.log')  # This is where the logs will be stored
file_handler.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)


# Create a formatter and add it to the handler
formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
    'Function: %(funcName)s - Line: %(lineno)d')
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# You can now use this logger throughout the project




