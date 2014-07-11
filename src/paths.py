import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
STORAGE_DIR = os.path.join(THIS_DIR, '..', 'data')
GIFS_DIR = os.path.join(STORAGE_DIR, 'gifs')
TOKENS_DIR = os.path.join(STORAGE_DIR, 'tokens')
DB_DIR = os.path.join(STORAGE_DIR, 'sqlite3')

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

def storage_dir():
    return STORAGE_DIR

def storage_file(filename):
    return os.path.join(storage_dir(), filename)

if not os.path.exists(GIFS_DIR):
    os.makedirs(GIFS_DIR)

def gifs_dir():
    return GIFS_DIR

def gifs_file(filename):
    return os.path.join(gifs_dir(), filename)

if not os.path.exists(TOKENS_DIR):
    os.makedirs(TOKENS_DIR)

def tokens_dir():
    return TOKENS_DIR

def tokens_file(filename):
    return os.path.join(tokens_dir(), filename)

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def db_dir():
    return DB_DIR

def db_file(filename):
    return os.path.join(db_dir(), filename)
