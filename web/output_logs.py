import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = ''

    try:
        conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
        # keys = conn.scan_iter("tweets*")
        # keys = sorted(keys, reverse=True)

        analytics_html = output_analytics(conn)
        tweets_html = output_tweets(conn)

        print(type(analytics_html))
        print(type(tweets_html))

        output += combine_outputs(analytics_html, tweets_html)
        #
        # output += analytics_html
        # output += tweets_html

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
    html = """
                 <tr>
                    <td>
                      <div>
                        <center> 
                          <small><i>@%s</i></small>
            
                          <br>
            
                          %s
            
                          <br>
            
                          <small>
                            <strong> Tweet Id: </strong> %s
                            <strong> Words:</strong> %s
                            <strong> Time analysed: </strong> %s
                          </small>
                        </center>
                      </div>
                    </td>
                  </tr>
               """

    keys = conn.scan_iter("tweets*")
    keys = sorted(keys, reverse=True)

    output = ''

    for key in keys:
        data = conn.hgetall(key)
        # decoded_data = data.
        output += html % (data["user"], data["text"], data["id"], data["word_count"], data["time_analysed"])

    return output


def output_analytics(conn):
    html = """
              <div id="first">
            
                <center><h3> All Time Total </h3></center>
                Total vowels: %s
                <br>
                Total Words: %s 
                <br>
                Average vowels per word: %s
            
            
                <center><h3> 3 Minute Sentiment </h3></center>
                %s
            
                <center><h3> Most of... </h3></center>
                Tweet with most words: %s 
                <br>
                Word count: %s
            
              </div>
           """

    total_vowel_count = str(conn.get("total_vowel_count"))
    total_word_count = str(conn.get("total_word_count"))

    sentiment_list = list(map(int, conn.get("3_minute_sentiment")[1:-1].split(",")))

    sentiment_message = ''
    if sentiment_list[0] == sentiment_list[4]:
        sentiment_message = "Just as many positive as negative"
    elif sentiment_list.index(max(sentiment_list)) == 0:
        sentiment_message = "Most are negative" + "<br>" + "(" + str(sentiment_list[4]) + " pos vs " + str(sentiment_list[0]) + " neg)"
    elif sentiment_list.index(max(sentiment_list)) == 4:
        sentiment_message = "Most are positive" + "<br>" + "(" + str(sentiment_list[4]) + " pos vs " + str(sentiment_list[0]) + " neg)"

    ath_word = str(conn.get("all_time_high_word"))
    ath_word_count = str(conn.get("all_time_high_word_count"))

    return html % (total_vowel_count, total_word_count, (int(total_vowel_count) / int(total_word_count)), sentiment_message, ath_word, ath_word_count)


def combine_outputs(analytics_html, tweets_html):
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
            """
    output += analytics_html
    output += """
              <div id="second">
            
                <table style="width:100%">
                """
    output += tweets_html
    output += """
                </table>
              </div>
            </div>
    """

    return output


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
