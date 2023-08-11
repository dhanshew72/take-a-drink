ACTIVATE_VENV=. .venv/bin/activate

dev-env: clean
	python3 -m venv .venv
	$(ACTIVATE_VENV); pip3 install -r requirements.txt

clean:
	rm -rf .venv

run:
	$(ACTIVATE_VENV); python3 main.py

docker-run: docker-build
	docker run -d take-a-drink

docker-stop:
	docker stop take-a-drink

docker-build:
	docker build -t take-a-drink .
