clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "*.swp" -exec rm -rf {} \;
	find . -name "*.swo" -exec rm -rf {} \;
	find . -name "node_modules" -exec rm -rf '{}' +
	-rm -r build/ dist/ horse.egg-info/


build:
	python setup.py sdist


upload: build
	twine upload dist/*


.PHONY: build upload clean
