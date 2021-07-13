import platform
import time
import redis
import flask
# from flask import Flask
app = flask.Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

PYTHON_VERSION = platform.python_version()
FLASK_VERSION = flask.__version__
REDIS_VERSION = cache.execute_command('INFO')['redis_version']

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
        retries -= 1
        time.sleep(0.5)

@app.route('/hits')
def hits():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/')
def hello():
    # return 'python: {} flask: {} redis: {}'.format(PYTHON_VERSION, FLASK_VERSION, REDIS_VERSION)
    return flask.render_template('index.html', python_version=PYTHON_VERSION, flask_version=FLASK_VERSION, redis_version=REDIS_VERSION)
