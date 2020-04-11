echo "Setting up deployments and services"
microk8s.kubectl create -f '../kubernetes/tweet-server-deploy.yml'
microk8s.kubectl create -f '../kubernetes/tweet-server-svc.yml'
microk8s.kubectl create -f '../kubernetes/reddit-post-server-deploy.yml'
microk8s.kubectl create -f '../kubernetes/reddit-post-server-svc.yml'
microk8s.kubectl create -f '../kubernetes/redis-deploy.yml'
microk8s.kubectl create -f '../kubernetes/redis-svc.yml'
microk8s.kubectl create -f '../kubernetes/tweet-analysis-client-deploy.yml'
microk8s.kubectl create -f '../kubernetes/reddit-analysis-client-deploy.yml'
microk8s.kubectl create -f '../kubernetes/website-deploy.yml'
microk8s.kubectl create -f '../kubernetes/website-svc.yml'

echo "Setting up Kubeless"
export RELEASE=$(curl -s https://api.github.com/repos/kubeless/kubeless/releases/latest | grep tag_name | cut -d '"' -f 4)
microk8s.kubectl create ns kubeless
microk8s.kubectl create -f https://github.com/kubeless/kubeless/releases/download/$RELEASE/kubeless-$RELEASE.yaml

echo "Deployments, services and kubeless function starting"

kubectl wait --for=condition=Ready pods --all -n kubeless
microk8s.config > $HOME/.kube/config
kubeless function deploy get-word-and-vowel-count --runtime python2.7 --from-file '../kubeless_function.py' --handler kubeless_function.get_word_and_vowel_count

kubectl wait --for=condition=Ready pods --all --all-namespaces
echo ""
echo "Everything is ready"