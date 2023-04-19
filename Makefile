project := tracklist

.PHONY: build
build:
	docker build . -t $(project)
