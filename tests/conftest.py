import os
import sys

import grpc
import pytest

# server code imports hello_pb2 as a top level module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server'))

import app  # noqa: E402
import hello_pb2_grpc  # noqa: E402


@pytest.fixture(scope='session')
def channel():
    server, port = app.create_server(0)
    server.start()
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        yield channel
    server.stop(None)


@pytest.fixture
def stub(channel):
    return hello_pb2_grpc.HelloStub(channel)
