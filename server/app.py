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
MAX_COUNT = 100


def get_name(request, context):
    name = request.name.strip()
    if not name:
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'name is required')
    return name


class LogInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        logger.info('call %s', handler_call_details.method)
        return continuation(handler_call_details)


class HelloWorld(hello_pb2_grpc.HelloServicer):
    def printHello(self, request, context):
        logger.info('printHello id=%s', request.id)
        return hello_pb2.HelloWorldResponse(id=request.id)

    def SayHello(self, request, context):
        name = get_name(request, context)
        return hello_pb2.GreetReply(message=f'Hello, {name}!')

    def SayHelloStream(self, request, context):
        name = get_name(request, context)
        count = request.count or 3
        if count < 1 or count > MAX_COUNT:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, f'count must be between 1 and {MAX_COUNT}')
        for i in range(count):
            # stop if client cancelled or deadline passed
            if not context.is_active():
                break
            yield hello_pb2.GreetReply(message=f'Hello, {name}! ({i + 1}/{count})')

    def SayHelloToMany(self, request_iterator, context):
        names = [r.name.strip() for r in request_iterator if r.name.strip()]
        if not names:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, 'send at least one name')
        return hello_pb2.GreetReply(message=f'Hello, {", ".join(names)}!')

    def Chat(self, request_iterator, context):
        for request in request_iterator:
            name = request.name.strip()
            if name:
                yield hello_pb2.GreetReply(message=f'Hello, {name}!')


def create_server(port, max_workers=MAX_WORKERS):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        interceptors=[LogInterceptor()],
    )
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
