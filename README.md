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


# Super useful Docker commands
 - `sudo docker system prune`
 - `sudo docker-compose up --build`
 