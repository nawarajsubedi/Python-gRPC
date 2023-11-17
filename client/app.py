from __future__ import print_function

import grpc
import hello_pb2
import hello_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        response = stub.printHello(hello_pb2.HelloWorldRequest(id="33"))
    print(response.id)

if __name__ == '__main__':
    run()

