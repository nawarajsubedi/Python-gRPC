#!/bin/sh
# generate python code from protos/ into server and client folder
set -e

cd "$(dirname "$0")/.."

for dir in server client; do
    python -m grpc_tools.protoc -I protos --python_out=$dir --pyi_out=$dir --grpc_python_out=$dir protos/hello.proto
done
