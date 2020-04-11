microk8s.kubectl delete deployment.apps/tweet-server-deploy
microk8s.kubectl delete deployment.apps/reddit-post-server-deploy
microk8s.kubectl delete deployment.apps/redis-deploy
microk8s.kubectl delete deployment.apps/tweet-analysis-client-deploy
microk8s.kubectl delete deployment.apps/reddit-analysis-client-deploy
microk8s.kubectl delete deployment.apps/website-deploy
microk8s.kubectl delete services/tweet-server
microk8s.kubectl delete services/reddit-post-server
microk8s.kubectl delete services/redis
microk8s.kubectl delete services/website

kubeless function delete get-word-and-vowel-count
