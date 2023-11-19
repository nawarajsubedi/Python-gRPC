import grpc
import pytest

import hello_pb2


def test_print_hello_returns_same_id(stub):
    response = stub.printHello(hello_pb2.HelloWorldRequest(id='33'))
    assert response.id == '33'


def test_say_hello(stub):
    response = stub.SayHello(hello_pb2.GreetRequest(name='Nawaraj'))
    assert response.message == 'Hello, Nawaraj!'


def test_say_hello_strips_spaces(stub):
    response = stub.SayHello(hello_pb2.GreetRequest(name='  Ram  '))
    assert response.message == 'Hello, Ram!'


def test_say_hello_without_name(stub):
    with pytest.raises(grpc.RpcError) as e:
        stub.SayHello(hello_pb2.GreetRequest(name=''))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT
