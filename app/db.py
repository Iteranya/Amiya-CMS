# Database Stuff Init And Yea~

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

# Path to your database file
DB_PATH = 'data/website_data.json'

# Initialize TinyDB with caching for performance
db = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))

# Handy reference for queries
SiteQuery = Query()
