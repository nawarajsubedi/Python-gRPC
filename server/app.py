import logging
from concurrent import futures

import grpc

import hello_pb2
import hello_pb2_grpc

logger = logging.getLogger(__name__)


class HelloWorld(hello_pb2_grpc.HelloServicer):
    def printHello(self, request, context):
        logger.info('printHello id=%s', request.id)
        return hello_pb2.HelloWorldResponse(id=request.id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(HelloWorld(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info('server started on port 50051')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    serve()
