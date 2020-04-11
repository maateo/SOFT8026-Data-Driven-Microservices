MY_PATH="`dirname \"$0\"`"

sh $MY_PATH/setup-deployments-services-functions.sh
sh $MY_PATH/setup-monitoring.sh "Website with analytics and tweets/posts is available on http://127.0.0.1:30000"
