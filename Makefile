.PHONY: 
	build

run:build
	docker run -v .:/code signal-info-bot  	

test:myTests
	docker run signal-info-bot:testing

build:
	docker build -t signal-info-bot:latest .

myTests:
	docker build -t signal-info-bot:testing .