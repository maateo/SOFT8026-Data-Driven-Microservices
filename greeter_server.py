# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import datetime
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

import redis

import time

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def __init__(self):
        self.greetings = ["Hello ", "Greetings ", "All the best ", "Nice to meet you "]

    def SayHello(self, request, context):
        for g in self.greetings:
            response = helloworld_pb2.HelloReply(message=g + request.name)
            try:
                conn = redis.StrictRedis(host='redis', port=6379) 
                conn.set("log.greeter_server." + str(datetime.datetime.now()), g + request.name) 
            except Exception as ex: 
                print('Error:', ex)
            yield response


def serve():
	    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
	    server.add_insecure_port('[::]:50051')
	    server.start()
	    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
