.PHONY: setup preview build deploy

setup:
	./setup.sh

preview:
	hugo server --buildDrafts --renderToMemory --bind 127.0.0.1

build:
	hugo --environment production --destination .build/site --cleanDestinationDir

deploy:
	./deploy.sh
