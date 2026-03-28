.PHONY: run up down reset logs rebuild freeze

run:
	uvicorn app.main:app --reload

up:
	docker compose up --build -d

down:
	docker compose down

reset:
	docker compose down -v

logs:
	docker compose logs -f

rebuild:
	docker compose down -v
	docker compose up --build -d

freeze:
	python3 -m pip freeze > requirements.txt