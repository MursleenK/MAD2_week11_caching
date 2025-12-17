from flask import Flask
from flask_caching import Cache
from time import sleep
import random

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "RedisCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 80,
    "CACHE_KEY_PREFIX": "my_cache_pre",#REDIS KEEPS STUFF AS KEY-VALUE. TELLS FLASK TAHT WHENEVER YOU MAKE A KEY, USE THIS PREFIX
    "CACHE_REDIS_URL": "redis://localhost:6379/1" 
    # `/1` selects Redis logical database 1 (DB index). Redis has multiple logical DBs (0–15 by default); this isolates cache data from the default DB 0. Ensures that multiples users can use the service freely.
    #CACHE_REDIS_URL is shortform of CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_PASSWORD, CACHE_REDIS_DB
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

#@cache.cached(timeout=60) 
#memoization is a special type of caching. Now, you can pass parameters and still use cache.
#Memoization creates an extra entry in the redis db for quick lookup. In this case, there will be three enteries: 2 for "/" and "/abc," and 1 more for memo table. 
#If you use memoization but without parameters, it will work the same as cache.cached. 
@cache.memoize(timeout=60)
def database_call(id):
    sleep(5)
    return "ID is:" +str(id)

@app.route("/")
# @cache.cached(timeout=60) Instead of caching individual routes, cache the time consuming function.
def index():
    a=database_call(1)
    return "Hello from root!" + str(random.randint(1,1000)) + " " + a

@app.route("/abc")
def abc():
    b=database_call(2)
    return "Hello from abc " + str(random.randint(1,1000)) + " " + b

@app.route("/delete")
def delete():
    cache.delete("common") #deletes specified key.
    cache.clear() #clears everything. 
    return "Cache cleared!"

if __name__ == "__main__":
    app.run()
    
#name of the cache keys for PATH created in redis
# my_cache_pre + view/ + request.path
# (CACHE_KEY_PREFIX) + view/ + (the path after the 127.0.0.1:5000 things in URL OR the app.route() path)

#name of the cache keys for FUNCTIONS created in redis
#<CACHE_KEY_PREFIX><specified_key_prefix>

