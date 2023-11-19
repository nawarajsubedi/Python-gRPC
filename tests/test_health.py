from grpc_health.v1 import health_pb2, health_pb2_grpc


def test_health_check(channel):
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(health_pb2.HealthCheckRequest(service='hello.Hello'))
    assert response.status == health_pb2.HealthCheckResponse.SERVING
