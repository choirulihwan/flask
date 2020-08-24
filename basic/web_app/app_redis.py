# compose_flask/app.py
from flask import Flask
from redis import Redis

def create_app():
    app = Flask(__name__)
    redis = Redis(host='redis', port=6379)

    @app.route('/')
    def index():
        redis.incr('hits')
        return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


    return app