# Copyright 2018 The gRPC Authors
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
"""The reflection-enabled version of gRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
from grpc_reflection.v1alpha import reflection

import Assignment1_pb2
import Assignment1_pb2_grpc


class Greeter(Assignment1_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return Assignment1_pb2.HelloReply(
            target=str("0"),
            id=str("1467810369"),
            date=str("Mon Apr 06 22:19:45 PDT 2009"),
            flag=str("NO_QUERY"),
            user=str("_TheSpecialOne_"),
            text=str("@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D")
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Assignment1_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    SERVICE_NAMES = (
        Assignment1_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
