import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = ''

    try:
        conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

        analytics_html = output_analytics(conn)
        tweets_html = output_tweets(conn)

        output += combine_outputs(analytics_html, tweets_html)

    except Exception as ex:
        output = 'Error:' + str(ex) + '<META HTTP-EQUIV="refresh" CONTENT="1">'

    return output


def output_tweets(conn):
    html = """
                 <tr>
                    <td>
                      <div style="background-color:%s;">
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

        background_color = ''
        if int(data["target"]) == 0:
            background_color = "coral"
        elif int(data["target"]) == 4:
            background_color = "lightblue"

        output += html % (background_color, data["user"], data["text"], data["id"], data["word_count"], data["time_analysed"])

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
                <strong>Tweet with most words:</strong> %s 
                <br><br>
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

    return html % (total_vowel_count, total_word_count, round(int(total_vowel_count) / int(total_word_count), 2), sentiment_message, ath_word, ath_word_count)


def combine_outputs(analytics_html, tweets_html):
    output = """
            <META HTTP-EQUIV="refresh" CONTENT="1.5">
            <style> 
              #wrapper {
                display: flex;
              }
              #first {
                width: 30%;
                padding: 1em;
              }
              #second {
                width: 70%;
                padding: 1em;
              }
              h3 {
                margin-top: 5em;
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
