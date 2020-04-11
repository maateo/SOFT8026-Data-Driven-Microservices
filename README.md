# Running the project
Please place the `training.1600000.processed.noemoticon.csv` file into the root of this project. The file can be downloaded from https://www.kaggle.com/kazanova/sentiment140/data.

# Building proto files
### Adapted from: https://grpc.io/docs/quickstart/python/

#### Install prerequisites 
```
python -m pip install --upgrade pip
python -m pip install grpcio
python -m pip install grpcio-tools
```

#### Generate the proto files
`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Assignment1.proto`


# gRPC streaming
https://github.com/grpc/grpc.github.io/blob/master/docs/tutorials/basic/python.md


# Super useful Docker commands
 - `sudo docker system prune`
 - `sudo docker-compose up --build`
 - `sudo docker stop $(sudo docker ps -a -q)` - Stops all running containers
  
 
# microk8s
## Avoid pulling images
It is possible to avoid having to pull images from dockerhub if they are available locally. 
To create images locally, build the docker file seperately, or use the `sudo docker-compose build` command.
The local images should saved as a tar file, and then imported to microk8s. 
 - Tag the image as usual
 - Save the image into a .tar file `sudo docker save matalt/reddit-post-server > reddit-post-server.tar`
 - Import the image into microk8s using `microk8s ctr image import reddit-post-server.tar`
 
 ## Other useful commands
 - `microk8s.kubectl create -f reddit-post-server-deploy.yml`
 - `microk8s.kubectl get pods`
 - `microk8s.kubectl get deployments`
 - `microk8s.kubectl get services`
 - `microk8s.kubectl delete deployment.apps/reddit-post-server-deploy`
 - `microk8s ctr images ls`
 - `microk8s.kubectl create -f reddit-post-server-svc.yml`
 - `microk8s reset`
 - `microk8s enable dns storage`



# Saving some time

## Tagging
 - `sudo docker tag soft8026-data-driven-microservices-assignment-1_website matalt/website:latest`
 - `sudo docker tag soft8026-data-driven-microservices-assignment-1_reddit-analysis-client matalt/reddit-analysis-client:latest`
 - `sudo docker tag soft8026-data-driven-microservices-assignment-1_reddit-post-server matalt/reddit-post-server:latest`
 - `sudo docker tag soft8026-data-driven-microservices-assignment-1_tweet-analysis-client matalt/tweet-analysis-client:latest`
 - `sudo docker tag soft8026-data-driven-microservices-assignment-1_tweet-server matalt/tweet-server:latest`

## Pushing to dockerhub
 - `sudo docker push matalt/website:latest`
 - `sudo docker push matalt/reddit-analysis-client:latest`
 - `sudo docker push matalt/reddit-post-server:latest`
 - `sudo docker push matalt/tweet-analysis-client:latest`
 - `sudo docker push matalt/tweet-server:latest`
 
## Moving images docker to microk8s
### Saving
 - `sudo docker save matalt/website > website.tar`
 - `sudo docker save matalt/reddit-analysis-client > reddit-analysis-client.tar`
 - `sudo docker save matalt/reddit-post-server > reddit-post-server.tar`
 - `sudo docker save matalt/tweet-analysis-client > tweet-analysis-client.tar`
 - `sudo docker save matalt/tweet-server > tweet-server.tar`

### Importing
 - `microk8s ctr image import website.tar`
 - `microk8s ctr image import reddit-analysis-client.tar`
 - `microk8s ctr image import reddit-post-server.tar`
 - `microk8s ctr image import tweet-analysis-client.tar`
 - `microk8s ctr image import tweet-server.tar`


## Deploy everything
 - `microk8s.kubectl create -f tweet-server-deploy.yml`
 - `microk8s.kubectl create -f tweet-server-svc.yml`
 - `microk8s.kubectl create -f reddit-post-server-deploy.yml`
 - `microk8s.kubectl create -f reddit-post-server-svc.yml`
 - `microk8s.kubectl create -f redis-deploy.yml`
 - `microk8s.kubectl create -f redis-svc.yml`
 - `microk8s.kubectl create -f tweet-analysis-client-deploy.yml`
 - `microk8s.kubectl create -f reddit-analysis-client-deploy.yml`
 - `microk8s.kubectl create -f website-deploy.yml`
 - `microk8s.kubectl create -f website-svc.yml`

 
## Delete everything
### Deployments
 - `microk8s.kubectl delete deployment.apps/tweet-server-deploy`
 - `microk8s.kubectl delete deployment.apps/reddit-post-server-deploy`
 - `microk8s.kubectl delete deployment.apps/redis-deploy`
 - `microk8s.kubectl delete deployment.apps/tweet-analysis-client-deploy`
 - `microk8s.kubectl delete deployment.apps/reddit-analysis-client-deploy`
 - `microk8s.kubectl delete deployment.apps/website-deploy`
 ## Services
 - `microk8s.kubectl delete services/tweet-server`
 - `microk8s.kubectl delete services/reddit-post-server`
 - `microk8s.kubectl delete services/redis`
 - `microk8s.kubectl delete services/website`



# Kubeless
## Adding kubeless namespace and pods to kubernetes
Assuming you  have kubeless installed
 - `export RELEASE=$(curl -s https://api.github.com/repos/kubeless/kubeless/releases/latest | grep tag_name | cut -d '"' -f 4)`
 - `microk8s.kubectl create ns kubeless`
 - `microk8s.kubectl create -f https://github.com/kubeless/kubeless/releases/download/$RELEASE/kubeless-$RELEASE.yaml`
 - `microk8s.kubectl get pods -n kubeless`
 
Other useful commands

 - `microk8s.config > $HOME/.kube/config`
 - `kubeless function deploy get-word-and-vowel-count --runtime python2.7 --from-file kubeless_function.py --handler kubeless_function.get_word_and_vowel_count`

#### You can also deploy with requirements (dependencies)
 - `kubeless function deploy get-word-and-vowel-count --runtime python2.7 --from-file kubeless_function.py --handler kubeless_function.get_word_and_vowel_count --dependencies requirements.txt`
 
#### Deleting
 - `kubeless function delete get-word-and-vowel-count`

#### Executing 
 - `kubeless function call get-word-and-vowel-count --data "HELLO WORLD!"`
or 
 - `microk8s.kubectl get services` --> Take the CLUSTER-IP
 - `curl -L --data 'hello world a' 10.152.183.219:8080/api/v1/namespaces/default/services/get-word-and-vowel-count`


# Deleting stubborn namespace (kubeless in this example)
 - `kubectl get namespace kubeless -o json > tmp.json`
 - `nano tmp.json` -> remove kubernetes finalizer
 - `kubectl proxy` -> Do this in a new window to start a proxy. It will be 127.0.0.1:8001 by default
 - `curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json 127.0.0.1:8001/api/v1/namespaces/kubeless/finalize`
 - `microk8s.kubectl get namespace`