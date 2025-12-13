.PHONY: all install clean

all: install
	python src/views/system_topology.py
	python src/views/data_pipeline.py
	python src/views/security_model.py
	python scripts/embed_images.py

install:
	pip install -r requirements.txt

clean:
	rm -f *.png *.svg