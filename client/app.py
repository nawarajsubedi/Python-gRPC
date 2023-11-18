import os

import grpc
import hello_pb2
import hello_pb2_grpc

TARGET = os.environ.get('GRPC_TARGET', 'localhost:50051')


def run():
    with grpc.insecure_channel(TARGET) as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        response = stub.printHello(hello_pb2.HelloWorldRequest(id="33"))
    print(response.id)

if __name__ == '__main__':
    run()
