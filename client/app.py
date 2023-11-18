import argparse
import os
import sys

import grpc
import hello_pb2
import hello_pb2_grpc

TARGET = os.environ.get('GRPC_TARGET', 'localhost:50051')
TIMEOUT = float(os.environ.get('GRPC_TIMEOUT', 5))


def print_hello(stub, args):
    response = stub.printHello(hello_pb2.HelloWorldRequest(id=args.id), timeout=TIMEOUT)
    print(response.id)


def get_args():
    parser = argparse.ArgumentParser(description='client for the hello grpc server')
    parser.add_argument('--target', default=TARGET, help='server address (default %(default)s)')
    # no command given -> call printHello like before
    parser.set_defaults(func=print_hello, id='33')
    sub = parser.add_subparsers()

    p = sub.add_parser('print-hello', help='call printHello')
    p.add_argument('--id', default='33')
    p.set_defaults(func=print_hello)

    return parser.parse_args()


def main():
    args = get_args()
    with grpc.insecure_channel(args.target) as channel:
        stub = hello_pb2_grpc.HelloStub(channel)
        args.func(stub, args)


if __name__ == '__main__':
    try:
        main()
    except grpc.RpcError as e:
        print(f'error: {e.code().name} {e.details()}', file=sys.stderr)
        sys.exit(1)
