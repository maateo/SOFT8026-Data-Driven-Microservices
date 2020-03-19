import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = '''
        
    '''
    try:
        conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
        # keys = conn.scan_iter("tweets*")
        # keys = sorted(keys, reverse=True)

        output += str(conn.get("3_minute_sentiment"))

        output += "<br><br>"

        output += str(conn.get("total_vowel_count"))
        output += "<br>"
        output += str(conn.get("total_word_count"))

        output += "<br><br>"
        output += output_tweets(conn)

        output +=str(conn.get("all_time_high_word_count"))
        output +=str(conn.get("all_time_high_word"))

        # datakeys = conn.scan_iter("data*")
        #
        # for key in datakeys:
        #     data = conn.hgetall(key)
        #
        # for key in keys:
        #     value = str(conn.get(key))
        #     # output += str(key) + " AAAA " + value + '<br>'  # Style the output lines
        #     output += str(data) + " AAAA " + str(data) + '<br>'  # Style the output lines
    except Exception as ex:
        output = 'Error:' + str(ex)
    return output


def output_tweets(conn):
    keys = conn.scan_iter("tweets*")
    keys = sorted(keys, reverse=True)

    output = ''

    for key in keys:
        data = conn.hgetall(key)
        # decoded_data = data.
        output += str(data)

    return output


def combine_outputs():
    output = """
                <style> 
              #wrapper {
                display: flex;
                border: 1px solid black;
              }
              #first {
                border: 1px solid red;
                width: 30%;
                padding: 1em;
              }
              #second {
                border: 1px solid green;
                width: 70%;
                padding: 1em;
              }
            </style>
            
            <div id="wrapper">
            
              <div id="first">
            
                <center><h3> Total Letters </h3></center>
                Total Letters: 3
            
            
                <center><h3> 3 Minute Sentiment </h3></center>
                All good 
            
                <center><h3> Most of... </h3></center>
                Tweet with most words: 
                <br>
                Word count: 5
            
              </div>
            
              <div id="second">
            
                <table style="width:100%">
                  <tr>
                    <td>
                      <div>
                        <center> 
                          <small><i>joe1232</i></small>
            
                          <br>
            
                          I love this world
            
                          <br>
            
                          <small>
                            <strong> Tweet Id: </strong> 75354
                            <strong> Time analised: </strong> 11:30am
                            <strong> Words:</strong> 20
                          </small>
                        </center>
                      </div>
                    </td>
                  </tr>
                </table>
              </div>
            </div>




    """


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
