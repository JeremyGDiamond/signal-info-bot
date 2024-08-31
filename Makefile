.PHONY: 
	build

run:build
	docker rm signalInfoBotContainer
	docker run --name signalInfoBotContainer -v .:/code signal-info-bot:latest

test:myTests
	docker run signal-info-bot:testing

build:
	docker build -t signal-info-bot:latest .

myTests:
	docker build -t signal-info-bot:testing .

restart:
	docker restart signalInfoBotContainer
	docker attach signalInfoBotContainer	