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
 