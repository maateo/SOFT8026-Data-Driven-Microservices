from flask import Flask 
 
import redis 
 
app = Flask(__name__) 
 
@app.route('/') 
def print_logs():
    output = ''
    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("log.greeter_server*"):
            value = str(conn.get(key))
            output += str(key) + value + '<br>'
    except Exception as ex:
        output = 'Error:' + str(ex)
    return output

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')