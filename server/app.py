from concurrent import futures
import grpc

import hello_pb2
import hello_pb2_grpc


class HelloWorld(hello_pb2_grpc.HelloServicer):
    def printHello(self, request, context):
        print(request.id)
        return hello_pb2.HelloWorldResponse(id="10")
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(HelloWorld(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()