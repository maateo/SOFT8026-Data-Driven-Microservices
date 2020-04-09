import redis
from flask import Flask

app = Flask(__name__)


@app.route('/')
def print_logs():
    output = ''

    try:
        conn = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

        tweets_analytics_output = tweets_analytics(conn)
        tweets_table_output = tweets_table(conn)
        reddit_analytics_output = reddit_posts_analytics(conn)
        reddit_table_output = reddit_posts_table(conn)

        output += combine_outputs(tweets_analytics_output, tweets_table_output, reddit_analytics_output, reddit_table_output)

    except Exception as ex:
        output = 'Error:' + str(ex) + '<META HTTP-EQUIV="refresh" CONTENT="1">'

    return output


def tweets_table(conn):
    row_html = """
                 <tr>
                    <td>
                      <div style="background-color:%s;">
                        <div style="text-align: center;"> 
                          <small><i>@%s</i></small>
            
                          <br>
            
                          %s
            
                          <br>
            
                          <small>
                            <strong> Tweet Id: </strong> %s
                            <strong> Words:</strong> %s
                            <strong> Time analysed: </strong> %s
                          </small>
                        </div>
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

        output += row_html % (background_color, data["user"], data["text"], data["id"], data["word_count"], data["time_analysed"])

    return output


def tweets_analytics(conn):
    html = """
            <div style="text-align: center;"><h3> All Time Total </h3></div>
            Total vowels: %s
            <br>
            Total Words: %s 
            <br>
            Average vowels per word: %s
        
        
            <div style="text-align: center;"><h3> 3 Minute Sentiment </h3></div>
            %s
        
            <div style="text-align: center;"><h3> Most of... </h3></div>
            <strong>Tweet with most words:</strong> %s 
            <br><br>
            Word count: %s
           """

    total_vowel_count = str(conn.get("total_vowel_count"))
    total_word_count = str(conn.get("total_word_count"))

    sentiment_list = list(map(int, conn.get("3_minute_sentiment")[1:-1].split(",")))

    sentiment_message = ''
    if sentiment_list[0] == sentiment_list[4]:
        sentiment_message = "Just as many positive as negative" + "<br>" + "(" + str(sentiment_list[4]) + " pos and " + str(sentiment_list[0]) + " neg)"
    elif sentiment_list.index(max(sentiment_list)) == 0:
        sentiment_message = "Most are negative" + "<br>" + "(" + str(sentiment_list[4]) + " pos vs " + str(sentiment_list[0]) + " neg)"
    elif sentiment_list.index(max(sentiment_list)) == 4:
        sentiment_message = "Most are positive" + "<br>" + "(" + str(sentiment_list[4]) + " pos vs " + str(sentiment_list[0]) + " neg)"

    ath_word = str(conn.get("all_time_high_word"))
    ath_word_count = str(conn.get("all_time_high_word_count"))

    return html % (total_vowel_count, total_word_count, round(int(total_vowel_count) / int(total_word_count), 2), sentiment_message, ath_word, ath_word_count)


def reddit_posts_table(conn):
    html = """
                <tr>
                    <td>
                        <div style="text-align: center;">
                            <small><i>%s</i></small>
                
                            <br>
                
                            %s
                
                            <br>
                
                            <small>
                                Reddit URL: %s
                            </small>
                
                            <br>
                
                            <small>
                                <strong> Reddit Post Id: </strong> %s
                                <strong> Words:</strong> %s
                                <strong> Time analysed: </strong> %s
                            </small>
                        </div>
                    </td>
                </tr>
           """

    keys = conn.scan_iter("reddit_posts.*")
    keys = sorted(keys, reverse=True)

    output = ''

    for key in keys:
        data = conn.hgetall(key)

        output += html % (data["author"], data["title"], data["full_link"], data["id"], data["word_count"], data["time_analysed"])

    return output


def reddit_posts_analytics(conn):
    html = """
            <div style="text-align: center;"><h3> All Time Total </h3></div>
            Total vowels: %s
            <br>
            Total Words: %s 
            <br>
            Average vowels per word: %s
        
        
            <div style="text-align: center;"><h3> 3 Minute Sentiment </h3></div>
            Over 18: %s
            <br>
            Under 18: %s
        
            <div style="text-align: center;"><h3> Most of... </h3></div>
            <strong>Reddit Post with most words:</strong> %s 
            <br><br>
            Word count: %s
           """

    total_vowel_count = str(conn.get("reddit_posts_total_vowel_count"))
    total_word_count = str(conn.get("reddit_posts_total_word_count"))

    over_18_count = conn.get("reddit_posts_3_minute_over_18")
    under_18_count = conn.get("reddit_posts_3_minute_under_18")

    ath_word = str(conn.get("reddit_posts_all_time_high_word"))
    ath_word_count = str(conn.get("reddit_posts_all_time_high_word_count"))

    return html % (total_vowel_count, total_word_count, round(int(total_vowel_count) / int(total_word_count), 2), over_18_count, under_18_count, ath_word, ath_word_count)


def combine_outputs(tweets_analytics, tweets_table, reddit_analytics, reddit_table):
    output = """
            <META HTTP-EQUIV="refresh" CONTENT="1.5">
            <style> 
              #wrapper {
                display: flex;
              }
              #first {
                width: 50%;
                padding: 1em;
              }
              #second {
                width: 50%;
                padding: 1em;
              }
              h3 {
                margin-top: 5em;
              }
            </style>
            <div id="wrapper">
            """
    # Left side
    output += """
              <div id="first">
              """
    output += tweets_analytics
    output += """
                  
                <table style="width:100%">
              """
    output += tweets_table
    output += """
                </table>
              </div>
    """

    # Right side
    output += """
              <div id="second">
              """
    output += reddit_analytics
    output += """              
                <table style="width:100%">
              """
    output += reddit_table

    output += """
                </table>
              </div>
            </div>
    """

    return output


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
