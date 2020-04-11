#microk8s enable dashboard metrics-server
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
token=$(microk8s kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s kubectl -n kube-system describe secret $token
echo "Waiting for everything to come online"
kubectl wait --for=condition=Ready pods --all -n kubernetes-dashboard
echo "Use the above token to access the panel on https://127.0.0.1:10443"
microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard 10443:443
