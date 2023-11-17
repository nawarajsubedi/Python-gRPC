import logging
import os
import signal
import threading
from concurrent import futures

import grpc

import hello_pb2
import hello_pb2_grpc

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('GRPC_PORT', 50051))
MAX_WORKERS = int(os.environ.get('GRPC_MAX_WORKERS', 10))


class HelloWorld(hello_pb2_grpc.HelloServicer):
    def printHello(self, request, context):
        logger.info('printHello id=%s', request.id)
        return hello_pb2.HelloWorldResponse(id=request.id)


def create_server(port, max_workers=MAX_WORKERS):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    hello_pb2_grpc.add_HelloServicer_to_server(HelloWorld(), server)
    # port 0 means pick any free port, returns the real one
    port = server.add_insecure_port(f'[::]:{port}')
    return server, port


def serve():
    server, port = create_server(PORT)
    server.start()
    logger.info('server started on port %s', port)

    done = threading.Event()

    def stop(signum, frame):
        logger.info('stopping server')
        # wait up to 5 sec for running calls to finish
        server.stop(5).wait()
        done.set()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    done.wait()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    serve()
