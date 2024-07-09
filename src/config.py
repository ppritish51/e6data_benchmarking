import os
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    config = {
        'USERNAME': os.getenv('USERNAME'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'DATABASE': os.getenv('DATABASE'),
        'PORT': int(os.getenv('PORT', 80)),
        'CATALOG': os.getenv('CATALOG', 'glue')
    }
    return config
