.PHONY: setup preview build check deploy drafts

setup:
	./setup.sh

preview:
	hugo server --buildDrafts --renderToMemory --bind 127.0.0.1

build:
	hugo --environment production --destination .build/site --cleanDestinationDir --noBuildLock
	python3 scripts/prepare_release.py

check: build
	python3 scripts/check_site.py

drafts:
	hugo list drafts --noBuildLock

deploy:
	./deploy.sh
