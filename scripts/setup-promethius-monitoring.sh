microk8s.kubectl apply -f ../kubernetes/promethius/promethius-namespace.yml
microk8s.kubectl apply -f ../kubernetes/promethius/clusterRole.yml
microk8s.kubectl apply -f ../kubernetes/promethius/config-map.yml
microk8s.kubectl apply -f ../kubernetes/promethius/prometheus-deployment.yml