.PHONY: 
	build

run:build
	docker run --name signalInfoBotContainer -v .:/code \
	--user $$(id -u):$$(id -g) \
	signal-info-bot:latest

build:remove
	docker build -t signal-info-bot:latest .

restart:
	docker restart signalInfoBotContainer
	docker attach signalInfoBotContainer

remove:
	docker rm signalInfoBotContainer

clean:remove
	docker rmi signal-info-bot

runNew:buildNew
	docker run --name signalInfoBotContainer -v .:/code \
	--user $$(id -u):$$(id -g) \
	signal-info-bot:latest

buildNew:
	docker build -t signal-info-bot:latest .

stop:
	docker stop signalInfoBotContainer

