import grpc
import pytest

import hello_pb2


def test_say_hello_stream(stub):
    replies = list(stub.SayHelloStream(hello_pb2.GreetRequest(name='Ram', count=2)))
    assert [r.message for r in replies] == ['Hello, Ram! (1/2)', 'Hello, Ram! (2/2)']


def test_say_hello_stream_default_count(stub):
    replies = list(stub.SayHelloStream(hello_pb2.GreetRequest(name='Ram')))
    assert len(replies) == 3


@pytest.mark.parametrize('count', [-1, 101])
def test_say_hello_stream_bad_count(stub, count):
    with pytest.raises(grpc.RpcError) as e:
        list(stub.SayHelloStream(hello_pb2.GreetRequest(name='Ram', count=count)))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_say_hello_to_many(stub):
    requests = iter([hello_pb2.GreetRequest(name=n) for n in ['Ram', ' ', 'Sita']])
    response = stub.SayHelloToMany(requests)
    assert response.message == 'Hello, Ram, Sita!'


def test_say_hello_to_many_empty(stub):
    with pytest.raises(grpc.RpcError) as e:
        stub.SayHelloToMany(iter([]))
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_chat(stub):
    requests = iter([hello_pb2.GreetRequest(name=n) for n in ['Ram', '', 'Sita']])
    replies = [r.message for r in stub.Chat(requests)]
    assert replies == ['Hello, Ram!', 'Hello, Sita!']
