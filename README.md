# Python gRPC

A small gRPC server and client in Python. The `Hello` service shows all four gRPC call types:

| RPC              | Type                 | What it does                                  |
|------------------|----------------------|-----------------------------------------------|
| `printHello`     | unary                | sends an id and gets the same id back         |
| `SayHello`       | unary                | greets one name                               |
| `SayHelloStream` | server streaming     | sends back `count` greetings (default 3)      |
| `SayHelloToMany` | client streaming     | send many names, get one greeting for all     |
| `Chat`           | bidirectional stream | replies to every name as it arrives           |

The service is defined in [protos/hello.proto](protos/hello.proto).

## Getting Started

### 1. Requirements

- Python 3.10 or newer
- pip

Check your version:
```bash
python3 --version
```

### 2. Clone the repository

```bash
git clone https://github.com/nawarajsubedi/Python-gRPC.git
cd Python-gRPC
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows use `.venv\Scripts\activate` instead.

### 4. Install dependencies

```bash
pip install -r requirements-dev.txt
```

`requirements.txt` has only what is needed to run the server and client, `requirements-dev.txt` also installs `grpcio-tools` and `pytest`.

### 5. Start the server

```bash
cd server
python app.py
```

You should see:
```
INFO server started on port 50051
```

Keep this terminal open.

### 6. Call the server from the client

Open a second terminal, activate the virtual environment again and run:

```bash
cd client
python app.py
```

It prints `33`, the id sent with `printHello`. The other calls:

```bash
python app.py say-hello Nawaraj
python app.py say-hello-stream Nawaraj --count 5
python app.py say-hello-many Ram Sita Hari
python app.py chat Ram Sita Hari
```

See all options with `python app.py -h`.

### 7. Stop the server

Press `Ctrl+C` in the server terminal. The server waits up to 5 seconds for running calls to finish before it exits.

## Configuration

| Variable           | Used by | Default           |
|--------------------|---------|-------------------|
| `GRPC_PORT`        | server  | `50051`           |
| `GRPC_MAX_WORKERS` | server  | `10`              |
| `GRPC_TARGET`      | client  | `localhost:50051` |
| `GRPC_TIMEOUT`     | client  | `5` (seconds)     |

Example:
```bash
GRPC_PORT=6000 python app.py                              # server
GRPC_TARGET=localhost:6000 python app.py say-hello Ram    # client
```

## Run with Docker

Requires Docker and docker-compose.

1. Build and start the server:
    ```bash
    docker-compose up --build -d server
    ```
2. Run the client against it:
    ```bash
    docker-compose run --rm client
    docker-compose run --rm client python client/app.py chat Ram Sita
    ```
3. Stop everything:
    ```bash
    docker-compose down
    ```

The server is also published on `localhost:50051`, so the local client from step 6 works too.

## Try it with grpcurl

The server has reflection turned on, so [grpcurl](https://github.com/fullstorydev/grpcurl) works without the proto file:

```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"name": "Ram"}' localhost:50051 hello.Hello/SayHello
grpcurl -plaintext -d '{"name": "Ram", "count": 2}' localhost:50051 hello.Hello/SayHelloStream
```

Health check:
```bash
grpcurl -plaintext -d '{"service": "hello.Hello"}' localhost:50051 grpc.health.v1.Health/Check
```
