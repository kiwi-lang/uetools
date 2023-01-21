

build-doc:
	rm -rf api
	READTHEDOCS=True sphinx-build --color -c . -b html . _build/html

rm-doc:
	rm -rf Doxyfile ../Build/xml ../Build/html api/
	rm -rf _build

serve-doc:
	sphinx-serve

update-doc: build-doc serve-doc

yolo: rm-doc build-doc serve-doc

install-deps:
	apt-install doxygen
	apt-install graphviz
	pip install -r requirements.txt
