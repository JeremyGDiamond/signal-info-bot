.PHONY: 
	build

run:build
	docker run --name signalInfoBotContainer -v .:/code signal-info-bot:latest

test:myTests
	docker run signal-info-bot:testing

build:remove
	docker build -t signal-info-bot:latest .

myTests:
	docker build -t signal-info-bot:testing .

restart:
	docker restart signalInfoBotContainer
	docker attach signalInfoBotContainer

remove:
	docker rm signalInfoBotContainer

clean:remove
	docker rmi signal-info-bot
