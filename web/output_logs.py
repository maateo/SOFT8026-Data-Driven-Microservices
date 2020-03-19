import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = ''
    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        keys = conn.scan_iter("tweets*")
        keys = sorted(keys, reverse=True)

        for key in keys:
            value = str(conn.get(key))
            output += str(key) + " AAAA " + value + '<br>'  # Style the output lines
    except Exception as ex:
        output = 'Error:' + str(ex)
    return output


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
