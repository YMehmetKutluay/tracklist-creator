project := tracklist

.PHONY: build
build:
	docker build . -t $(project)

.PHONY: app
app:
	docker-compose up app