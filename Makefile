build:
	docker build -t horse-server .

run: build
	docker run -ti --rm -p 0.0.0.0:5000:5000 -v $(CURDIR)/app:/app horse-server
 
shell: build
	docker run -ti --rm -p 0.0.0.0:5000:5000 -v $(CURDIR)/app:/app horse-server bash

ngrok:
	ngrok http 5000
