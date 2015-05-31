build:
	docker build -t horse-server .

run: build
	docker run \
		-ti --rm \
		-p 0.0.0.0:5000:5000 \
		-v $(CURDIR)/app:/app \
		-v $(CURDIR)/.data:/data \
		horse-server
 
shell: build
	docker run \
		-ti --rm \
		-p 0.0.0.0:5000:5000 \
		-v $(CURDIR)/app:/app \
		-v $(CURDIR)/.data:/data \
		horse-server \
		bash

ngrok:
	ngrok http 5000

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.swp" -exec rm -rf {} \;
	find . -name "*.swo" -exec rm -rf {} \;
	find . -name "node_modules" -exec rm -rf '{}' +
