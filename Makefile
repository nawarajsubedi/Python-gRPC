.PHONY: install proto server client test docker

install:
	pip install -r requirements-dev.txt

proto:
	sh scripts/gen_protos.sh

server:
	cd server && python app.py

client:
	cd client && python app.py

test:
	python -m pytest -v

docker:
	docker-compose up --build server
