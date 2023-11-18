import os
import sys

import grpc
import hello_pb2
import hello_pb2_grpc

TARGET = os.environ.get('GRPC_TARGET', 'localhost:50051')
TIMEOUT = float(os.environ.get('GRPC_TIMEOUT', 5))


def run():
    with grpc.insecure_channel(TARGET) as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        response = stub.printHello(hello_pb2.HelloWorldRequest(id="33"), timeout=TIMEOUT)
    print(response.id)


if __name__ == '__main__':
    try:
        run()
    except grpc.RpcError as e:
        print(f'error: {e.code().name} {e.details()}', file=sys.stderr)
        sys.exit(1)
